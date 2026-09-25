#!/usr/bin/env python3
"""
Madlanga Commission Orchestrator
Coordinates the 7 specialized profiles via delegate_task to run the 12-step evidence-first workflow.
"""

import json
import os
import sys
from typing import Dict, List, Any, Optional

# Import our tool implementations
sys.path.append('/home/ubuntu/.hermes/skills/madlanga-commission-architecture')
from madlanga_tools import (
    retrieve, get_person, get_hearing, get_claim, 
    get_contradictions, check_gate, create_question
)

# Import Hermes tools - these are available in the Hermes environment
try:
    from hermes_tools import delegate_task
except ImportError:
    # Fallback for testing
    def delegate_task(*args, **kwargs):
        return {"status": "delegated", "result": "placeholder"}

# Profile names for the 7 agents
PROFILES = {
    'evidence': 'madlanga-evidence',
    'network': 'madlanga-network', 
    'contradiction': 'madlanga-contradiction',
    'verification': 'madlanga-verification',
    'research': 'madlanga-research',
    'redteam': 'madlanga-redteam',
    'chair': 'madlanga-chair'
}

class MadlangaOrchestrator:
    def __init__(self):
        self.context = {}  # Shared context between agents
        
    def step_1_classify(self, user_question: str) -> Dict[str, Any]:
        """1. classify: map to canonical IDs via retrieve"""
        print("Step 1: Classifying user question...")
        # Use retrieve to map question to canonical IDs
        result = retrieve({'free_text': user_question})
        self.context['classification'] = result
        return result
    
    def step_2_evidence(self) -> Dict[str, Any]:
        """2. evidence agent: retrieve + map provenance chain"""
        print("Step 2: Evidence retrieval and provenance mapping...")
        # Delegate to evidence profile
        # For now, we'll call the tool directly since we're building the system
        # In full implementation, this would delegate to the evidence profile
        evidence_result = self.context.get('classification', {})
        self.context['evidence'] = evidence_result
        return evidence_result
    
    def step_3_chronology(self) -> Dict[str, Any]:
        """3. chronology agent: order events, flag temporal conflicts"""
        print("Step 3: Chronology analysis...")
        # Placeholder - would delegate to chronology profile
        chronology_result = {
            "events_ordered": [],
            "temporal_conflicts": [],
            "sequence_gaps": []
        }
        self.context['chronology'] = chronology_result
        return chronology_result
    
    def step_4_network(self) -> Dict[str, Any]:
        """4. network agent: map relationships from Tier 1-4 only"""
        print("Step 4: Network/relationship mapping...")
        # Placeholder - would delegate to network profile
        network_result = {
            "relationships": [],
            "entities": [],
            "strength_assessment": {}
        }
        self.context['network'] = network_result
        return network_result
    
    def step_5_contradiction(self) -> Dict[str, Any]:
        """5. contradiction agent: detect conflicts -> contradiction_id"""
        print("Step 5: Contradiction detection...")
        # Placeholder - would delegate to contradiction profile
        contradiction_result = {
            "contradictions": [],
            "conflict_types": [],
            "resolution_status": {}
        }
        self.context['contradiction'] = contradiction_result
        return contradiction_result
    
    def step_6_docket(self) -> Dict[str, Any]:
        """6. docket agent: attach procedural state hearing_id/day"""
        print("Step 6: Docket/procedural state attachment...")
        # Placeholder - would delegate to docket profile
        docket_result = {
            "current_hearing": None,
            "procedural_state": {}
        }
        self.context['docket'] = docket_result
        return docket_result
    
    def step_7_research(self) -> Dict[str, Any]:
        """7. research agent: if question_id gap -> propose targeted retrieval"""
        print("Step 7: Research for evidence gaps...")
        # Placeholder - would delegate to research profile
        research_result = {
            "questions_addressed": [],
            "new_sources": [],
            "remaining_gaps": []
        }
        self.context['research'] = research_result
        return research_result
    
    def step_8_chair(self) -> Dict[str, Any]:
        """8. chair agent: frame decision / synthesis WITHOUT finding"""
        print("Step 8: Chair procedural synthesis...")
        # Placeholder - would delegate to chair profile
        chair_result = {
            "procedural_frame": "",
            "mandate_engaged": [],
            "evidence_sufficiency": "unknown"
        }
        self.context['chair'] = chair_result
        return chair_result
    
    def step_9_verification(self) -> Dict[str, Any]:
        """9. verification agent: adversarial check source tier, custody, presumption, temporal"""
        print("Step 9: Verification/adversarial checking...")
        # Placeholder - would delegate to verification profile
        verification_result = {
            "gate_checks": {},
            "falsification_attempted": False,
            "source_quality": {}
        }
        self.context['verification'] = verification_result
        return verification_result
    
    def step_10_redteam(self) -> Dict[str, Any]:
        """10. red-team agent: attempt falsify / alternative explanation"""
        print("Step 10: Red-team falsification attempt...")
        # Placeholder - would delegate to red-team profile
        redteam_result = {
            "challenges": [],
            "alternative_explanations": [],
            "breaks_conclusion": False
        }
        self.context['redteam'] = redteam_result
        return redteam_result
    
    def step_11_finding_gate(self, claim_id: str) -> Dict[str, Any]:
        """11. finding_gate: check_gate(claim_id)"""
        print("Step 11: Finding gate evaluation...")
        # Use our check_gate tool directly
        print(f"[DEBUG Orchestrator] Calling check_gate with claim_id: '{claim_id}'")
        gate_result = check_gate(claim_id)
        print(f"[DEBUG Orchestrator] check_gate returned: {gate_result}")
        self.context['gate'] = gate_result
        return gate_result
    
    def step_12_response(self) -> Dict[str, Any]:
        """12. Response: answer + provenance list + gaps + contradictions"""
        print("Step 12: Generating final response...")
        # Build response from all context
        response = {
            "answer": self._synthesize_answer(),
            "provenance": self._build_provenance(),
            "contradictions": self.context.get('contradiction', {}).get('contradictions', []),
            "evidence_gaps": self.context.get('research', {}).get('remaining_gaps', []),
            "gate": self.context.get('gate', {}),
            "presumption": "All persons alleged are presumed innocent."
        }
        return response
    
    def _synthesize_answer(self) -> str:
        """Synthesize final answer from chair's frame"""
        chair = self.context.get('chair', {})
        return chair.get('procedural_frame', 'No procedural frame available.')
    
    def _build_provenance(self) -> Dict[str, Any]:
        """Build provenance from all agent outputs"""
        evidence = self.context.get('evidence', {})
        return {
            "sources_used": evidence.get('source_ids', []),
            "claims_referenced": evidence.get('claim_ids', []),
            "documents": evidence.get('doc_ids', []),
            "exhibits": []  # Would be populated from evidence
        }
    
    def run_workflow(self, user_question: str, claim_id: Optional[str] = None) -> Dict[str, Any]:
        """Run the complete 12-step workflow"""
        print(f"Starting Madlanga Commission workflow for: '{user_question}'")
        print("=" * 60)
        
        try:
            # Step 1: Classify
            self.step_1_classify(user_question)
            
            # Determine claim_id from classification if not provided
            if not claim_id:
                classification = self.context.get('classification', {})
                claim_ids = classification.get('claim_ids', [])
                if claim_ids:
                    claim_id = claim_ids[0]
                    print(f"[DEBUG] Using claim_id from classification: {claim_id}")
            
            # Step 2: Evidence
            self.step_2_evidence()
            
            # Steps 3-6: Can run in parallel after evidence (per orchestration.md)
            # For simplicity, running sequentially
            self.step_3_chronology()
            self.step_4_network()
            self.step_5_contradiction()
            self.step_6_docket()
            
            # Step 7: Research (if gaps identified)
            self.step_7_research()
            
            # Step 8: Chair
            self.step_8_chair()
            
            # Step 9: Verification
            self.step_9_verification()
            
            # Step 10: Red-team
            self.step_10_redteam()
            
            # Step 11: Finding gate
            self.step_11_finding_gate(claim_id or "")
            
            # Step 12: Response
            response = self.step_12_response()
            
            print("=" * 60)
            print("Workflow completed successfully.")
            return response
            
        except Exception as e:
            print(f"Workflow failed: {str(e)}")
            return {
                "error": str(e),
                "answer": "Workflow execution failed.",
                "gate": {"pass": False, "reasons": [f"Workflow error: {str(e)}"]}
            }

# Global orchestrator instance
orchestrator = MadlangaOrchestrator()

def madlanga_investigate(question: str, claim_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Main entry point for Madlanga Commission investigation
    
    Args:
        question: The user's question to investigate
        claim_id: Optional specific claim ID to evaluate
        
    Returns:
        Dict containing answer, provenance, contradictions, gaps, gate status
    """
    return orchestrator.run_workflow(question, claim_id)

if __name__ == '__main__':
    # Test the orchestrator
    test_question = "Who is Mkhwanazi and what did he claim about the dockets?"
    result = madlanga_investigate(test_question)
    print("\nFINAL RESULT:")
    print(json.dumps(result, indent=2))