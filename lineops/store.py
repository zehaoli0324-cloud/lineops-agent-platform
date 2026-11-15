import json
import sqlite3
from datetime import datetime, timezone
from uuid import uuid4


def now(): return datetime.now(timezone.utc).isoformat()

class Store:
    """SQLite audit and immutable PNG evidence. World recovery is not yet implemented."""
    def __init__(self, path=":memory:"):
        self.db = sqlite3.connect(path, check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS incidents(id TEXT PRIMARY KEY, scene TEXT, mode TEXT, status TEXT, started_at TEXT, finished_at TEXT, detail TEXT);
        CREATE TABLE IF NOT EXISTS traces(seq INTEGER PRIMARY KEY AUTOINCREMENT, incident_id TEXT, at TEXT, role TEXT, tool TEXT, arguments TEXT, result TEXT);
        CREATE TABLE IF NOT EXISTS frames(id TEXT PRIMARY KEY, incident_id TEXT, observation TEXT, png BLOB);
        CREATE TABLE IF NOT EXISTS orders(id TEXT PRIMARY KEY, incident_id TEXT, reason TEXT, status TEXT);
        """)
        # Incomplete runs are explicit failures on process restart, never silently recovered.
        self.db.execute("UPDATE incidents SET status='failed', finished_at=?, detail=? WHERE status IN ('created','running')", (now(), 'runtime restarted; world state unavailable'))
        self.db.commit()

    def create(self, scene, mode):
        i=uuid4().hex
        self.db.execute("INSERT INTO incidents VALUES(?,?,?,?,?,?,?)", (i,scene,mode,'created',now(),None,'')); self.db.commit(); return i

    def status(self, i, status, detail=''):
        self.db.execute("UPDATE incidents SET status=?, finished_at=?, detail=? WHERE id=?", (status,None if status=='running' else now(),detail,i)); self.db.commit()

    def trace(self,i,role,tool,args,result):
        self.db.execute("INSERT INTO traces(incident_id,at,role,tool,arguments,result) VALUES(?,?,?,?,?,?)", (i,now(),role,tool,json.dumps(args),json.dumps(result))); self.db.commit()

    def frame(self,i,o,png):
        self.db.execute("INSERT INTO frames VALUES(?,?,?,?)",(o['id'],i,json.dumps(o),png));self.db.commit()

    def order(self,i,reason):
        oid=uuid4().hex;self.db.execute("INSERT INTO orders VALUES(?,?,?,?)",(oid,i,reason,'open'));self.db.commit();return {"id":oid,"status":"open"}

    def get(self,i):
        row=self.db.execute("SELECT * FROM incidents WHERE id=?",(i,)).fetchone()
        if row is None: return None
        result=dict(row);result['trace']=[]
        for r in self.db.execute("SELECT * FROM traces WHERE incident_id=? ORDER BY seq",(i,)):
            v=dict(r); v['arguments']=json.loads(v['arguments']);v['result']=json.loads(v['result']);result['trace'].append(v)
        result['orders']=[dict(r) for r in self.db.execute("SELECT * FROM orders WHERE incident_id=?",(i,))]
        return result

    def list(self): return [dict(r) for r in self.db.execute("SELECT * FROM incidents ORDER BY started_at DESC LIMIT 100")]
    def png(self,fid):
        row=self.db.execute("SELECT png FROM frames WHERE id=?",(fid,)).fetchone()
        return bytes(row['png']) if row else None
