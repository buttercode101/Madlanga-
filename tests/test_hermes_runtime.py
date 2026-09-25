import os,sys
ROOT=os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0,ROOT)
from hermes.runtime import EvidenceGate, EvidenceItem

def test_gate_blocks_unsourced_claim():
    ok,reasons=EvidenceGate().validate([EvidenceItem("x","unsupported","FACT",[])])
    assert not ok and "missing source ids" in reasons[0]

def test_gate_preserves_allegation():
    r=EvidenceGate().package("Reported allegation",[
        EvidenceItem("a","A witness alleged X","ALLEGATION",["source-1"])
    ])
    assert r.gate["status"]=="pass"
    assert r.claims[0]["classification"]=="ALLEGATION"
    assert r.claims[0]["verification_state"]=="partial"
