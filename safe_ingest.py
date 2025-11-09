#!/usr/bin/env python3
# safe_ingest.py — Observatory safe ingest scaffold

import argparse, json, os, time, hashlib, datetime

OUT_AUDIT = "audit_log.json"
OUT_PROV_DIR = "provenance"

def sha256_of(path, chunk=1024*1024):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while (b := f.read(chunk)):
            h.update(b)
    return h.hexdigest()

def write_json_append(file, obj):
    data = []
    if os.path.exists(file):
        try: data = json.load(open(file))
        except: pass
    data.append(obj)
    json.dump(data, open(file, "w"), indent=2)

def emit_provenance_ttl(event_id, actor, src_path, sha, dest_stage):
    os.makedirs(OUT_PROV_DIR, exist_ok=True)
    now = datetime.datetime.utcnow().isoformat() + "Z"
    ttl = f"""@prefix : <http://nkllon/ontology/policy#> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

:provenance_{event_id} a prov:Entity ;
    prov:generatedAtTime "{now}"^^xsd:dateTime ;
    prov:wasAttributedTo "{actor}" ;
    prov:hadPrimarySource "{src_path}" ;
    :archivedIn "{dest_stage}" ;
    :sha256 "{sha}" .
"""
    open(f"{OUT_PROV_DIR}/provenance_{event_id}.ttl","w").write(ttl)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--actor", required=True)
    ap.add_argument("--policy", default="RestrictedProcessing-001")
    ap.add_argument("--stage", default="observatory.stage.sensitive_data")
    args = ap.parse_args()

    sha = sha256_of(args.file)
    event_id = f"evt-{int(time.time())}"
    audit_row = {
        "event_id": event_id,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "actor": args.actor,
        "action": "safe_ingest",
        "object": {"name": os.path.basename(args.file),
                   "size_bytes": os.path.getsize(args.file),
                   "source": os.path.abspath(args.file),
                   "sha256": sha},
        "destination": {"type": "snowflake_stage",
                        "identifier": args.stage},
        "policy": {"policy_id": args.policy,
                   "no_training": True,
                   "private_vm_only": True}
    }
    write_json_append(OUT_AUDIT, audit_row)
    emit_provenance_ttl(event_id, args.actor, args.file, sha, args.stage)
    print("[OK] Ingest complete; audit + TTL emitted.")

if __name__ == "__main__":
    main()
