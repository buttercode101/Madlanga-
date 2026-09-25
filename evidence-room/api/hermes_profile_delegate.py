#!/usr/bin/env python3
"""
Real Hermes Profile Delegation for Madlanga Commission
Uses terminal commands to invoke specific Hermes profiles for each agent step.
Includes full data context so profiles can work with real evidence.
"""

import json
import subprocess
import os
from typing import Dict, Any, List, Optional
from pathlib import Path

# Load commission data once
COMMISSION_DATA = None
def get_commission_data():
    global COMMISSION_DATA
    if COMMISSION_DATA is None:
        with open('/home/ubuntu/.hermes/cache/documents/madlanga-extracted/madlanga-work/data/commission.json') as f:
            COMMISSION_DATA = json.load(f)
    return COMMISSION_DATA

# Load contradictions from DB
CONTRADICTIONS_DATA = None
def get_contradictions_data():
    global CONTRADICTIONS_DATA
    if CONTRADICTIONS_DATA is None:
        import sqlite3
        conn = sqlite3.connect('/home/ubuntu/.hermes/cache/documents/madlanga-extracted/madlanga-work/data/evidence.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM contradictions')
        rows = cursor.fetchall()
        cols = [d[0] for d in cursor.description]
        CONTRADICTIONS_DATA = [dict(zip(cols, row)) for row in rows]
        conn.close()
    return CONTRADICTIONS_DATA

HERMES_HOME = Path.home() / '.hermes'
HERMES_BIN = 'hermes'

PROFILE_MAP = {
    'evidence': 'madlanga-evidence',
    'chronology': 'madlanga-evidence',  # Same profile handles chronology
    'network': 'madlanga-network',
    'contradiction': 'madlanga-contradiction',
    'docket': 'madlanga-evidence',  # Evidence profile handles docket
    'research': 'madlanga-research',
    'chair': 'madlanga-chair',
    'verification': 'madlanga-verification',
    'redteam': 'madlanga-redteam',
}

def run_hermes_profile(profile_name: str, prompt: str, timeout: int = 120) -> Dict[str, Any]:
    """
    Run a Hermes profile with a specific prompt and return the response.
    
    Uses: hermes profile use <profile> && hermes -z "<prompt>"
    """
    profile = PROFILE_MAP.get(profile_name, profile_name)
    
    # Build the command - use -z for oneshot mode
    cmd = [
        'bash', '-c',
        f'hermes profile use {profile} && hermes -z {json.dumps(prompt)}'
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=os.environ.copy()
        )
        
        # Strip "Switched to: <profile>" from stdout
        stdout = result.stdout
        if stdout.startswith('Switched to:'):
            stdout = '\n'.join(stdout.split('\n')[1:])
        
        return {
            'success': result.returncode == 0,
            'stdout': stdout.strip(),
            'stderr': result.stderr.strip(),
            'profile': profile
        }
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'error': f'Timeout after {timeout}s',
            'profile': profile
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'profile': profile
        }

def _build_data_context() -> str:
    """Build a data context string with all relevant commission data"""
    data = get_commission_data()
    contras = get_contradictions_data()
    
    # Build concise data summary for prompts
    claims_summary = []
    for c in data['claims']:
        claims_summary.append({
            'id': c['id'],
            'statement': c['statement'][:200],
            'sourceIds': c['sourceIds'],
            'status': c.get('status', 'untested')
        })
    
    sources_summary = []
    for s in data['sources']:
        sources_summary.append({
            'id': s['id'],
            'tier': s['tier'],
            'url': s['url'][:80]
        })
    
    return json.dumps({
        'claims': claims_summary,
        'sources': sources_summary,
        'contradictions': contras,
        'people': data.get('people', []),
        'hearings': data.get('hearings', [])
    }, indent=2)

DATA_CONTEXT = _build_data_context()

def run_evidence_profile(query: Dict[str, Any]) -> Dict[str, Any]:
    """Run evidence retrieval via madlanga-evidence profile"""
    prompt = f"""You are the Evidence Agent for the Madlanga Commission.
Your SOUL: I inherit CONSTITUTION.md, EVIDENCE_PROTOCOL.md, SOURCE_HIERARCHY.md, FINDING_GATE.md. My role is source retrieval, evidence mapping, provenance.

COMMISSION DATA:
{DATA_CONTEXT}

QUERY: {json.dumps(query)}

TASK: Perform evidence retrieval and provenance mapping.
Return ONLY valid JSON with these exact keys:
{{
  "source_ids": [{{"id": "s1", "tier": "PRIMARY"}}],
  "doc_ids": [],
  "claim_ids": ["C-001"],
  "question_ids": []
}}"""
    return run_hermes_profile('evidence', prompt)

