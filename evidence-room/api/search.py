import json
import sys
import os

# Add the api directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from madlanga_tools import retrieve, get_claim, get_contradictions, check_gate

def handler(request):
    """Vercel serverless function handler for /api/search"""
    try:
        # Parse request
        if request.method == 'GET':
            query = request.query.get('q', '')
        else:
            body = json.loads(request.body) if request.body else {}
            query = body.get('q', '') or body.get('query', '')
        
        if not query:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Missing query parameter "q"'})
            }
        
        # Run evidence retrieval (direct tools, no profiles for Vercel)
        result = retrieve({'free_text': query})
        
        # Format response
        response = {
            "query": query,
            "claims": result.get('claim_ids', []),
            "sources": result.get('source_ids', []),
            "documents": result.get('doc_ids', []),
            "gaps": result.get('question_ids', [])
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

# For local testing
if __name__ == '__main__':
    class MockRequest:
        def __init__(self, query):
            self.method = 'GET'
            self.query = {'q': query}
            self.body = None
    
    result = handler(MockRequest("established commission"))
    print(json.dumps(json.loads(result['body']), indent=2))