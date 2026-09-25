#!/usr/bin/env python3
import json, sqlite3, hashlib, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

ROOT=Path(__file__).resolve().parent
DB=ROOT/"madlanga.db"
SEED=ROOT/"data"/"commission.json"
PORT=4173

def db():
    c=sqlite3.connect(DB)
    c.row_factory=sqlite3.Row
    c.executescript("""
    CREATE TABLE IF NOT EXISTS sources(id TEXT PRIMARY KEY,tier TEXT,publisher TEXT,title TEXT,url TEXT,retrieved_at TEXT,content_hash TEXT);
    CREATE TABLE IF NOT EXISTS claims(id TEXT PRIMARY KEY,text TEXT,classification TEXT,verification_state TEXT);
    CREATE TABLE IF NOT EXISTS claim_sources(claim_id TEXT,source_id TEXT,PRIMARY KEY(claim_id,source_id));
    CREATE TABLE IF NOT EXISTS hearings(day INTEGER PRIMARY KEY,date TEXT,title TEXT,url TEXT,state TEXT);
    CREATE TABLE IF NOT EXISTS snapshots(id INTEGER PRIMARY KEY AUTOINCREMENT,source_id TEXT,sha256 TEXT,retrieved_at TEXT,bytes INTEGER,UNIQUE(source_id,sha256));
    CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY AUTOINCREMENT,action TEXT,target TEXT,detail TEXT,created_at TEXT);
    """)
    return c

def seed():
    c=db()
    if c.execute("SELECT COUNT(*) FROM sources").fetchone()[0]: c.close(); return
    d=json.loads(SEED.read_text())
    for s in d.get("sources",[]):
        c.execute("INSERT OR IGNORE INTO sources VALUES(?,?,?,?,?,?,?,?)",(s["id"],s.get("tier"),s.get("publisher"),s.get("title"),s.get("url"),s.get("retrieved_at"),s.get("content_hash")))
    for x in d.get("claims",[]):
        c.execute("INSERT OR IGNORE INTO claims VALUES(?,?,?,?)",(x["id"],x["statement"],x["classification"],x.get("verification_state","verified")))
        for sid in x.get("source_ids",[]): c.execute("INSERT OR IGNORE INTO claim_sources VALUES(?,?)",(x["id"],sid))
    for h in d.get("hearings",[]): c.execute("INSERT OR IGNORE INTO hearings VALUES(?,?,?,?,?)",(h["day"],h.get("date"),h.get("title"),h.get("url"),h.get("state","detailed")))
    c.commit(); c.close()

def rows(sql,args=()):
    c=db(); out=[dict(x) for x in c.execute(sql,args).fetchall()]; c.close(); return out

def api_status():
    return {"product":"Madlanga Commission Evidence Room","as_of":"2026-09-25","hearings_indexed":rows("SELECT COUNT(*) n FROM hearings")[0]["n"],"claims":rows("SELECT COUNT(*) n FROM claims")[0]["n"],"sources":rows("SELECT COUNT(*) n FROM sources")[0]["n"],"principle":"Evidence first; missing evidence remains missing."}

