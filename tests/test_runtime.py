import json
import tempfile
import time
import unittest
from pathlib import Path
import httpx
from fastapi.testclient import TestClient
from lineops.api import create_app
from lineops.runtime import Runtime, ToolError
from lineops.simulator import SCENES, FAULTS, World, measure
from lineops.store import Store
from lineops.llm import LLMClient

class SandboxTests(unittest.TestCase):
    def test_ten_case_contract(self):
        for scene in SCENES:
            for fault in FAULTS:
                with self.subTest(scene=scene,fault=fault):
                    rt=Runtime();rt.configure(scene,fault);r=rt.run()
                    self.assertEqual(r['status'],'handed_off' if fault=='persistent' else 'recovered')
                    self.assertEqual(bool(r['orders']),fault=='persistent')
                    final=r['trace'][-1]['result']
                    self.assertEqual(len(set(final['frame_ids'])),3)
                    self.assertEqual(final['recovered'],fault!='persistent')
                    # Tools contain observable state, not injection labels.
                    public=json.dumps([t['result'] for t in r['trace']])
                    self.assertNotIn('"_fault"',public);self.assertNotIn('"fault"',public)

    def test_measurement_comes_from_pixels(self):
        normal,png=World('glue','normal').capture();_,bad=World('glue','clog').capture()
        self.assertGreater(measure('glue',png)['value'],.9)
        self.assertLess(measure('glue',bad)['value'],.5)
        _,grey=World('glue','camera').capture()
        self.assertEqual(measure('glue',grey)['quality'],'invalid')
        self.assertIsNone(measure('glue',grey)['value'])

    def test_gateway_preconditions_and_replay(self):
        rt=Runtime();rt.configure('glue','clog');future=time.time()+60
        def act(i,n,v=0,expiry=future):return rt.action(i,n,v,expiry)
        for kwargs in [('a','clean_outlet',0,future),('b','pause',0,0),('c','pause',99,future),('d','shell',0,future),('e','pause',0,float('nan')),('f','pause',False,future)]:
            with self.assertRaises(ToolError):act(*kwargs)
            self.assertEqual(rt.world.version,0)
        receipt=act('p','pause');self.assertEqual(rt.world.version,1)
        self.assertEqual(act('p','pause'),receipt);self.assertEqual(rt.world.version,1)
        with self.assertRaises(ToolError):act('p','resume',1)
        act('fix','clean_outlet',1);act('go','resume',2)
        self.assertTrue(rt.verify()['recovered'])

    def test_wrong_action_does_not_fix_fault(self):
        rt=Runtime();rt.configure('filling','supply');future=time.time()+60
        for i,n in enumerate(['pause','clean_outlet','resume']):rt.action(str(i),n,i,future)
        self.assertFalse(rt.verify()['recovered'])

    def test_model_cannot_declare_recovery(self):
        class Pretender:
            def run(self,rt): pass
        rt=Runtime();rt.configure('glue','clog');r=rt.run('llm',Pretender())
        self.assertEqual(r['status'],'failed');self.assertFalse(r['trace'][-1]['result']['recovered'])

    def test_work_order_while_running_is_not_handoff(self):
        class IncorrectHandoff:
            def run(self,rt):rt.tool('planning','work_order',{'reason':'needs repair'})
        rt=Runtime();rt.configure('glue','persistent');self.assertEqual(rt.run('llm',IncorrectHandoff())['status'],'failed')

    def test_budget_and_operator_stop(self):
        rt=Runtime();rt.configure('glue','clog');self.assertEqual(rt.run(budget=1)['status'],'stopped')
        class Stopper:
            def run(self,rt):rt.stop_event.set()
        self.assertEqual(rt.run('llm',Stopper())['status'],'stopped')

    def test_unauthorized_tool_is_audited(self):
        rt=Runtime();rt.incident=rt.store.create('glue','llm')
        r=rt.tool('diagnostic','act',{'name':'pause'})
        self.assertIn('error',r);self.assertEqual(rt.world.version,0)
        self.assertEqual(len(rt.store.get(rt.incident)['trace']),1)

    def test_restart_marks_unfinished_and_retains_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            path=str(Path(d)/'audit.sqlite');rt=Runtime(Store(path));rt.incident=rt.store.create('glue','offline')
            rt.store.status(rt.incident,'running');o=rt.observe();iid=rt.incident;rt.store.db.close()
            store=Store(path);r=store.get(iid)
            self.assertEqual(r['status'],'failed');self.assertEqual(store.png(o['id'])[:8],b'\x89PNG\r\n\x1a\n')
            store.db.close()

    def test_api_images_validation_and_ui(self):
        with TestClient(create_app(Runtime())) as c:
            self.assertIn('设备运维',c.get('/').text)
            self.assertEqual(c.post('/api/operator/configure',json={'scene':'invalid'}).status_code,422)
            c.post('/api/operator/configure',json={'scene':'filling','fault':'clog'})
            r=c.post('/api/incidents',json={'mode':'offline'}).json();self.assertEqual(r['status'],'recovered')
            f=r['trace'][0]['result']['frame'];self.assertEqual(c.get(f).headers['content-type'],'image/png')
            self.assertEqual(c.get('/api/incidents/'+r['id']).json()['id'],r['id'])
            self.assertEqual(c.get('/api/frames/missing').status_code,404)

class ModelProtocolTests(unittest.TestCase):
    def test_function_call_roundtrip_across_roles(self):
        seen=[]
        def handler(request):
            body=json.loads(request.content);seen.append(body)
            # Each role calls one real read tool then receives its result before ending.
            if len(body['messages'])==1:
                return httpx.Response(200,json={'choices':[{'message':{'role':'assistant','content':None,'tool_calls':[{'id':'read1','type':'function','function':{'name':'observe','arguments':'{}'}}]}}]})
            self.assertEqual(body['messages'][-1]['role'],'tool')
            result=json.loads(body['messages'][-1]['content']);self.assertIn('measurement',result)
            return httpx.Response(200,json={'choices':[{'message':{'role':'assistant','content':'Observed.'}}]})
        llm=LLMClient('https://unit.invalid/chat/completions','fake-key','test-model',httpx.Client(transport=httpx.MockTransport(handler)))
        rt=Runtime();r=rt.run('llm',llm)
        self.assertEqual(r['status'],'recovered');self.assertEqual(r['mode'],'llm');self.assertEqual(len(seen),6)
        self.assertEqual({t['role'] for t in r['trace']},{'diagnostic','planning','verification'})
        self.assertNotIn('act',[t['function']['name'] for t in seen[0]['tools']])

    def test_provider_error_is_failed_without_persisting_secret(self):
        def handler(request):return httpx.Response(500,text='secret-token-do-not-store')
        llm=LLMClient('https://unit.invalid/chat/completions','fake-key','test-model',httpx.Client(transport=httpx.MockTransport(handler)))
        r=Runtime().run('llm',llm);self.assertEqual(r['status'],'failed')
        self.assertNotIn('secret-token',json.dumps(r))

    def test_turn_limit_stops_run(self):
        def handler(request):return httpx.Response(200,json={'choices':[{'message':{'tool_calls':[{'id':'x','type':'function','function':{'name':'observe','arguments':'{}'}}]}}]})
        llm=LLMClient('https://unit.invalid/chat/completions','fake-key','test-model',httpx.Client(transport=httpx.MockTransport(handler)))
        self.assertEqual(Runtime().run('llm',llm)['status'],'stopped')

if __name__=='__main__':unittest.main()
