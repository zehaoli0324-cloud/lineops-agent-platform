import argparse
import json
from .runtime import Runtime
from .store import Store
from .simulator import SCENES, FAULTS

def main():
    p=argparse.ArgumentParser();sub=p.add_subparsers(dest='command',required=True)
    s=sub.add_parser('serve');s.add_argument('--host',default='127.0.0.1');s.add_argument('--port',type=int,default=8000)
    r=sub.add_parser('run');r.add_argument('--scene',choices=SCENES,default='glue');r.add_argument('--fault',choices=FAULTS,default='clog');r.add_argument('--mode',choices=['offline','llm'],default='offline');r.add_argument('--db',default='lineops.sqlite')
    sub.add_parser('suite');sub.add_parser('optical-check')
    a=p.parse_args()
    if a.command=='serve':
        import uvicorn
        from .api import create_app
        uvicorn.run(create_app(),host=a.host,port=a.port)
    elif a.command=='run':
        from .llm import LLMClient
        rt=Runtime(Store(a.db));rt.configure(a.scene,a.fault);print(json.dumps(rt.run(a.mode,LLMClient() if a.mode=='llm' else None),indent=2))
    elif a.command=='optical-check':
        from .optical import check
        print(json.dumps(check(),indent=2))
    else:
        rows=[]
        for scene in SCENES:
            for fault in FAULTS:
                rt=Runtime();rt.configure(scene,fault);r=rt.run();rows.append({'scene':scene,'injection':fault,'status':r['status'],'tool_calls':len(r['trace']),'actions':sum(t['tool']=='act' for t in r['trace'])})
        print(json.dumps({'mode':'offline-reference','cases':rows},indent=2))

if __name__=='__main__':main()