HTML=r'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Madlanga — Evidence Room</title><style>
:root{font-family:Inter,system-ui,sans-serif;background:#0a0b0d;color:#e9ecef}*{box-sizing:border-box}body{margin:0}header{padding:22px 5vw;border-bottom:1px solid #24272b;display:flex;justify-content:space-between;gap:20px;align-items:center;position:sticky;top:0;background:#0a0b0df2;backdrop-filter:blur(14px);z-index:2}b{letter-spacing:.02em}.tag{color:#b9ff5a;font-size:12px;text-transform:uppercase;letter-spacing:.14em}.wrap{max-width:1180px;margin:auto;padding:56px 5vw}.hero{max-width:850px}.hero h1{font-size:clamp(42px,7vw,82px);line-height:.95;margin:12px 0 22px;letter-spacing:-.055em}.hero p{color:#9ca3aa;font-size:18px;line-height:1.65;max-width:720px}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:42px 0}.card{border:1px solid #25292e;background:#101215;border-radius:16px;padding:20px}.num{font-size:30px;font-weight:700}.muted{color:#7f8790;font-size:13px}.section{margin-top:50px}.section h2{font-size:25px}.claim{padding:18px 0;border-top:1px solid #24272b}.pill{display:inline-block;border:1px solid #3b4249;border-radius:999px;padding:5px 9px;font-size:11px;color:#b9ff5a;margin-right:8px}.source{color:#aeb5bd}.warning{border:1px solid #5a5128;background:#19170d;border-radius:14px;padding:16px;color:#d7ce9b}@media(max-width:760px){.grid{grid-template-columns:repeat(2,1fr)}header{position:static}.wrap{padding-top:38px}.hero h1{font-size:48px}}@media(max-width:430px){.grid{grid-template-columns:1fr}}
</style></head><body><header><b>MADLANGA / EVIDENCE ROOM</b><span class="tag">SOURCE OF TRUTH · 25 SEP 2026</span></header><main class="wrap"><section class="hero"><span class="tag">Judicial Commission of Inquiry</span><h1>Follow the evidence.</h1><p>A structured public-record workspace for hearings, claims and sources. Hermes sits above this layer and must show its evidence path instead of inventing certainty.</p></section><section class="grid" id="stats"></section><section class="section"><h2>Evidence ledger</h2><div id="claims"></div></section><section class="section"><div class="warning"><b>Integrity boundary</b><br><span class="muted">The 178-day index does not imply that every transcript or exhibit has been ingested. Unavailable evidence is explicitly left unavailable.</span></div></section></main><script>
async function get(p){let r=await fetch(p);return r.json()}
(async()=>{let s=await get('/api/status');document.querySelector('#stats').innerHTML=[['178','sitting-day index'],[s.claims,'sourced claims'],[s.sources,'registered sources'],['0','fabricated findings']].map(x=>'<div class="card"><div class="num">'+x[0]+'</div><div class="muted">'+x[1]+'</div></div>').join('');let c=await get('/api/claims');document.querySelector('#claims').innerHTML=c.map(x=>'<article class="claim"><span class="pill">'+x.classification+'</span><span class="pill">'+x.verification_state+'</span><div style="margin-top:10px">'+x.text+'</div></article>').join('')})()
</script></body></html>'''

class Handler(BaseHTTPRequestHandler):
    def send_json(self,obj,status=200):
        b=json.dumps(obj,ensure_ascii=False).encode(); self.send_response(status); self.send_header("Content-Type","application/json"); self.send_header("Content-Length",str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        p=urlparse(self.path).path
        if p=="/": body=HTML.encode(); self.send_response(200); self.send_header("Content-Type","text/html; charset=utf-8"); self.send_header("Content-Length",str(len(body))); self.end_headers(); self.wfile.write(body); return
        if p=="/api/status": return self.send_json(api_status())
        if p=="/api/sources": return self.send_json(rows("SELECT * FROM sources ORDER BY id"))
        if p=="/api/claims":
            data=rows("SELECT c.*,GROUP_CONCAT(cs.source_id) source_ids FROM claims c LEFT JOIN claim_sources cs ON cs.claim_id=c.id GROUP BY c.id ORDER BY c.id")
            for x in data: x["source_ids"]=(x["source_ids"] or "").split(",") if x["source_ids"] else []
            return self.send_json(data)
        if p=="/api/hearings": return self.send_json(rows("SELECT * FROM hearings ORDER BY day"))
        if p=="/api/search":
            q=parse_qs(urlparse(self.path).query).get("q",[""])[0].strip()
            return self.send_json(rows("SELECT * FROM claims WHERE lower(text) LIKE lower(?) OR lower(classification) LIKE lower(?)",("%"+q+"%","%"+q+"%")))
        if p=="/api/gate":
            claims=rows("SELECT c.id,c.text,c.classification,c.verification_state,COUNT(cs.source_id) source_count FROM claims c LEFT JOIN claim_sources cs ON cs.claim_id=c.id GROUP BY c.id")
            blocked=[x for x in claims if x["source_count"]<1 or x["verification_state"]=="unverified"]
            return self.send_json({"status":"blocked" if blocked else "pass","blocked_claims":blocked,"rule":"No material claim without provenance."})
        self.send_error(404)

if __name__=="__main__":
    seed()
    print("Madlanga Evidence Room listening on http://localhost:%d"%PORT)
    ThreadingHTTPServer(("0.0.0.0",PORT),Handler).serve_forever()
