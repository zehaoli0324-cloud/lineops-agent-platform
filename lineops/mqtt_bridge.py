"""Optional read-only API -> MQTT bridge; no MQTT command subscription."""
import argparse
import json
import time
import httpx

def tags(incident):
    t=next((t for t in reversed(incident['trace']) if t['tool']=='verify' and 'observations' in t['result']),None)
    observation=t['result']['observations'][-1] if t else None
    return {'incident_id':incident['id'],'status':incident['status'],'scene':incident['scene'],
            'mode':incident['mode'],'telemetry':observation['telemetry'] if observation else {},
            'measurement':observation['measurement'] if observation else {}}

def main():
    p=argparse.ArgumentParser();p.add_argument('--api',default='http://127.0.0.1:8000');p.add_argument('--broker',default='127.0.0.1');a=p.parse_args()
    import paho.mqtt.client as mqtt
    client=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2);client.connect(a.broker,1883,60);client.loop_start()
    try:
        with httpx.Client(timeout=120) as h:
            while True:
                try:
                    rows=h.get(a.api+'/api/incidents');rows.raise_for_status()
                    if rows.json():
                        detail=h.get(a.api+'/api/incidents/'+rows.json()[0]['id']);detail.raise_for_status();r=detail.json()
                        info=client.publish('lineops/'+r['scene']+'/state',json.dumps(tags(r)),qos=1,retain=True);info.wait_for_publish(timeout=5)
                except (httpx.HTTPError,RuntimeError) as exc:print(type(exc).__name__,flush=True)
                time.sleep(2)
    finally:client.loop_stop();client.disconnect()

if __name__=='__main__':main()
