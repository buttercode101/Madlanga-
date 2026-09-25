import json, os, sqlite3, sys
ROOT=os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0,os.path.join(ROOT,"api"))
import server

def test_source_claim_integrity(tmp_path):
    old=server.DB; server.DB=str(tmp_path/"evidence.db")
    try:
        server.init_db()
        d=json.load(open(os.path.join(ROOT,"data","commission.json"),encoding="utf-8"))
        c=sqlite3.connect(server.DB)
        assert c.execute("SELECT COUNT(*) FROM sources").fetchone()[0]==len(d["sources"])
        assert c.execute("SELECT COUNT(*) FROM claims").fetchone()[0]==len(d["claims"])
        assert c.execute("SELECT COUNT(*) FROM claim_sources").fetchone()[0]==sum(len(x["sourceIds"]) for x in d["claims"])
        assert c.execute("SELECT COUNT(*) FROM claims c WHERE NOT EXISTS (SELECT 1 FROM claim_sources cs WHERE cs.claim_id=c.id)").fetchone()[0]==0
        assert c.execute("SELECT COUNT(*) FROM hearings").fetchone()[0]==178
        assert c.execute("SELECT COUNT(*) FROM hearings WHERE status='detailed'").fetchone()[0]==6
        c.close()
    finally: server.DB=old

def test_no_claim_without_source(tmp_path):
    old=server.DB; server.DB=str(tmp_path/"evidence.db")
    try:
        server.init_db(); c=sqlite3.connect(server.DB)
        assert c.execute("SELECT COUNT(*) FROM claims c WHERE NOT EXISTS (SELECT 1 FROM claim_sources cs WHERE cs.claim_id=c.id)").fetchone()[0]==0
        c.close()
    finally: server.DB=old