def run_chronology_profile(evidence: Dict[str, Any]) -> Dict[str, Any]:
    """Run chronology analysis via madlanga-evidence profile"""
    prompt = f"""You are the Chronology Agent for the Madlanga Commission.
Your SOUL: I inherit CONSTITUTION.md, EVIDENCE_PROTOCOL.md, SOURCE_HIERARCHY.md, FINDING_GATE.md. My role is ordering events, flagging temporal conflicts.

COMMISSION DATA:
{DATA_CONTEXT}

EVIDENCE FROM PREVIOUS STEP:
{json.dumps(evidence)}

TASK: Order events and flag temporal conflicts.
Return ONLY valid JSON with these exact keys:
{{
  "events_ordered": [{{"claim_id": "C-001", "date": "2025-07-23", "event": "Commission established", "source": "claim"}}],
  "temporal_conflicts": [],
  "sequence_gaps": []
}}"""
    return run_hermes_profile('chronology', prompt)

def run_network_profile(evidence: Dict[str, Any], chronology: Dict[str, Any]) -> Dict[str, Any]:
    """Run network mapping via madlanga-network profile"""
    prompt = f"""You are the Network Agent for the Madlanga Commission.
Your SOUL: I inherit CONSTITUTION.md, EVIDENCE_PROTOCOL.md, SOURCE_HIERARCHY.md, FINDING_GATE.md. My role is entity/relationship mapping from sourced evidence. Map people relationships only from Tier 1-4.

COMMISSION DATA:
{DATA_CONTEXT}

EVIDENCE: {json.dumps(evidence)}
CHRONOLOGY: {json.dumps(chronology)}

TASK: Map entities and relationships from Tier 1-4 sources only.
Return ONLY valid JSON with these exact keys:
{{
  "relationships": [{{"from": "person.madlanga.mbuyiseli", "to": "person.mkhwanazi.nhlanhla", "type": "alleged_association", "strength": "alleged", "source": "C-003", "claim": "Mkhwanazi testified about Madlanga"}}],
  "entities": ["person.madlanga.mbuyiseli", "person.mkhwanazi.nhlanhla"],
  "strength_assessment": {{"person.madlanga.mbuyiseli->person.mkhwanazi.nhlanhla": "alleged (Tier 3)"}}
}}"""
    return run_hermes_profile('network', prompt)

def run_contradiction_profile(evidence: Dict[str, Any], network: Dict[str, Any]) -> Dict[str, Any]:
    """Run contradiction detection via madlanga-contradiction profile"""
    prompt = f"""You are the Contradiction Agent for the Madlanga Commission.
Your SOUL: I inherit CONSTITUTION.md, EVIDENCE_PROTOCOL.md, SOURCE_HIERARCHY.md, FINDING_GATE.md. My role is detect conflicting testimony/documents.

COMMISSION DATA:
{DATA_CONTEXT}

EVIDENCE: {json.dumps(evidence)}
NETWORK: {json.dumps(network)}

TASK: Detect conflicting testimony/documents and create contradiction_ids.
Return ONLY valid JSON with these exact keys:
{{
  "contradictions": ["contra.mkhwanazi.vs.sibiya.dockets"],
  "conflict_types": [{{"contradiction_id": "contra.mkhwanazi.vs.sibiya.dockets", "claim_id": "C-003", "type": "direct_conflict", "status": "identified"}}],
  "resolution_status": {{"contra.mkhwanazi.vs.sibiya.dockets": "unresolved"}}
}}"""
    return run_hermes_profile('contradiction', prompt)

def run_docket_profile(evidence: Dict[str, Any], chronology: Dict[str, Any]) -> Dict[str, Any]:
    """Run docket/procedural state via madlanga-evidence profile"""
    prompt = f"""You are the Docket Agent for the Madlanga Commission.
Your SOUL: I inherit CONSTITUTION.md, EVIDENCE_PROTOCOL.md, SOURCE_HIERARCHY.md, FINDING_GATE.md. My role is attach procedural state hearing_id/day.

COMMISSION DATA:
{DATA_CONTEXT}

EVIDENCE: {json.dumps(evidence)}
CHRONOLOGY: {json.dumps(chronology)}

TASK: Attach procedural state including hearing_id and day.
Return ONLY valid JSON with these exact keys:
{{
  "current_hearing": "hearing.2026-09-23.day178",
  "procedural_state": {{"total_hearing_days": 178, "transcripts_ingested": 40, "latest_hearing": "Day 178 (2026-09-23)", "status": "active"}}
}}"""
    return run_hermes_profile('docket', prompt)

