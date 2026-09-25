# Agent / Tool Contracts + Orchestration — Evidence-First

## Tool Contracts (all agents must implement via JSON)

### retrieve(query)
- Input: { issue_id | claim_id | person_id | event_id | free_text }
- Output: { source_ids: [source_id: tier], doc_ids: [doc_id], claim_ids: [claim_id], question_ids: [q_id if gap] }
- Must return tier for each source

### get_person(person_id)
- Output: { id, full_name, rank, org, verified_bio: bool, bio_sources: [source_id], protection_status }

### get_hearing(hearing_id)
- Output: { id, date, day_number, witnesses: [person_id], transcript_id, status, rulings: [decision_id] }

### get_claim(claim_id)
- Output: { id, claimant, statement verbatim, date_claimed, subjects: [person_id], evidence_ids: [doc_id], status, sources: [source_id] }

### get_contradictions(claim_id)
- Output: [contradiction_id]

### check_gate(claim_id)
- Implements FINDING_GATE.md logic
- Output: { pass: bool, reasons: [string], required_sources: [type], contradictions: [contradiction_id], gaps: [question_id] }

### create_question(text, priority, related_claims)
- Output: question_id

## Orchestration Workflow

```
User question
  -> 1. classify: map to canonical IDs (people, issues, claims, events) via retrieve
  -> 2. evidence agent: retrieve + map provenance chain
  -> 3. chronology agent: order events, flag temporal conflicts
  -> 4. network agent: map relationships from Tier 1-4 only
  -> 5. contradiction agent: detect conflicts -> contradiction_id
  -> 6. docket agent: attach procedural state hearing_id/day
  -> 7. research agent: if question_id gap -> propose targeted retrieval
  -> 8. chair agent: frame decision / synthesis WITHOUT finding
  -> 9. verification agent: adversarial check source tier, custody, presumption, temporal
  -> 10. red-team agent: attempt falsify / alternative explanation
  -> 11. finding_gate: check_gate(claim_id)
        if PASS: publish FINDING with sources + limitations
        if FAIL: publish NO FINDING with gaps + contradictions + missing
  -> 12. Response: answer + provenance list + gaps + contradictions
```

Not: User question -> ask 6 bots -> average opinions. That is prohibited.

## Response Template

**Answer:** [synthesis from chair, citing source_ids]

**Provenance:**
- Sources used: [source_id tier]
- Claims: [claim_id status]
- Documents: [doc_id bundle]
- Exhibits: [exhibit_id]

**Contradictions:** [contradiction_id or none]

**Evidence Gaps:** [question_id or none]

**Gate:** PASS/FAIL — [reasons]

**Presumption:** All persons alleged are presumed innocent.

## No Old Souls

Old six soul.md files (chair_madlanga_bot.md etc) are deprecated. They were bot-first containing facts in prompt. New architecture: soul = behaviour + role + constraints. Facts = evidence store.

Migration: old files retained in /hermes_bots/deprecated/ for reference but not used.

## Implementation Order
1. Canonical model (done) -> 2. Constitution + Hierarchy + Protocol + Gate (done) -> 3. 9 souls (done) -> 4. Tool contracts + orchestration (this file) -> 5. Connect to actual evidence engine (vector DB + source registry)
