from snowflake.snowpark import Session
import os, json

def get_session():
    cfg = {
        "account": os.environ["SNOWFLAKE_ACCOUNT"],
        "user": os.environ["SNOWFLAKE_USER"],
        "password": os.environ["SNOWFLAKE_PASSWORD"],
        "warehouse": "OBS_SMALL_WH",
        "database": "OBSERVATORY",
        "schema": "AUDIT",
        "role": "OBSERVATORY_WRITER",
    }
    return Session.builder.configs(cfg).create()

def insert_audit_rows(s, path="audit_log.json"):
    rows = json.load(open(path))
    df = s.create_dataframe([(r["event_id"], r["timestamp"], r["actor"], r["action"],
        r["object"]["name"], r["object"]["size_bytes"], r["object"]["sha256"],
        r["object"]["source"], r["destination"]["type"], r["destination"]["identifier"],
        r["policy"]["policy_id"], r["policy"]["no_training"], r["policy"]["private_vm_only"]) 
        for r in rows],
        schema=["EVENT_ID","TS_UTC","ACTOR","ACTION","OBJ_NAME","OBJ_SIZE_BYTES",
                "OBJ_SHA256","OBJ_SOURCE_PATH","DEST_TYPE","DEST_IDENTIFIER",
                "POLICY_ID","NO_TRAINING","PRIVATE_VM_ONLY"])
    df.write.save_as_table("OBSERVATORY.AUDIT.AUDIT_LOG", mode="append")
    print("[OK] rows inserted:", len(rows))

if __name__ == "__main__":
    s = get_session(); insert_audit_rows(s); s.close()
