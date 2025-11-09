# Nkllon Stories — Tales from the Lab

This repo is an executable spore that bundles:
- Safe ingest scaffold (audit + provenance TTL)
- Snowflake schema and Snowpark insert example
- Gmail MCP mailbox skeleton
- Lab stories content

## Prereqs
- Python 3.11+
- uv (https://astral.sh/uv/) — install: `curl -LsSf https://astral.sh/uv/install.sh | sh`

## Quickstart
```bash
uv sync
make ingest FILE=README.md ACTOR="Your Name"
```
Outputs:
- `audit_log.json`
- `provenance/provenance_<evt>.ttl`

## Snowflake (optional)
Set env vars:
- `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`, `SNOWFLAKE_PASSWORD`
Then:
```bash
uv run python snowpark_audit_example.py
```

## cc-sdd (Spec-Driven Development)
Without global install:
```bash
uvx cc-sdd --help
make specs-sync
make specs-coverage
make specs-map
make specs-validate
```
Artifacts land under `.kiro/`.

## Publish
```bash
make publish REMOTE=https://github.com/niklon/nkllon-stories.git
```

## Files
- `safe_ingest.py`, `snowflake_ddl.sql`, `snowpark_audit_example.py`, `gmail_mcp.py`
- `content/stories/*.md`
- `.kiro/specs/` placeholders
