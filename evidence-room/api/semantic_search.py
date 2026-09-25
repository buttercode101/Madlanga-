#!/usr/bin/env python3
"""
Madlanga Commission - Semantic Search & Embeddings
Uses local embeddings for classification and retrieval
"""

import json
import os
import numpy as np
from typing import Dict, List, Any, Optional
from pathlib import Path

# Try to use sentence-transformers for embeddings
try:
    from sentence_transformers import SentenceTransformer
    EMBEDDING_MODEL = SentenceTransformer('all-MiniLM-L6-v2')
    HAS_EMBEDDINGS = True
except ImportError:
    EMBEDDING_MODEL = None
    HAS_EMBEDDINGS = False

# Paths
SKILLS_DIR = Path(__file__).parent
EXTRACTED_DIR = Path(os.path.dirname(os.path.dirname(os.path.dirname(SKILLS_DIR)))) / '.hermes' / 'cache' / 'documents' / 'madlanga-extracted' / 'madlanga-work'
DATA_DIR = EXTRACTED_DIR / 'data'
# Check for commission.json in local api directory first (for Vercel deployment)
LOCAL_COMMISSION = SKILLS_DIR / 'commission.json'
COMMISSION_JSON = LOCAL_COMMISSION if LOCAL_COMMISSION.exists() else DATA_DIR / 'commission.json'

# Cache for embeddings
EMBEDDINGS_CACHE_FILE = SKILLS_DIR / 'embeddings_cache.json'
EMBEDDINGS_NPY_FILE = SKILLS_DIR / 'embeddings_cache.npy'

