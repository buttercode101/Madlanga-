# Evidence data model

SQLite is the local runtime store; the logical model is portable to Postgres.

| Object | Purpose |
|---|---|
| source | canonical publisher, URL, tier and dates |
| snapshot | immutable SHA-256 capture of source bytes |
| claim | bounded statement + classification + verification state |
| claim_sources | many-to-many provenance |
| hearing | indexed sitting day; detailed or index-only |
| audit | append-only operational trail |

### Classifications

FACT, MANDATE, RECORD, TESTIMONY, ALLEGATION, ANALYSIS, INFERENCE.

Classification is not decoration: it prevents testimony or allegations from being rendered as established fact.

### Hearing integrity

The archive index is represented separately from detailed source-backed hearing records. An index-only day must never acquire invented witness, date or procedural detail.
