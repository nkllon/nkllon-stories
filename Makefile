setup:
	uv sync

ingest FILE?=README.md ACTOR?=you
ingest:
	uv run python tools/safe_ingest.py --file $(FILE) --actor $(ACTOR)

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

.PHONY: ingest audit-insert gen-manifest

INGEST_FILE ?= README.md
ACTOR ?= you@nkllon

ingest:
	uv run python tools/safe_ingest.py --file "" --actor ""

audit-insert:
	uv run python tools/snowpark_audit_example.py

gen-manifest:
	uv run python - << PY
import os, re, pathlib, datetime
p=pathlib.Path("stories"); out=pathlib.Path("spores"); out.mkdir(parents=True, exist_ok=True)
items=[]
for f in sorted(p.glob("*.md")):
    stem=f.stem.split("-",3); date="-".join(stem[:3]); title=(stem[3] if len(stem)>3 else f.stem).replace("-"," ").title()
    iri=re.sub(r[^a-z0-9],,title.lower())
    url=f"https://github.com/nkllon/nkllon-stories/blob/main/{f.as_posix()}"
    items.append((iri,title,date,url))
ttl=["""@prefix story: <http://nkllon.com/story#> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
"""]
for iri,title,date,url in items:
    ttl.append(f"""story:{iri} a story:Post ;
  story:title "{title}" ;
  story:created "{date}" ;
  foaf:page <{url}> ;
  prov:wasGeneratedBy story:Observatory .

""")
out.joinpath("story-manifest.ttl").write_text("".join(ttl), encoding="utf-8")
print("[OK] spores/story-manifest.ttl written:", len(items))
PY
