import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from madlanga_tools import retrieve, get_claim, get_contradictions, check_gate
import sqlite3

# Use local database file (copied to api/ for Vercel)
SKILLS_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_DB = os.path.join(SKILLS_DIR, 'evidence.db')
DB_PATH = LOCAL_DB if os.path.exists(LOCAL_DB) else '/home/ubuntu/.hermes/cache/documents/madlanga-extracted/madlanga-work/data/evidence.db'

def get_contradiction_details(contra_id: str):
    """Get full contradiction details from database"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.execute('SELECT * FROM contradictions WHERE id = ?', (contra_id,))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None
    finally:
        conn.close()

def handler(request):
    """Vercel serverless function handler for /api/contradictions"""
    try:
        # Check if specific contradiction requested
        contra_id = None
        if '/api/contradictions/' in request.url:
            path = request.url.split('/api/contradictions/')[-1]
            contra_id = path.split('?')[0].split('/')[0]
        
        if contra_id:
            # Return specific contradiction
            detail = get_contradiction_details(contra_id)
            if not detail:
                return {
                    'statusCode': 404,
                    'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                    'body': json.dumps({'error': f'Contradiction {contra_id} not found'})
                }
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'body': json.dumps(detail)
            }
        
        # Return all contradictions
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        try:
            cursor = conn.execute('SELECT * FROM contradictions')
            rows = cursor.fetchall()
            contradictions = [dict(row) for row in rows]
        finally:
            conn.close()
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({"contradictions": contradictions})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }

if __name__ == '__main__':
    class MockRequest:
        def __init__(self, url):
            self.method = 'GET'
            self.query = {}
            self.body = None
            self.url = url
    
    result = handler(MockRequest('/api/contradictions'))
    print(json.dumps(json.loads(result['body']), indent=2))