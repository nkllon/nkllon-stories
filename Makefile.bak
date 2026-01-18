setup:
	uv sync

ingest FILE?=README.md ACTOR?=you
ingest:
	uv run python safe_ingest.py --file $(FILE) --actor $(ACTOR)

snowpark:
	uv run python snowpark_audit_example.py

specs-sync:
	uvx cc-sdd sync

specs-coverage:
	uvx cc-sdd coverage --out .kiro/coverage.md

specs-map:
	uvx cc-sdd map --out .kiro/traceability/cicd-pipeline.mapping.md

specs-validate:
	uvx cc-sdd validate

publish REMOTE?=<REMOTE_URL>
publish:
	git init
	git add .
	git commit -m "feat: initial import (nkllon-stories spore)"
	git branch -M main
	git remote add origin $(REMOTE)
	git push -u origin main
