#!/usr/bin/env python3
"""
Madlanga Commission Evidence Ingestion Pipeline
Uses Tinyfish to fetch hearing transcripts and stores them in the evidence database
"""

import json
import os
import sqlite3
import hashlib
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from pathlib import Path

# Import Tinyfish client
import sys
sys.path.append('/home/ubuntu/.hermes/skills/madlanga-commission-architecture')
from tinyfish_client import tinyfish_search, tinyfish_fetch, tinyfish_search_and_fetch, tinyfish_batch_fetch

# Paths
SKILLS_DIR = Path(__file__).parent
EXTRACTED_DIR = Path(os.path.dirname(os.path.dirname(SKILLS_DIR))) / 'cache' / 'documents' / 'madlanga-extracted' / 'madlanga-work'
DATA_DIR = EXTRACTED_DIR / 'data'
DB_PATH = DATA_DIR / 'evidence.db'
COMMISSION_JSON = DATA_DIR / 'commission.json'

def now() -> str:
    return datetime.now(timezone.utc).isoformat()

def get_db_connection():
    """Get a connection to the evidence database"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys=ON')
    return conn

def init_ingestion_tables():
    """Add tables for transcript and document ingestion"""
    conn = get_db_connection()
    try:
        conn.executescript('''
        CREATE TABLE IF NOT EXISTS transcripts(
            id TEXT PRIMARY KEY,
            hearing_day INTEGER NOT NULL,
            hearing_date TEXT,
            witness_names TEXT,  -- JSON array
            evidence_leader TEXT,
            url TEXT,
            full_text TEXT,
            text_hash TEXT NOT NULL,
            pages INTEGER,
            language TEXT DEFAULT 'en',
            status TEXT NOT NULL,  -- fetched, parsed, verified
            fetched_at TEXT NOT NULL,
            FOREIGN KEY(hearing_day) REFERENCES hearings(day)
        );
        
        CREATE TABLE IF NOT EXISTS documents(
            id TEXT PRIMARY KEY,
            doc_type TEXT NOT NULL,  -- affidavit, correspondence, bank_record, forensic_report, tender_doc, phone_extraction, policy_doc, transcript_excerpt
            title TEXT,
            related_hearing_day INTEGER,
            related_person_ids TEXT,  -- JSON array
            source_url TEXT,
            file_path TEXT,
            content_hash TEXT NOT NULL,
            pages INTEGER,
            chain_of_custody_verified INTEGER DEFAULT 0,
            ingested_at TEXT NOT NULL,
            metadata TEXT  -- JSON
        );
        
        CREATE TABLE IF NOT EXISTS exhibits(
            id TEXT PRIMARY KEY,
            hearing_day INTEGER NOT NULL,
            exhibit_number TEXT,
            document_id TEXT,
            presented_by TEXT,
            admitted INTEGER DEFAULT 0,
            objection_grounds TEXT,
            FOREIGN KEY(hearing_day) REFERENCES hearings(day),
            FOREIGN KEY(document_id) REFERENCES documents(id)
        );
        
        CREATE TABLE IF NOT EXISTS ingestion_log(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            at TEXT NOT NULL,
            action TEXT NOT NULL,  -- fetch, parse, store, verify
            object_type TEXT NOT NULL,  -- transcript, document, exhibit
            object_id TEXT NOT NULL,
            status TEXT NOT NULL,  -- success, failed, partial
            details TEXT
        );
        ''')
        conn.commit()
    finally:
        conn.close()

def log_ingestion(action: str, object_type: str, object_id: str, status: str, details: str = ""):
    """Log an ingestion action"""
    conn = get_db_connection()
    try:
        conn.execute(
            'INSERT INTO ingestion_log(at, action, object_type, object_id, status, details) VALUES(?,?,?,?,?,?)',
            (now(), action, object_type, object_id, status, details)
        )
        conn.commit()
    finally:
        conn.close()

def fetch_hearing_urls(limit_days: int = 178) -> List[Dict[str, Any]]:
    """Get all hearing URLs from the database and supplement with search"""
    conn = get_db_connection()
    try:
        cursor = conn.execute('SELECT day, date, url FROM hearings WHERE url IS NOT NULL ORDER BY day')
        rows = cursor.fetchall()
        return [{'day': r['day'], 'date': r['date'], 'url': r['url']} for r in rows]
    finally:
        conn.close()

def fetch_and_store_transcript(hearing_day: int, url: str) -> Dict[str, Any]:
    """Fetch a hearing page and store the transcript"""
    print(f"Fetching Day {hearing_day}: {url}")
    
    try:
        # Fetch the page content
        result = tinyfish_fetch([url])
        
        if 'results' not in result or not result['results']:
            log_ingestion('fetch', 'transcript', f'day-{hearing_day}', 'failed', 'No results from fetch')
            return {'status': 'failed', 'reason': 'No results'}
        
        fetch_result = result['results'][0]
        
        if 'error' in fetch_result:
            log_ingestion('fetch', 'transcript', f'day-{hearing_day}', 'failed', fetch_result['error'])
            return {'status': 'failed', 'reason': fetch_result['error']}
        
        # Extract content
        text = fetch_result.get('text', '')
        title = fetch_result.get('title', '')
        description = fetch_result.get('description', '')
        published_date = fetch_result.get('published_date', '')
        language = fetch_result.get('language', 'en')
        
        # Compute hash
        content_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
        
        # Store in database
        conn = get_db_connection()
        try:
            conn.execute('''
                INSERT OR REPLACE INTO transcripts 
                (id, hearing_day, hearing_date, url, full_text, text_hash, language, status, fetched_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                f'transcript.day{hearing_day}',
                hearing_day,
                published_date,
                url,
                text,
                content_hash,
                language,
                'fetched',
                now()
            ))
            conn.commit()
            
            log_ingestion('store', 'transcript', f'day-{hearing_day}', 'success', f'Stored {len(text)} chars, hash: {content_hash[:16]}')
            
            return {
                'status': 'success',
                'hearing_day': hearing_day,
                'title': title,
                'chars': len(text),
                'hash': content_hash,
                'url': url
            }
        finally:
            conn.close()
            
    except Exception as e:
        log_ingestion('fetch', 'transcript', f'day-{hearing_day}', 'failed', str(e))
        return {'status': 'failed', 'reason': str(e)}

def ingest_all_hearings(start_day: int = 1, end_day: int = 178) -> Dict[str, Any]:
    """Ingest all hearings in range"""
    urls = fetch_hearing_urls()
    results = {'success': [], 'failed': [], 'skipped': []}
    
    for hearing in urls:
        day = hearing['day']
        if day < start_day or day > end_day:
            continue
            
        url = hearing['url']
        if not url:
            results['skipped'].append({'day': day, 'reason': 'No URL'})
            continue
        
        result = fetch_and_store_transcript(day, url)
        if result['status'] == 'success':
            results['success'].append(result)
        else:
            results['failed'].append(result)
    
    return results

def search_and_ingest_witness_pages(witness_name: str) -> List[Dict[str, Any]]:
    """Search for and ingest witness-specific pages"""
    query = f"{witness_name} Madlanga Commission witness"
    search_results = tinyfish_search(query, page=1)
    
    urls = []
    if isinstance(search_results, dict):
        for r in search_results.get('results', [])[:5]:
            if isinstance(r, dict) and r.get('url'):
                urls.append(r['url'])
    
    if not urls:
        return []
    
    # Fetch all URLs
    fetch_results = tinyfish_batch_fetch(urls)
    stored = []
    
    # batch_fetch returns a list of individual result objects
    for result in fetch_results:
        if 'error' in result:
            continue
            
        url = result.get('url', '')
        text = result.get('text', '')
        title = result.get('title', '')
        if not text:
            continue
        content_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
        
        # Store as document
        conn = get_db_connection()
        try:
            doc_id = f"doc.witness.{witness_name.replace(' ', '_').lower()}.{content_hash[:16]}"
            conn.execute('''
                INSERT OR REPLACE INTO documents
                (id, doc_type, title, source_url, content_hash, pages, chain_of_custody_verified, ingested_at, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                doc_id,
                'witness_profile',
                title,
                url,
                content_hash,
                1,
                0,
                now(),
                json.dumps({'witness': witness_name, 'source': 'tinyfish'})
            ))
            conn.commit()
            stored.append({'id': doc_id, 'title': title, 'url': url})
        finally:
            conn.close()
    
    return stored

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Madlanga Commission Evidence Ingestion')
    parser.add_argument('--init', action='store_true', help='Initialize ingestion tables')
    parser.add_argument('--all', action='store_true', help='Ingest all hearings')
    parser.add_argument('--day', type=int, help='Ingest specific day')
    parser.add_argument('--witness', type=str, help='Ingest witness pages')
    parser.add_argument('--start', type=int, default=1, help='Start day')
    parser.add_argument('--end', type=int, default=178, help='End day')
    
    args = parser.parse_args()
    
    if args.init:
        init_ingestion_tables()
        print("Ingestion tables initialized")
    
    if args.all:
        print("Ingesting all hearings...")
        results = ingest_all_hearings(args.start, args.end)
        print(f"Success: {len(results['success'])}, Failed: {len(results['failed'])}, Skipped: {len(results['skipped'])}")
    
    if args.day:
        urls = fetch_hearing_urls()
        hearing = next((h for h in urls if h['day'] == args.day), None)
        if hearing:
            result = fetch_and_store_transcript(args.day, hearing['url'])
            print(json.dumps(result, indent=2))
        else:
            print(f"No hearing found for day {args.day}")
    
    if args.witness:
        print(f"Ingesting witness pages for: {args.witness}")
        stored = search_and_ingest_witness_pages(args.witness)
        print(f"Stored {len(stored)} documents")
        for doc in stored:
            print(f"  - {doc['title']}: {doc['url']}")