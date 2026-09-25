# Madlanga Commission — Evidence Room

Evidence-first digital public-record workspace for the Judicial Commission of Inquiry into Alleged Criminality, Political Interference and Corruption in the Criminal Justice System.

This repository is intentionally evidence-constrained. It does not manufacture findings, testimony, exhibits, dates, or guilt.

## Runtime
- Python standard library only.
- SQLite evidence store.
- JSON-backed seed data.
- HTTP API: /api/status, /api/sources, /api/claims, /api/hearings, /api/search, /api/gate.
- Hermes governance under /hermes/.
- All 178 sitting-day slots are represented; only source-backed detailed records are populated.

## Integrity rules
1. Primary legal/government sources outrank secondary reporting.
2. Every material claim has provenance.
3. FACT, MANDATE, RECORD, TESTIMONY, ALLEGATION, ANALYSIS and INFERENCE stay distinct.
4. Contradictions are preserved.
5. Missing evidence stays missing.
6. Hermes is a reasoning layer, never the source of truth.
7. No guilt-by-association inference.

## Run
```bash
python3 app.py
```
Then open http://localhost:4173/.

## Production path
The next major data task is ingestion of the actual transcript/document/exhibit corpus into immutable hashed snapshots, followed by full-text retrieval and an evidence graph.