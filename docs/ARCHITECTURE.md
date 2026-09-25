# Production architecture

The Commission is built as an evidence system first and an AI system second.

Browser UI -> HTTP API -> evidence store -> immutable source snapshots -> retrieval/index -> Hermes orchestration.

## Evidence objects

- source: publisher, canonical URL, tier, publication/retrieval metadata
- snapshot: immutable byte capture identified by SHA-256
- claim: bounded statement with explicit classification and verification state
- hearing: procedural index with a strict distinction between index-only and source-backed detail
- audit: append-only operational record

## Hermes boundary

Hermes can retrieve, compare, classify, challenge and explain evidence. It cannot silently promote allegations to facts, invent missing records, or issue an official finding.

## Production invariant

Derived claims must point to source IDs and, when available, exact transcript/document locations. Source snapshots are append-only so later web changes cannot silently rewrite historical evidence.
