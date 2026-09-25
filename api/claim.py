import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from madlanga_tools import retrieve, get_claim, get_contradictions, check_gate

def handler(request):
    """Vercel serverless function handler for /api/claim/<claim_id>"""
    try:
        # Extract claim_id from path
        path = request.url.split('/api/claim/')[-1] if '/api/claim/' in request.url else ''
        claim_id = path.split('?')[0].split('/')[0] if path else ''
        
        if not claim_id:
            # Try query parameter
            if request.method == 'GET':
                claim_id = request.query.get('claim_id', '')
        
        if not claim_id:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Missing claim_id'})
            }
        
        # Get claim details
        claim = get_claim(claim_id)
        contradictions = get_contradictions(claim_id)
        gate = check_gate(claim_id)
        
        response = {
            "claim": claim,
            "contradictions": contradictions,
            "gate": gate
        }
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps(response)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }

if __name__ == '__main__':
    class MockRequest:
        def __init__(self, claim_id):
            self.method = 'GET'
            self.query = {'claim_id': claim_id}
            self.body = None
            self.url = f'/api/claim/{claim_id}'
    
    result = handler(MockRequest("C-001"))
    print(json.dumps(json.loads(result['body']), indent=2))