# Operations

## Local

python3 run.py

The service initializes SQLite under data/evidence.db and serves the public interface.

## Validate

python3 api/validate.py
python3 -m pytest -q

## Ingestion

python3 api/ingest.py <source_id>

Ingestion fetches the registered URL, hashes the exact bytes with SHA-256, stores an immutable snapshot and records an audit event.

## Safety

- Never overwrite an existing snapshot.
- Never edit a source URL to make an old record appear current.
- Never delete conflicting evidence to simplify an answer.
- Keep source-backed records separate from index-only records.
- Review external-source changes before treating them as authoritative.
