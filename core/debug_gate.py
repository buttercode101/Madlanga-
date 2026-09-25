#!/usr/bin/env python3
"""
Debug version of check_gate
"""

import json
import os
import sqlite3
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

# Paths - corrected to point to extracted data
SKILLS_DIR = os.path.dirname(os.path.abspath(__file__))
EXTRACTED_DIR = os.path.join(os.path.dirname(os.path.dirname(SKILLS_DIR)), 'cache', 'documents', 'madlanga-extracted', 'madlanga-work')
DATA_DIR = os.path.join(EXTRACTED_DIR, 'data')
COMMISSION_JSON = os.path.join(DATA_DIR, 'commission.json')
DB_PATH = os.path.join(DATA_DIR, 'evidence.db')

def now() -> str:
    return datetime.now(timezone.utc).isoformat()

def get_db_connection():
    """Get a connection to the evidence database"""
    if not os.path.exists(DB_PATH):
        # Initialize database if it doesn't exist
        init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys=ON')
    return conn

def load_commission_data() -> Dict[str, Any]:
    """Load the master commission.json file"""
    with open(COMMISSION_JSON, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_claim(claim_id: str) -> Dict[str, Any]:
    """
    get_claim(claim_id)
    - Output: { id, claimant, statement verbatim, date_claimed, subjects: [person_id], evidence_ids: [doc_id], status, sources: [source_id] }
    """
    data = load_commission_data()
    
    claim = next((c for c in data['claims'] if c['id'] == claim_id), None)
    if not claim:
        # Return empty structure if claim not found
        return {
            'id': claim_id,
            'claimant': '',
            'statement': '',
            'date_claimed': None,
            'subjects': [],
            'evidence_ids': [],
            'status': 'unknown',
            'sources': []
        }
    
    # We don't have claimant, date_claimed, subjects, evidence_ids in our current data
    # These would come from a more detailed claim structure
    
    # Get sources with their IDs
    sources = []
    for source_id in claim['sourceIds']:
        source = next((s for s in data['sources'] if s['id'] == source_id), None)
        if source:
            sources.append(source_id)  # Just the ID for now, but could be more detailed
    
    return {
        'id': claim['id'],
        'claimant': '',  # TODO: implement claimant tracking
        'statement': claim['statement'],
        'date_claimed': None,  # TODO: implement date tracking
        'subjects': [],        # TODO: implement subject mapping (who the claim is about)
        'evidence_ids': [],    # TODO: implement evidence/documents tracking
        'status': claim.get('classification', 'unknown'),  # Using classification as status for now
        'sources': sources
    }

def get_contradictions(claim_id: str) -> List[str]:
    """
    get_contradictions(claim_id)
    - Output: [contradiction_id]
    """
    # We don't have contradiction tracking in our current data
    # This would be implemented when we have a contradictions table/entity
    return []

def check_gate_debug(claim_id: str) -> Dict[str, Any]:
    """
    check_gate(claim_id) with debug output
    - Implements FINDING_GATE.md logic
    - Output: { pass: bool, reasons: [string], required_sources: [type], contradictions: [contradiction_id], gaps: [question_id] }
    """
    print(f"[DEBUG] Checking gate for claim_id: {claim_id}")
    claim = get_claim(claim_id)
    print(f"[DEBUG] Claim: {claim}")
    
    # Get source IDs from the claim
    source_ids = claim.get('sources', [])
    print(f"[DEBUG] Source IDs from claim: {source_ids}")
    
    # Load commission data to get source tiers
    data = load_commission_data()
    sources_by_id = {s['id']: s for s in data['sources']}
    print(f"[DEBUG] Sources by ID: {list(sources_by_id.keys())}")
    
    # Check gate conditions
    reasons = []
    pass_status = True
    
    # Condition 1: Minimum 2 independent Tier 1-4 sources
    # For now, we consider all our sources as Tier 1 (PRIMARY) or PUBLIC RECORD ARCHIVE
    tier_sources = []
    for source_id in source_ids:
        source = sources_by_id.get(source_id)
        if source:
            tier = source.get('tier', '')
            print(f"[DEBUG] Source {source_id}: tier = '{tier}'")
            # Consider PRIMARY and PUBLIC RECORD ARCHIVE as acceptable tiers for now
            if tier in ['PRIMARY', 'PUBLIC RECORD ARCHIVE']:
                tier_sources.append(source)
                print(f"[DEBUG]  -> Added to tier_sources (now {len(tier_sources)} sources)")
            else:
                print(f"[DEBUG]  -> Skipped (not in acceptable tiers)")
        else:
            print(f"[DEBUG] Source {source_id}: not found in sources_by_id")
    
    print(f"[DEBUG] Final tier_sources count: {len(tier_sources)}")
    for s in tier_sources:
        print(f"[DEBUG]  - {s['id']}: {s['tier']}")
    
    if len(tier_sources) < 2:
        pass_status = False
        reasons.append(f'Insufficient Tier 1-4 sources: {len(tier_sources)} found, minimum 2 required')
        print(f"[DEBUG] FAIL: {reasons[-1]}")
    else:
        print(f"[DEBUG] PASS: Sufficient tier sources ({len(tier_sources)})")
    
    # Condition 2: No unresolved contradiction_id linked to claim
    contradictions = get_contradictions(claim_id)
    print(f"[DEBUG] Contradictions: {contradictions}")
    if contradictions:
        pass_status = False
        reasons.append(f'Unresolved contradictions found: {contradictions}')
        print(f"[DEBUG] FAIL: {reasons[-1]}")
    
    # Condition 3-10: We'll implement simplified versions for now
    # In a full implementation, these would check:
    # 3. Chain of custody verified for documentary evidence
    # 4. Temporal consistency checked by chronology agent
    # 5. Relationship mapping does not rely solely on alleged strength
    # 6. Presumption of innocence language preserved
    # 7. Verification agent has attempted falsification and failed
    # 8. Red Team has attempted to weaken conclusion and finding survived
    # 9. Evidence gap question_ids closed or explicitly listed as limitation
    # 10. Sources published: list source_ids with tier, access note if restricted
    
    # For now, we'll just note that these need implementation
    if pass_status and len(tier_sources) >= 2:
        # Basic pass - but note that full gate checking needs implementation
        print(f"[DEBUG] PASS: Basic gate conditions met")
        pass
    
    result = {
        'pass': pass_status,
        'reasons': reasons,
        'required_sources': [],  # TODO: implement based on claim requirements
        'contradictions': contradictions,
        'gaps': []  # TODO: implement question/gap tracking
    }
    print(f"[DEBUG] Final result: {result}")
    return result

if __name__ == '__main__':
    # Test the debug version
    print("Testing check_gate_debug for C-002:")
    result = check_gate_debug('C-002')
    print("\nFinal result:")
    print(json.dumps(result, indent=2))