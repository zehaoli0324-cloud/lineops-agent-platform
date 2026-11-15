import os
from pathlib import Path
from typing import Literal
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, Response
from pydantic import BaseModel, Field
from .runtime import Runtime
from .store import Store
from .llm import LLMClient

class Configure(BaseModel):
    scene: Literal['glue','filling']='glue'
    fault: Literal['normal','clog','supply','camera','persistent']='clog'

class Run(BaseModel):
    mode: Literal['offline','llm']='offline'
    budget: int=Field(default=48,ge=1,le=100)


def create_app(runtime=None):
    app=FastAPI(title='LineOps local sandbox',version='0.1.0');rt=runtime or Runtime(Store(os.getenv('LINEOPS_DB','lineops.sqlite')))
    app.state.runtime=rt
    @app.get('/',response_class=HTMLResponse)
    def index():return (Path(__file__).parent/'static/index.html').read_text()
    @app.get('/health')
    def health():return {'status':'ok','scope':'local-software-sandbox'}
    @app.post('/api/operator/configure')
    def configure(body:Configure):return rt.configure(body.scene,body.fault)
    @app.post('/api/incidents')
    def run(body:Run):
        # Endpoint is synchronous local v0.1; production queue is a later milestone.
        try:client=LLMClient() if body.mode=='llm' else None
        except ValueError as exc:raise HTTPException(400,str(exc))
        return rt.run(body.mode,client,body.budget)
    @app.post('/api/stop')
    def stop():rt.stop_event.set();return {'stop_requested':True}
    @app.get('/api/incidents')
    def incidents():
        with rt.lock:return rt.store.list()
    @app.get('/api/incidents/{iid}')
    def incident(iid:str):
        with rt.lock:r=rt.store.get(iid)
        if r is None:raise HTTPException(404,'unknown incident')
        return r
    @app.get('/api/frames/{fid}')
    def frame(fid:str):
        with rt.lock:p=rt.store.png(fid)
        if p is None:raise HTTPException(404,'unknown frame')
        return Response(p,media_type='image/png')
    return app
