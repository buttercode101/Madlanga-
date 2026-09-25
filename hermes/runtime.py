"""Deterministic Hermes runtime boundary.

This module deliberately contains no LLM call. It provides the enforceable evidence
contract that an eventual model adapter must satisfy.
"""
from dataclasses import dataclass, field
from typing import Any

ALLOWED={"FACT","MANDATE","RECORD","TESTIMONY","ALLEGATION","ANALYSIS","INFERENCE"}

@dataclass
class EvidenceItem:
    id: str
    text: str
    classification: str
    source_ids: list[str]=field(default_factory=list)
    location: str|None=None

@dataclass
class HermesResult:
    answer: str
    claims: list[dict[str,Any]]
    conflicts: list[dict[str,Any]]=field(default_factory=list)
    evidence_gaps: list[str]=field(default_factory=list)
    gate: dict[str,Any]=field(default_factory=dict)

class EvidenceGate:
    def validate(self, items:list[EvidenceItem]) -> tuple[bool,list[str]]:
        reasons=[]
        for item in items:
            if item.classification not in ALLOWED:
                reasons.append(f"{item.id}: invalid classification")
            if not item.source_ids:
                reasons.append(f"{item.id}: missing source ids")
        return (not reasons,reasons)

    def package(self, answer:str, items:list[EvidenceItem], conflicts=None) -> HermesResult:
        ok,reasons=self.validate(items)
        claims=[{
            "text":i.text,
            "classification":i.classification,
            "source_ids":i.source_ids,
            "transcript_location":i.location,
            "verification_state":"verified" if i.classification in {"FACT","MANDATE","RECORD"} else "partial"
        } for i in items]
        return HermesResult(
            answer=answer,
            claims=claims,
            conflicts=conflicts or [],
            evidence_gaps=reasons,
            gate={"status":"pass" if ok else "blocked","reasons":reasons}
        )
