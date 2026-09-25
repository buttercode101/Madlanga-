# Canonical Data Model — Madlanga Commission
# This is the shared operating environment. No bot may invent fields outside this model.
# Version: 1.0-evidence-first 2026-09-25

## 1. people
- id: string (e.g., person.mkhwanazi.nhlanhla)
- type: [commissioner, evidence_leader, witness, subject, official, businessperson, counsel, staff]
- full_name, rank_title, organization, role_at_commission
- dob, bio_verified: bool, bio_sources: [source_id]
- credibility_factors: [prior_testimony_count, convictions, disciplinary_history]
- protection_status: [none, offered_declined, granted]

## 2. hearings
- id: string (hearing.2025-09-17.day001)
- date, day_number: int (1-178+), location: Brigitte Mabandla Justice College
- chair_present: [person_id], commissioners_present: [person_id]
- evidence_leaders: [person_id]
- witnesses: [person_id]
- status: [scheduled, in_progress, postponed, completed, in_camera]
- rulings: [decision_id]
- transcript_pages: int, transcript_id: doc_id

## 3. transcripts
- id: transcript.2025-09-17.day001
- hearing_id, pages, date, language
- text_hash, redacted: bool, in_camera: bool
- source_id: primary source gazette/commission site

## 4. documents
- id: doc.bundle.001
- type: [affidavit, correspondence, bank_record, forensic_report, tender_doc, phone_extraction, policy_doc]
- pages, date_created, author: person_id
- bundle_number: 1-750, chain_of_custody_verified: bool
- source_id

## 5. exhibits
- id: exhibit.whatsapp.sibanyoni.001
- hearing_id, document_id, exhibit_number
- presented_by: person_id, objected_by: [person_id]
- admitted: bool, objection_grounds: string

## 6. claims
- id: claim.mkhwanazi.121dockets.removal.2025-03
- claimant: person_id, date_claimed: 2025-07-06
- statement: verbatim, source_id: transcript or briefing
- subjects: [person_id], entities: [org]
- evidence_required: [type], evidence_ids: [doc_id]
- status: [untested, corroborated, contradicted, withdrawn]
- presumption: all subjects presumed innocent until conviction

## 7. issues
- id: issue.infiltration.police
- terms_of_reference_clause: string
- description, related_claims: [claim_id], related_hearings: [hearing_id]

## 8. events
- id: event.2024-12.instruction.disband.pktt
- date, type: [instruction, removal, arrest, tender_award, meeting, briefing]
- actors: [person_id], documents: [doc_id], claims: [claim_id]
- temporal_conflicts: [contradiction_id]

## 9. relationships
- id: rel.mchunu.matlala.alleged
- from: person_id, to: person_id, type: [alleged_association, professional, reporting_line, business, legal_rep]
- strength: [alleged, documented, admitted], sources: [source_id], first_alleged: date

## 10. sources
- id: source.gazette.53048
- type: [gazette, commission_site, transcript, court_filing, parliamentary_report, media_verified, affidavit]
- url, date_published, publisher, hash
- reliability_tier: [1-primary-official, 2-commission-record, 3-sworn-testimony, 4-documentary-verified, 5-media-corroborated, 6-unverified]
- access: [public, restricted, in_camera]

## 11. contradictions
- id: contra.mkhwanazi.vs.sibiya.dockets
- claim_ids: [claim_id], source_ids: [source_id], hearing_ids: [hearing_id]
- type: [direct_conflict, temporal_impossible, documentary_vs_oral, recanted]
- status: [identified, under_review, resolved_favor_claimA, unresolved]
- detected_by: agent.contradiction

## 12. decisions (rulings)
- id: decision.2026-07-01.khan.incamera.refused
- hearing_id, date, chair: person.madlanga.mbuyiseli
- applicant: person_id, application_type: [in_camera, postponement, recusal]
- grounds, ruling: [granted, refused, reserved], reasoning, precedent: [decision_id]
- published_to_record: bool

## 13. questions (evidence gaps)
- id: q.2026-09-23.sindane.whatsapp.admissibility
- raised_by: agent_id, related_claims: [claim_id], related_decisions: [decision_id]
- question_text, priority: [critical, high, medium, low], status: [open, research_assigned, answered, blocked]
- required_sources: [type]

---
All agents must reference IDs. No free-text facts without source_id. If source missing, agent must return: "I don't have sufficient sourced evidence to answer that — evidence gap: [question_id]"
