"""OpenAI-compatible Chat Completions function tools; no provider SDK dependency."""
import json
import os
import httpx

FUNCTIONS={
'observe':('Capture a new frame, measure pixels, read telemetry and current world version.',{}),
'manual':('Read scenario manual and recovery threshold.',{}),
'act':('Execute one sandbox action. Maintenance requires pause. Use fresh observed version and future epoch expires_at.',{'action_id':{'type':'string'},'name':{'type':'string','enum':['pause','resume','clean_outlet','refill_supply','clean_camera']},'expected_version':{'type':'integer'},'expires_at':{'type':'number'}}),
'work_order':('Create maintenance handoff with unresolved evidence.',{'reason':{'type':'string'}}),
'verify':('Check three fresh frames and process state for recovery.',{})}
ROLES={'diagnostic':['observe','manual'],'planning':['observe','manual','act','work_order'],'verification':['observe','manual','verify']}

class LLMClient:
    def __init__(self,url=None,key=None,model=None,client=None):
        self.url=url or os.getenv('LINEOPS_LLM_URL','https://api.openai.com/v1/chat/completions')
        self.key=key or os.getenv('LINEOPS_API_KEY');self.model=model or os.getenv('LINEOPS_MODEL')
        if not self.key or not self.model:raise ValueError('Set LINEOPS_API_KEY and LINEOPS_MODEL')
        self.client=client or httpx.Client(timeout=45)

    def run(self,runtime):
        import time
        context=[]
        for role,names in ROLES.items():
            messages=[{'role':'system','content':f'You are the {role} role for a local industrial software sandbox. Use tools to collect evidence. Never invent tool results. Diagnose first, plan and execute allowed repair or handoff second, verify third. Read manual. For maintenance pause first, then clean outlet/refill supply/clean camera, then resume and inspect. Persistent faults require pause and work order. Do not ask the user. Current epoch seconds: {time.time()}. Prior roles: '+json.dumps(context)}]
            tools=[{'type':'function','function':{'name':n,'description':FUNCTIONS[n][0],'parameters':{'type':'object','properties':FUNCTIONS[n][1],'required':list(FUNCTIONS[n][1]),'additionalProperties':False}}} for n in names]
            for _ in range(12):
                if runtime.stop_event.is_set():
                    from .runtime import BudgetExceeded
                    raise BudgetExceeded('operator stop')
                response=self.client.post(self.url,headers={'Authorization':'Bearer '+self.key},json={'model':self.model,'messages':messages,'tools':tools,'tool_choice':'auto'})
                response.raise_for_status();message=response.json()['choices'][0]['message']
                calls=message.get('tool_calls') or []
                # Keep only protocol fields, not arbitrary provider metadata.
                assistant={'role':'assistant','content':message.get('content')}
                if calls:assistant['tool_calls']=calls
                messages.append(assistant)
                if not calls:break
                for call in calls:
                    name=call['function']['name']
                    args=json.loads(call['function']['arguments'])
                    if not isinstance(args,dict):raise ValueError('tool arguments must be an object')
                    result=runtime.tool(role,name,args)
                    messages.append({'role':'tool','tool_call_id':call['id'],'content':json.dumps(result)})
                    context.append({'role':role,'tool':name,'result':result})
            else:
                from .runtime import BudgetExceeded
                raise BudgetExceeded('model turn limit exhausted')
