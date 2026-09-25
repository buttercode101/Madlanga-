# Orchestration

1. Classify the request.
2. Evidence Agent retrieves the relevant source set.
3. Specialist agents analyze in parallel.
4. Contradiction Agent tests incompatibilities.
5. Red Team attempts falsification and overclaim detection.
6. Verification Agent applies the gate.
7. Synthesis returns only evidence-supported material.

Response contract:
```json
{"answer":"","claims":[],"conflicts":[],"evidence_gaps":[],"questions_for_human":[],"gate":{"status":"pass|conditional|blocked","reasons":[]}}
```