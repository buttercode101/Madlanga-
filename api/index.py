import json
from pathlib import Path
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/"data"/"commission.json").read_text(encoding="utf-8"))
app=FastAPI(title="Madlanga Evidence Room API", version="1.0.0")

@app.get("/api")
def home():
    return {"name":"Madlanga Evidence Room","status":"online","mode":"evidence-first"}

@app.get("/api/status")
def status():
    return {"ok":True,**DATA["status"],"sources":len(DATA["sources"]),"claims":len(DATA["claims"]),"hearingsIndexed":178,"hearingsDetailed":len(DATA["hearings"])}

@app.get("/api/sources")
def sources():
    return {"items":DATA["sources"]}

@app.get("/api/claims")
def claims():
    return {"items":[{**c,"source_ids":c.get("sourceIds",[])} for c in DATA["claims"]]}

@app.get("/api/hearings")
def hearings(detailed: bool=False):
    items=list(reversed(DATA["hearings"])) if detailed else list(reversed(DATA["hearings"]))
    if not detailed:
        known={h["day"]:h for h in DATA["hearings"]}
        items=[known.get(day,{"day":day,"status":"index_only"}) for day in range(178,0,-1)]
    return {"items":items}

@app.get("/api/search")
def search(q: str=Query(default="")):
    term=q.strip().lower()
    if not term: return {"claims":[],"sources":[]}
    return {
        "claims":[{"id":c["id"],"statement":c["statement"],"classification":c["classification"]} for c in DATA["claims"] if term in (c["id"]+" "+c["statement"]+" "+c["classification"]).lower()],
        "sources":[{"id":s["id"],"title":s["title"],"tier":s["tier"],"url":s["url"]} for s in DATA["sources"] if term in (s["id"]+" "+s["title"]+" "+s["publisher"]).lower()]
    }

@app.get("/api/gate")
def gate():
    issues=[c["id"]+": no source" for c in DATA["claims"] if not c.get("sourceIds")]
    return {"status":"pass" if not issues else "blocked","reasons":issues,"rules":["every claim has source ids","classification is preserved","official findings are not emitted by Hermes"]}
