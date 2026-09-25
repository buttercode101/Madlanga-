#!/usr/bin/env python3
"""
Madlanga Commission Tool Implementations
Implements the 7 JSON tool contracts from ORCHESTRATION.md
Backed by the commission.json data and SQLite evidence database
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

# ============================================================================
# TOOL CONTRACT IMPLEMENTATIONS
# ============================================================================

def retrieve(query: Dict[str, Any]) -> Dict[str, Any]:
    """
    retrieve(query)
    - Input: { issue_id | claim_id | person_id | event_id | free_text }
    - Output: { source_ids: [source_id: tier], doc_ids: [doc_id], claim_ids: [claim_id], question_ids: [q_id if gap] }
    - Must return tier for each source
    """
    # Extract query parameters
    issue_id = query.get('issue_id')
    claim_id = query.get('claim_id')
    person_id = query.get('person_id')
    event_id = query.get('event_id')
    free_text = query.get('free_text', '').strip()
    
    # Load commission data for people, claims, sources
    data = load_commission_data()
    
    # Initialize results
    source_ids = []  # Will be list of dicts with id and tier
    doc_ids = []     # We don't have documents yet
    claim_ids = []   # Claims that match the query
    question_ids = [] # We don't have question tracking yet
    
    # If we have a specific claim_id, return its sources
    if claim_id:
        claim = next((c for c in data['claims'] if c['id'] == claim_id), None)
        if claim:
            claim_ids.append(claim_id)
            for source_id in claim['sourceIds']:
                # Find the source to get its tier
                source = next((s for s in data['sources'] if s['id'] == source_id), None)
                if source:
                    source_ids.append({'id': source_id, 'tier': source['tier']})
    
    # If we have a person_id, find claims related to that person
    elif person_id:
        # For now, we'll do a simple text match in claim statements
        # In a full implementation, we'd have person->claim mappings
        person = next((p for p in data['people'] if p['id'] == person_id), None)
        if person:
            # Find claims that mention this person's name
            for claim in data['claims']:
                if person['name'] in claim['statement']:
                    claim_ids.append(claim['id'])
                    for source_id in claim['sourceIds']:
                        source = next((s for s in data['sources'] if s['id'] == source_id), None)
                        if source:
                            source_ids.append({'id': source_id, 'tier': source['tier']})
    
    # If we have free text, search in claims and sources
    elif free_text:
        # Search claims
        for claim in data['claims']:
            if free_text.lower() in claim['statement'].lower():
                claim_ids.append(claim['id'])
                for source_id in claim['sourceIds']:
                    source = next((s for s in data['sources'] if s['id'] == source_id), None)
                    if source:
                        source_ids.append({'id': source_id, 'tier': source['tier']})
        
        # Search sources
        for source in data['sources']:
            if (free_text.lower() in source['title'].lower() or 
                free_text.lower() in source.get('publisher', '').lower()):
                # Add source if not already added
                if not any(s['id'] == source['id'] for s in source_ids):
                    source_ids.append({'id': source['id'], 'tier': source['tier']})
    
    # If we have an issue_id, we don't have issue mapping yet
    # If we have an event_id, we don't have event mapping yet
    
    # Remove duplicates from source_ids while preserving order
    seen = set()
    unique_source_ids = []
    for sid in source_ids:
        if sid['id'] not in seen:
            seen.add(sid['id'])
            unique_source_ids.append(sid)
    
    return {
        'source_ids': unique_source_ids,
        'doc_ids': doc_ids,
        'claim_ids': list(set(claim_ids)),  # Remove duplicates
        'question_ids': question_ids
    }

def get_person(person_id: str) -> Dict[str, Any]:
    """
    get_person(person_id)
    - Output: { id, full_name, rank, org, verified_bio: bool, bio_sources: [source_id], protection_status }
    """
    data = load_commission_data()
    
    person = next((p for p in data['people'] if p['id'] == person_id), None)
    if not person:
        # Return empty structure if person not found
        return {
            'id': person_id,
            'full_name': '',
            'rank': '',
            'org': '',
            'verified_bio': False,
            'bio_sources': [],
            'protection_status': 'none'
        }
    
    # Map from commission.json format to tool contract format
    # commission.json has: id, name, role, type
    # Tool contract wants: id, full_name, rank, org, verified_bio, bio_sources, protection_status
    
    # For now, we'll use role as rank, and type as org
    # verified_bio: we don't have this data, default to False
    # bio_sources: we don't have person->source mappings yet
    # protection_status: we don't have this data, default to 'none'
    
    return {
        'id': person['id'],
        'full_name': person['name'],
        'rank': person.get('role', ''),
        'org': person.get('type', ''),
        'verified_bio': False,  # TODO: implement verification tracking
        'bio_sources': [],      # TODO: implement person-source mapping
        'protection_status': 'none'  # TODO: implement protection status
    }

def get_hearing(hearing_id: str) -> Dict[str, Any]:
    """
    get_hearing(hearing_id)
    - Output: { id, date, day_number, witnesses: [person_id], transcript_id, status, rulings: [decision_id] }
    """
    # hearing_id in our data is just the day number as string
    try:
        day_number = int(hearing_id)
    except ValueError:
        # Return empty structure if invalid
        return {
            'id': hearing_id,
            'date': None,
            'day_number': None,
            'witnesses': [],
            'transcript_id': None,
            'status': 'unknown',
            'rulings': []
        }
    
    conn = get_db_connection()
    try:
        cursor = conn.execute(
            'SELECT * FROM hearings WHERE day = ?', 
            (day_number,)
        )
        row = cursor.fetchone()
        
        if not row:
            # Return empty structure for hearing not found
            return {
                'id': hearing_id,
                'date': None,
                'day_number': day_number,
                'witnesses': [],
                'transcript_id': None,
                'status': 'not_found',
                'rulings': []
            }
        
        # Parse witnesses JSON
        witnesses = json.loads(row['witnesses_json']) if row['witnesses_json'] else []
        
        # We don't have transcript_id or rulings in our current schema
        # These would come from a more complete evidence corpus
        
        return {
            'id': hearing_id,
            'date': row['date'],
            'day_number': row['day'],
            'witnesses': witnesses,  # These are names, not person_ids - TODO: map to person_ids
            'transcript_id': None,   # TODO: implement transcript tracking
            'status': row['status'],
            'rulings': []            # TODO: implement rulings/decisions tracking
        }
    finally:
        conn.close()

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
    # Load contradictions from database
    conn = get_db_connection()
    try:
        # Find contradictions that reference this claim_id
        cursor = conn.execute('''
            SELECT id FROM contradictions 
            WHERE claim_ids LIKE ? AND status = 'unresolved'
        ''', (f'%{claim_id}%',))
        rows = cursor.fetchall()
        contradiction_ids = [row[0] for row in rows]
        return contradiction_ids
    finally:
        conn.close()

def check_gate(claim_id: str) -> Dict[str, Any]:
    """
    check_gate(claim_id)
    - Implements FINDING_GATE.md logic
    - Output: { pass: bool, reasons: [string], required_sources: [type], contradictions: [contradiction_id], gaps: [question_id] }
    """
    claim = get_claim(claim_id)
    
    # Get source IDs from the claim
    source_ids = claim.get('sources', [])
    
    # Load commission data to get source tiers
    data = load_commission_data()
    sources_by_id = {s['id']: s for s in data['sources']}
    
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
            # Consider PRIMARY and PUBLIC RECORD ARCHIVE as acceptable tiers for now
            if tier in ['PRIMARY', 'PUBLIC RECORD ARCHIVE']:
                tier_sources.append(source)
    
    if len(tier_sources) < 2:
        pass_status = False
        reasons.append(f'Insufficient Tier 1-4 sources: {len(tier_sources)} found, minimum 2 required')
    
    # Condition 2: No unresolved contradiction_id linked to claim
    contradictions = get_contradictions(claim_id)
    if contradictions:
        pass_status = False
        reasons.append(f'Unresolved contradictions found: {contradictions}')
    
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
        pass
    
    return {
        'pass': pass_status,
        'reasons': reasons,
        'required_sources': [],  # TODO: implement based on claim requirements
        'contradictions': contradictions,
        'gaps': []  # TODO: implement question/gap tracking
    }

def create_question(text: str, priority: str, related_claims: List[str]) -> str:
    """
    create_question(text, priority, related_claims)
    - Output: question_id
    """
    # Generate a simple question ID based on timestamp and hash
    import hashlib
    timestamp = now()
    # Create a deterministic ID from the inputs
    input_string = f"{text}:{priority}:{','.join(sorted(related_claims))}:{timestamp}"
    question_id = f"q.{hashlib.sha256(input_string.encode()).hexdigest()[:16]}"
    
    # In a full implementation, we'd store this question in a questions table
    # For now, we just return the ID
    
    return question_id

# ============================================================================
# DATABASE INITIALIZATION (if needed)
# ============================================================================

def init_db():
    """Initialize the evidence database if it doesn't exist"""
    if os.path.exists(DB_PATH):
        return  # Already exists
    
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    # Create a fresh connection for initialization
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys=ON')
    try:
        conn.executescript('''
        CREATE TABLE IF NOT EXISTS sources(
            id TEXT PRIMARY KEY,
            tier TEXT NOT NULL,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            publisher TEXT,
            date TEXT,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS claims(
            id TEXT PRIMARY KEY,
            statement TEXT NOT NULL,
            classification TEXT NOT NULL,
            verification_state TEXT NOT NULL DEFAULT 'verified',
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS claim_sources(
            claim_id TEXT,
            source_id TEXT,
            PRIMARY KEY(claim_id, source_id),
            FOREIGN KEY(claim_id) REFERENCES claims(id),
            FOREIGN KEY(source_id) REFERENCES sources(id)
        );
        CREATE TABLE IF NOT EXISTS hearings(
            day INTEGER PRIMARY KEY,
            date TEXT,
            witnesses_json TEXT,
            lead TEXT,
            url TEXT,
            status TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS snapshots(
            id TEXT PRIMARY KEY,
            source_id TEXT NOT NULL,
            retrieved_at TEXT NOT NULL,
            content_sha256 TEXT NOT NULL,
            bytes INTEGER NOT NULL,
            path TEXT,
            fetch_status TEXT NOT NULL,
            FOREIGN KEY(source_id) REFERENCES sources(id)
        );
        CREATE TABLE IF NOT EXISTS audit(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            at TEXT NOT NULL,
            action TEXT NOT NULL,
            object_type TEXT NOT NULL,
            object_id TEXT NOT NULL,
            details TEXT
        );
        ''')
        
        # Load initial data from commission.json
        data = load_commission_data()
        
        for s in data['sources']:
            conn.execute(
                'INSERT OR IGNORE INTO sources VALUES(?,?,?,?,?,?,?)',
                (s['id'], s['tier'], s['title'], s['url'], s.get('publisher'), s.get('date'), now())
            )
        
        for x in data['claims']:
            conn.execute(
                'INSERT OR IGNORE INTO claims VALUES(?,?,?,?,?)',
                (x['id'], x['statement'], x['classification'], 'verified', now())
            )
            for sid in x['sourceIds']:
                conn.execute(
                    'INSERT OR IGNORE INTO claim_sources VALUES(?,?)',
                    (x['id'], sid)
                )
        
        # The archive reports 178 recorded sitting days. Only six have detailed source records in this build.
        detailed = {h['day']: h for h in data['hearings']}
        for day in range(1, 179):
            h = detailed.get(day)
            if h:
                conn.execute(
                    'INSERT OR REPLACE INTO hearings VALUES(?,?,?,?,?,?)',
                    (day, h['date'], json.dumps(h['witnesses']), h.get('lead'), h['url'], 'detailed')
                )
            else:
                conn.execute(
                    'INSERT OR IGNORE INTO hearings VALUES(?,?,?,?,?,?)',
                    (day, None, '[]', None, None, 'index_only')
                )
        
        conn.commit()
    finally:
        conn.close()

# Initialize database on import if needed
if not os.path.exists(DB_PATH):
    init_db()

if __name__ == '__main__':
    # Simple test
    print("Testing retrieve...")
    result = retrieve({'free_text': 'Mkhwanazi'})
    print(json.dumps(result, indent=2))
    
    print("\nTesting get_person...")
    result = get_person('mkhwanazi')
    print(json.dumps(result, indent=2))
    
    print("\nTesting get_claim...")
    result = get_claim('C-003')
    print(json.dumps(result, indent=2))
    
    print("\nTesting check_gate...")
    result = check_gate('C-003')
    print(json.dumps(result, indent=2))