def run_research_profile(evidence: Dict[str, Any], verification: Dict[str, Any]) -> Dict[str, Any]:
    """Run research for gaps via madlanga-research profile"""
    prompt = f"""You are the Research Agent for the Madlanga Commission.
Your SOUL: I inherit CONSTITUTION.md, EVIDENCE_PROTOCOL.md, SOURCE_HIERARCHY.md, FINDING_GATE.md. My role is targeted research and evidence-gap discovery.

COMMISSION DATA:
{DATA_CONTEXT}

EVIDENCE GAPS: {json.dumps(evidence.get('question_ids', []))}
VERIFICATION RESULTS: {json.dumps(verification.get('gate_checks', {}))}

TASK: Research targeted sources to fill evidence gaps.
Return ONLY valid JSON with these exact keys:
{{
  "questions_addressed": [],
  "new_sources": [],
  "remaining_gaps": []
}}"""
    return run_hermes_profile('research', prompt)

def run_chair_profile(context: Dict[str, Any]) -> Dict[str, Any]:
    """Run chair synthesis via madlanga-chair profile"""
    prompt = f"""You are the Chair Agent for the Madlanga Commission.
Your SOUL: I inherit CONSTITUTION.md, EVIDENCE_PROTOCOL.md, SOURCE_HIERARCHY.md, FINDING_GATE.md. My role is procedural synthesis, mandate, decision framing. I may not act outside it. No unilateral finding — I frame, gate decides.

COMMISSION DATA:
{DATA_CONTEXT}

ALL PREVIOUS STEPS: {json.dumps(context)}

TASK: Frame procedural synthesis WITHOUT issuing factual findings.
Return ONLY valid JSON with these exact keys:
{{
  "procedural_frame": "Evidence gathered for 1 claims. 2 Tier 1-4 sources identified. Procedural state: active.",
  "mandate_engaged": [{{"claim": "C-001", "mandate_clause": "establishment", "status": "corroborated"}}],
  "evidence_sufficiency": "sufficient"
}}"""
    return run_hermes_profile('chair', prompt)

def run_verification_profile(chair: Dict[str, Any], evidence: Dict[str, Any], contradiction: Dict[str, Any]) -> Dict[str, Any]:
    """Run verification via madlanga-verification profile"""
    template = """{
  "gate_checks": {
    "tier_sufficiency": {"pass": true, "tier_1_4_count": 2, "required": 2},
    "custody": {"pass": true},
    "presumption_language": {"pass": true},
    "temporal_consistency": {"pass": true},
    "no_unresolved_contradictions": {"pass": false}
  },
  "falsification_attempted": true,
  "source_quality": {}
}"""
    prompt = f"""You are the Verification Agent for the Madlanga Commission.
SOUL: Adversarial checking / source-quality challenge.

DATA: {DATA_CONTEXT}
CHAIR: {json.dumps(chair)}
EVIDENCE: {json.dumps(evidence)}
CONTRADICTIONS: {json.dumps(contradiction)}

Return ONLY JSON:
{template}"""
    return run_hermes_profile('verification', prompt, timeout=180)

def run_redteam_profile(verification: Dict[str, Any], chair: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """Run red-team via madlanga-redteam profile"""
    template = """{{
  "challenges": [],
  "alternative_explanations": [],
  "breaks_conclusion": false
}}"""
    prompt = f"""You are the Red Team Agent for the Madlanga Commission.
SOUL: Attempts to falsify or weaken proposed conclusions.

DATA: {DATA_CONTEXT}
VERIFICATION: {json.dumps(verification)}
CHAIR: {json.dumps(chair)}

Return ONLY JSON:
{template}"""
    return run_hermes_profile('redteam', prompt, timeout=180)


# Test function
if __name__ == '__main__':
    # Quick test
    result = run_hermes_profile('evidence', 'Test prompt - respond with "OK"')
    print(json.dumps(result, indent=2))