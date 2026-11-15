"""Bounded tools, deterministic action constraints and evidence-based terminal states."""
import json
import math
import threading
import time
from uuid import uuid4
from .simulator import World, SCENES, ACTIONS, measure
from .store import Store

class ToolError(ValueError): pass
class BudgetExceeded(ToolError): pass

class Runtime:
    def __init__(self, store=None):
        self.store=store or Store(); self.world=World(); self.lock=threading.RLock()
        self.stop_event=threading.Event();self.incident=None;self.calls=0;self.budget=48;self.receipts={}

    def configure(self,scene,fault):
        with self.lock:
            self.world=World(scene,fault); self.receipts={}
            return {"scene":scene,"version":0,"running":True}

    def observe(self):
        o,png=self.world.capture(); m=measure(o['scene'],png);m['frame_id']=o['id'];o['measurement']=m
        self.store.frame(self.incident,o,png);return o

    def action(self, action_id, name, expected_version, expires_at):
        if not isinstance(action_id,str) or not action_id or len(action_id)>100: raise ToolError('invalid action_id')
        signature=json.dumps([name,expected_version,expires_at])
        if action_id in self.receipts:
            prior=self.receipts[action_id]
            if prior[0]!=signature: raise ToolError('action_id reused with different arguments')
            return prior[1]
        if name not in ACTIONS: raise ToolError('unknown action')
        if type(expected_version) is not int: raise ToolError('version must be an integer')
        if type(expires_at) not in (int,float) or not math.isfinite(expires_at): raise ToolError('expiry must be a finite epoch timestamp')
        if expires_at<=time.time(): raise ToolError('action expired')
        if expected_version!=self.world.version: raise ToolError('stale world version; observe again')
        if name in ('clean_outlet','refill_supply','clean_camera') and self.world.running:
            raise ToolError('maintenance requires paused device')
        before=self.world.version;self.world.mutate(name)
        result={"action_id":action_id,"accepted":True,"before_version":before,"after_version":self.world.version,"name":name}
        self.receipts[action_id]=(signature,result);return result

    def verify(self):
        obs=[self.observe() for _ in range(3)]
        valid=all(o['measurement']['quality']=='valid' and o['measurement']['value']>=SCENES[self.world.scene]['threshold'] and o['telemetry']['supply_pressure']>=.8 and o['telemetry']['running'] for o in obs)
        return {"recovered":valid,"frame_ids":[o['id'] for o in obs],"observations":obs,"rule":"three_valid_fresh_frames_v1"}

    def tool(self, role, name, args):
        if self.stop_event.is_set(): raise BudgetExceeded('operator stop')
        if self.calls>=self.budget: raise BudgetExceeded('tool budget exhausted')
        self.calls+=1
        permissions={'diagnostic':('observe','manual'), 'planning':('observe','manual','act','work_order'), 'verification':('observe','manual','verify'), 'offline':('observe','manual','act','work_order','verify')}
        try:
            if name not in permissions.get(role,()): raise ToolError('tool not allowed for role')
            if name=='observe': result=self.observe()
            elif name=='manual': result={"scene":self.world.scene,**SCENES[self.world.scene]}
            elif name=='act': result=self.action(**args)
            elif name=='work_order':
                reason=args['reason']
                if not isinstance(reason,str) or not reason.strip() or len(reason)>2000: raise ToolError('invalid work order reason')
                result=self.store.order(self.incident,reason)
            elif name=='verify': result=self.verify()
        except (ToolError,TypeError,KeyError) as exc: result={"error":str(exc)}
        self.store.trace(self.incident,role,name,args,result);return result

    def offline(self):
        o=self.tool('offline','observe',{})
        if self.tool('offline','verify',{})['recovered']: return
        choice='clean_camera' if o['measurement']['quality']!='valid' else ('refill_supply' if o['telemetry']['supply_pressure']<.8 else 'clean_outlet')
        for name in ('pause',choice,'resume'):
            o=self.tool('offline','observe',{})
            self.tool('offline','act',{'action_id':uuid4().hex,'name':name,'expected_version':o['version'],'expires_at':time.time()+60})
        if not self.tool('offline','verify',{})['recovered']:
            o=self.tool('offline','observe',{})
            self.tool('offline','act',{'action_id':uuid4().hex,'name':'pause','expected_version':o['version'],'expires_at':time.time()+60})
            self.tool('offline','work_order',{'reason':'Repair did not restore observed quality; requires maintenance investigation.'})

    def run(self, mode='offline', llm=None, budget=48):
        if mode not in ('offline','llm'):raise ValueError('unsupported mode')
        with self.lock:
            self.incident=self.store.create(self.world.scene,mode);self.calls=0;self.budget=budget;self.stop_event.clear()
            self.store.status(self.incident,'running')
            try:
                if mode=='offline':self.offline()
                else:
                    if llm is None:raise ValueError('LLM client is required')
                    llm.run(self)
                # This verifier is mandatory, independent of model prose or tool success.
                if self.stop_event.is_set():raise BudgetExceeded('operator stop')
                if self.calls>=self.budget:raise BudgetExceeded('tool budget exhausted before final verification')
                final=self.tool('verification','verify',{})
                orders=self.store.get(self.incident)['orders']
                state='recovered' if final['recovered'] else ('handed_off' if orders and not self.world.running else 'failed')
                self.store.status(self.incident,state,'deterministic final verification')
            except BudgetExceeded as exc:self.store.status(self.incident,'stopped',str(exc))
            except Exception as exc:
                # Do not persist endpoint errors that could contain secrets or request headers.
                self.store.status(self.incident,'failed',type(exc).__name__)
            return self.store.get(self.incident)
