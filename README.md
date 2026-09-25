# Madlanga Commission — Evidence Room

Evidence-first digital public-record workspace for the Judicial Commission of Inquiry into Alleged Criminality, Political Interference and Corruption in the Criminal Justice System.

**Live Evidence Room:** https://madlanga-commission-architecture.vercel.app

---

## Repository Structure

```
├── core/                    # Evidence-first engine (Python)
│   ├── madlanga_orchestrator_wired.py   # 12-step orchestrator with 7 Hermes agents
│   ├── madlanga_tools.py                # 7 JSON tool contracts
│   ├── semantic_search.py               # sentence-transformers embeddings
│   ├── tinyfish_client.py               # Tinyfish API client (free-tier)
│   ├── ingestion_pipeline.py            # Auto-ingests hearing days + witness docs
│   └── debug_gate.py                    # Gate debugging utility
│
├── evidence-room/           # React Evidence Room v2 (TypeScript/React)
│   ├── src/
│   │   ├── main.jsx         # Entry point
│   │   ├── App.jsx          # Main component with gate-checked UI
│   │   └── styles.css       # Paper texture, hazard stripes, marquee, stamps
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
│
├── viral/                   # Viral campaign assets
│   ├── finding_cards/       # Auto-generated finding cards (PNG)
│   ├── architecture_diagram.png
│   ├── 7_DAY_VIRAL_PLAN.md
│   ├── DEMO_VIDEO_SCRIPT.md
│   └── VALIDATION_REPORT.md
│
├── finding_cards/           # Finding card images (PNG)
│
├── api/                     # Python HTTP API (Vercel serverless)
│   ├── index.py             # Entry point
│   ├── server.py            # HTTP handlers
│   ├── ingest.py            # Ingestion endpoints
│   └── validate.py          # Validation utilities
│
├── data/                    # Canonical source data
│   └── commission.json      # 5 sources, 5 claims, 178 hearing days
│
├── hermes/                  # Governance layer
│   ├── CONSTITUTION.md      # Evidence Constitution (8 Articles)
│   ├── EVIDENCE_PROTOCOL.md
│   ├── FINDING_GATE.md      # 10-condition gate
│   ├── SOURCE_HIERARCHY.md  # Tier 1-6 definitions
│   ├── ORCHESTRATION.md     # 12-step workflow
│   ├── TOOL_CONTRACTS.md    # 7 JSON contracts
│   ├── runtime.py           # Hermes runtime
│   └── agents/              # 7 agent souls (chair, evidence, network, contradiction, verification, research, red-team)
│
├── docs/                    # Documentation
│   ├── ARCHITECTURE.md
│   ├── DATA_MODEL.md
│   └── OPERATIONS.md
│
├── agents/                  # Legacy agent contracts
│   └── HERMES_CONTRACT.md
│
├── tests/                   # Integrity tests
│   ├── test_integrity.py
│   └── test_hermes_runtime.py
│
├── app.py                   # Legacy Flask entry point
├── run.py                   # Legacy runner
└── requirements.txt         # Python deps
```

---

## Quick Start

### Evidence Room (React + Vite)
```bash
cd evidence-room
npm install
npm run dev          # http://localhost:3000
npm run build        # Outputs to dist/ for Vercel
```

### Core Engine (Python)
```bash
# Install deps
pip install sentence-transformers tinyfish

# Run orchestrator demo
cd core
python3 -c "
from madlanga_orchestrator_wired import madlanga_investigate
import json
print(json.dumps(madlanga_investigate('Mkhwanazi dockets'), indent=2))
"
```

### Ingest New Evidence
```bash
cd core
python3 ingestion_pipeline.py --all-hearings
python3 ingestion_pipeline.py --witnesses
```

---

## The Finding Gate (10 Conditions)

A finding **only passes** if ALL conditions met:

1. **≥2 Independent Tier 1-4 Sources** — At least one Tier 1/2, or two Tier 3/4 from different origins
2. **No Unresolved Contradictions** — Zero contradiction_ids linked to claim
3. **Chain of Custody Verified** — For documentary evidence
4. **Temporal Consistency** — Event dates are possible
5. **Relationships Not Just Alleged** — Documented/admitted only
6. **Presumption of Innocence Language** — "Alleged, if established, would indicate"
7. **Verification Agent Failed to Falsify** — Adversarial check passed
8. **Red Team Failed to Weaken** — Alternative explanations tested
9. **Evidence Gaps Listed** — question_ids closed or explicitly listed
10. **Sources Published** — source_ids with tier + access notes

**Output:** `FINDING: [claim_id] — [summary] — Sources: [ids] — Limitations: [gaps]`
**Or:** `NO FINDING: Insufficient evidence — Retrieved: [ids] — Missing: [required] — Contradictions: [ids] — Gaps: [ids]`

---

## Evidence Tiers (Source Hierarchy)

| Tier | Type | Examples |
|------|------|----------|
| **1** | Primary Official | Gazette 53048, Proclamations, Treasury allocations |
| **2** | Commission Record | criminaljusticecommission.org.za, rulings, spokesperson statements |
| **3** | Sworn Testimony | Transcripts, affidavits under oath |
| **4** | Documentary Verified | Bank records, forensic reports, admitted exhibits |
| **5** | Media Corroborated | SABC, Daily Maverick, News24 (supporting only) |
| **6** | Unverified | Social media, untested allegations |

---

## Free-Tier Stack

| Component | Tool | Cost |
|-----------|------|------|
| Search/Fetch | Tinyfish API | $0 (2 keys, $8 credits) |
| Embeddings | sentence-transformers (local) | $0 |
| Database | SQLite | $0 |
| Orchestration | Hermes Agents (local) | $0 |
| Hosting | Vercel (static) | $0 |
| CI/CD | GitHub Actions | $0 |

**Total: $0/month**

---

## Viral Campaign (7 Days)

See `viral/7_DAY_VIRAL_PLAN.md` for the full X (Twitter) execution plan:

- **Day 1:** Deploy Evidence Room + 60s demo video ("R147M vs $0")
- **Day 2:** Commission vs Tool comparison thread
- **Day 3:** "Ask the Evidence" UGC campaign
- **Day 4:** Expose 3 unresolved contradictions
- **Day 5:** Technical deep dive (architecture diagram)
- **Day 6:** Journalist/influencer outreach
- **Day 7:** Commission Starter Kit launch

Assets: `finding_cards/*.png`, `architecture_diagram.png`, `DEMO_VIDEO_SCRIPT.md`

---

## Validation Report

See `viral/VALIDATION_REPORT.md` for data-backed evaluation:
- Technical comparison vs actual Commission (R147M budget)
- Monetization analysis (per-commission model: R500K-R2M)
- Target market (SA commissions + 40+ global inquiries)
- Competitive landscape (CaseLines, Relativity, Opus 2)
- Risk mitigation

---

## Disclaimer

Independent evidence analysis tool. All persons named in claims are presumed innocent until convicted by a competent court. 
Findings require minimum 2 independent Tier 1-4 sources with no unresolved contradictions. 
This tool does not represent the official Madlanga Commission.

---

**Built by Loopii Business Services** · Evidence-first architecture · Zero hallucination · Free-tier stack