class SemanticSearch:
    def __init__(self):
        self.data = None
        self.claim_texts = []
        self.claim_ids = []
        self.source_texts = []
        self.source_ids = []
        self.claim_embeddings = None
        self.source_embeddings = None
        self._load_data()
        self._build_embeddings()
    
    def _load_data(self):
        """Load commission data"""
        with open(COMMISSION_JSON, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        # Prepare claim texts for embedding
        for claim in self.data['claims']:
            self.claim_ids.append(claim['id'])
            # Combine statement and classification for richer embedding
            text = f"{claim['statement']} Classification: {claim['classification']}"
            self.claim_texts.append(text)
        
        # Prepare source texts for embedding
        for source in self.data['sources']:
            self.source_ids.append(source['id'])
            text = f"{source['title']} {source.get('publisher', '')} {source.get('tier', '')}"
            self.source_texts.append(text)
    
    def _build_embeddings(self):
        """Build or load embeddings"""
        if not HAS_EMBEDDINGS:
            print("[SemanticSearch] sentence-transformers not available, using fallback")
            return
        
        # Try to load cached embeddings
        if EMBEDDINGS_NPY_FILE.exists() and EMBEDDINGS_CACHE_FILE.exists():
            try:
                with open(EMBEDDINGS_CACHE_FILE, 'r') as f:
                    cache_info = json.load(f)
                if (cache_info.get('claim_count') == len(self.claim_texts) and 
                    cache_info.get('source_count') == len(self.source_texts)):
                    self.claim_embeddings = np.load(EMBEDDINGS_NPY_FILE)
                    self.source_embeddings = np.load(str(EMBEDDINGS_NPY_FILE).replace('claims', 'sources'))
                    print(f"[SemanticSearch] Loaded cached embeddings: {self.claim_embeddings.shape} claims, {self.source_embeddings.shape} sources")
                    return
            except Exception as e:
                print(f"[SemanticSearch] Failed to load cache: {e}")
        
        # Build new embeddings
        print("[SemanticSearch] Building embeddings...")
        self.claim_embeddings = EMBEDDING_MODEL.encode(self.claim_texts, show_progress_bar=False)
        self.source_embeddings = EMBEDDING_MODEL.encode(self.source_texts, show_progress_bar=False)
        
        # Save cache
        try:
            np.save(EMBEDDINGS_NPY_FILE, self.claim_embeddings)
            np.save(str(EMBEDDINGS_NPY_FILE).replace('claims', 'sources'), self.source_embeddings)
            with open(EMBEDDINGS_CACHE_FILE, 'w') as f:
                json.dump({
                    'claim_count': len(self.claim_texts),
                    'source_count': len(self.source_texts)
                }, f)
            print("[SemanticSearch] Embeddings cached")
        except Exception as e:
            print(f"[SemanticSearch] Failed to cache: {e}")
    
    def classify_query(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """Classify user query to canonical IDs using semantic similarity"""
        if not HAS_EMBEDDINGS or self.claim_embeddings is None:
            # Fallback to keyword matching
            return self._keyword_classify(query, top_k)
        
        query_embedding = EMBEDDING_MODEL.encode([query])
        
        # Find similar claims
        claim_sims = np.dot(query_embedding, self.claim_embeddings.T)[0]
        claim_top_indices = np.argsort(claim_sims)[::-1][:top_k]
        
        claim_ids = [self.claim_ids[i] for i in claim_top_indices]
        claim_scores = [float(claim_sims[i]) for i in claim_top_indices]
        
        # Find similar sources
        source_sims = np.dot(query_embedding, self.source_embeddings.T)[0]
        source_top_indices = np.argsort(source_sims)[::-1][:top_k]
        
        source_results = []
        for i in source_top_indices:
            source_id = self.source_ids[i]
            source = next(s for s in self.data['sources'] if s['id'] == source_id)
            source_results.append({
                'id': source_id,
                'tier': source['tier'],
                'score': float(source_sims[i])
            })
        
        return {
            'source_ids': source_results,
            'doc_ids': [],
            'claim_ids': claim_ids,
            'claim_scores': claim_scores,
            'question_ids': []
        }
    
    def _keyword_classify(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """Fallback keyword-based classification"""
        query_lower = query.lower()
        
        # Score claims by keyword overlap
        claim_scores = []
        for i, text in enumerate(self.claim_texts):
            score = sum(1 for word in query_lower.split() if word in text.lower())
            claim_scores.append((score, i))
        
        claim_scores.sort(reverse=True)
        claim_ids = [self.claim_ids[i] for score, i in claim_scores[:top_k] if score > 0]
        
        # Score sources
        source_results = []
        for i, source in enumerate(self.data['sources']):
            text = f"{source['title']} {source.get('publisher', '')}".lower()
            score = sum(1 for word in query_lower.split() if word in text)
            if score > 0:
                source_results.append({
                    'id': source['id'],
                    'tier': source['tier'],
                    'score': float(score)
                })
        
        source_results.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            'source_ids': source_results[:top_k],
            'doc_ids': [],
            'claim_ids': claim_ids,
            'claim_scores': [1.0] * len(claim_ids),
            'question_ids': []
        }
    
    def retrieve(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Main retrieve function using semantic search"""
        free_text = query.get('free_text', '').strip()
        claim_id = query.get('claim_id')
        person_id = query.get('person_id')
        issue_id = query.get('issue_id')
        event_id = query.get('event_id')
        
        # If specific claim_id requested, use that
        if claim_id:
            claim = next((c for c in self.data['claims'] if c['id'] == claim_id), None)
            if claim:
                source_results = []
                for sid in claim['sourceIds']:
                    source = next((s for s in self.data['sources'] if s['id'] == sid), None)
                    if source:
                        source_results.append({'id': sid, 'tier': source['tier']})
                return {
                    'source_ids': source_results,
                    'doc_ids': [],
                    'claim_ids': [claim_id],
                    'question_ids': []
                }
        
        # If person_id, find related claims
        if person_id:
            person = next((p for p in self.data['people'] if p['id'] == person_id), None)
            if person:
                claim_ids = []
                source_results = []
                for claim in self.data['claims']:
                    if person['name'] in claim['statement']:
                        claim_ids.append(claim['id'])
                        for sid in claim['sourceIds']:
                            source = next((s for s in self.data['sources'] if s['id'] == sid), None)
                            if source and not any(s['id'] == sid for s in source_results):
                                source_results.append({'id': sid, 'tier': source['tier']})
                return {
                    'source_ids': source_results,
                    'doc_ids': [],
                    'claim_ids': claim_ids,
                    'question_ids': []
                }
        
        # Use semantic search for free text
        if free_text:
            return self.classify_query(free_text)
        
        return {
            'source_ids': [],
            'doc_ids': [],
            'claim_ids': [],
            'question_ids': []
        }

# Global instance
semantic_search = SemanticSearch()

def retrieve(query: Dict[str, Any]) -> Dict[str, Any]:
    """Entry point for retrieve tool contract"""
    return semantic_search.retrieve(query)

if __name__ == '__main__':
    # Test
    import sys
    test_query = sys.argv[1] if len(sys.argv) > 1 else "Madlanga Commission established"
    result = retrieve({'free_text': test_query})
    print(json.dumps(result, indent=2))