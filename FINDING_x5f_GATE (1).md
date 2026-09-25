# FINDING GATE

A finding may only be published if ALL conditions met:

1. Minimum 2 independent Tier 1-4 sources
   - At least one Tier 1 or Tier 2, or two Tier 3/4 from different origins

2. No unresolved contradiction_id linked to claim

3. Chain of custody verified for documentary evidence (if applicable)

4. Temporal consistency checked by chronology agent — event dates possible

5. Relationship mapping does not rely solely on alleged strength

6. Presumption of innocence language preserved: "alleged, if established, would indicate"

7. Verification agent has attempted falsification and failed

8. Red Team has attempted to weaken conclusion and finding survived or was amended

9. Evidence gap question_ids closed or explicitly listed as limitation

10. Sources published: list source_ids with tier, access note if restricted

## Gate Output
If pass:
FINDING: [claim_id] — [summary] — Sources: [source_ids] — Limitations: [question_ids]

If fail:
NO FINDING: Insufficient evidence — Retrieved: [source_ids] — Missing: [required] — Contradictions: [contradiction_ids] — Gaps: [question_ids]

No agent may bypass gate. Chair may frame decision but may not declare finding alone.

## Example
Claim: 121 dockets removed March 2025
Sources: transcript.2025-09-17.mkhwanazi + doc.transfer.letter.sibiya + source.commission.return.confirmation 2025-09
Tier: 3 + 4 + 2 = PASS (pending contradiction check vs Sibiya testimony)
