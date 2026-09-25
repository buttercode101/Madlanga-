#!/usr/bin/env python3
"""
Tinyfish API Client for Madlanga Commission
Used for search, fetch, and evidence ingestion
Uses the official Tinyfish SDK
"""

import os
import json
import requests
from typing import Dict, List, Any, Optional
from pathlib import Path

# Use the official SDK
try:
    from tinyfish import TinyFish
    HAS_TINYFISH_SDK = True
except ImportError:
    HAS_TINYFISH_SDK = False

class TinyfishClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or self._load_api_key()
        
        if HAS_TINYFISH_SDK:
            self.client = TinyFish(api_key=self.api_key)
        else:
            # Fallback to direct HTTP
            self.base_search_url = "https://api.search.tinyfish.ai/v1"
            self.base_fetch_url = "https://api.fetch.tinyfish.ai/v1"
            self.session = requests.Session()
            self.session.headers.update({
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            })
    
    def _load_api_key(self) -> str:
        key_path = Path("/home/ubuntu/.hermes/tinyfish/api_key.txt")
        if key_path.exists():
            return key_path.read_text().strip()
        raise ValueError("Tinyfish API key not found")
    
    def search(self, query: str, page: int = 1, **kwargs) -> Dict[str, Any]:
        """Search the web using Tinyfish"""
        if HAS_TINYFISH_SDK:
            # Use the SDK's search product - method is 'query'
            response = self.client.search.query(query=query, page=page, **kwargs)
            # Convert Pydantic model to dict if needed
            if hasattr(response, 'model_dump'):
                return response.model_dump()
            elif hasattr(response, 'dict'):
                return response.dict()
            return response
        else:
            payload = {"query": query, "page": page, **kwargs}
            response = requests.post(
                f"{self.base_search_url}/search",
                json=payload,
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
    
    def fetch(self, urls: List[str], **kwargs) -> Dict[str, Any]:
        """Fetch and extract content from URLs"""
        if HAS_TINYFISH_SDK:
            # Use the SDK's fetch product - method is 'get_contents', takes list of URLs
            response = self.client.fetch.get_contents(urls=urls, **kwargs)
            if hasattr(response, 'model_dump'):
                return response.model_dump()
            elif hasattr(response, 'dict'):
                return response.dict()
            return response
        else:
            payload = {"urls": urls, **kwargs}
            response = requests.post(
                f"{self.base_fetch_url}/fetch",
                json=payload,
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
    
    def batch_fetch(self, urls: List[str], **kwargs) -> List[Dict[str, Any]]:
        """Fetch multiple URLs in batch - returns list of results"""
        if HAS_TINYFISH_SDK:
            # The SDK's get_contents already handles batch
            response = self.fetch(urls, **kwargs)
            if isinstance(response, dict) and 'results' in response:
                return response['results']
            return [response] if response else []
        else:
            # Fallback: fetch one by one
            results = []
            for url in urls:
                try:
                    result = self.fetch([url], **kwargs)
                    results.append(result)
                except Exception as e:
                    results.append({"url": url, "error": str(e)})
            return results
    
    def search_and_fetch(self, query: str, limit: int = 5, **kwargs) -> List[Dict[str, Any]]:
        """Search and fetch top results"""
        search_results = self.search(query, page=1)
        # Extract URLs from search results
        urls = []
        if isinstance(search_results, dict):
            results = search_results.get('results', []) or search_results.get('data', []) or []
        else:
            results = []
        for r in results[:limit]:
            if isinstance(r, dict):
                url = r.get('url') or r.get('link')
                if url:
                    urls.append(url)
        if urls:
            return self.batch_fetch(urls, **kwargs)
        return []

# Global client instance
_tinyfish_client = None

def get_tinyfish_client() -> TinyfishClient:
    global _tinyfish_client
    if _tinyfish_client is None:
        _tinyfish_client = TinyfishClient()
    return _tinyfish_client

# Convenience functions for integration
def tinyfish_search(query: str, page: int = 1) -> Dict[str, Any]:
    """Search using Tinyfish"""
    return get_tinyfish_client().search(query, page)

def tinyfish_fetch(urls: List[str]) -> Dict[str, Any]:
    """Fetch URLs using Tinyfish"""
    return get_tinyfish_client().fetch(urls)

def tinyfish_batch_fetch(urls: List[str]) -> List[Dict[str, Any]]:
    """Fetch multiple URLs"""
    return get_tinyfish_client().batch_fetch(urls)

def tinyfish_search_and_fetch(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Search and fetch results"""
    return get_tinyfish_client().search_and_fetch(query, limit)

if __name__ == '__main__':
    # Test the client
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "Madlanga Commission South Africa"
    client = TinyfishClient()
    print(f"Searching for: {query}")
    results = client.search(query, page=1)
    print(json.dumps(results, indent=2))