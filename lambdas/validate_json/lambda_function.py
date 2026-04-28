import json

REQUIRED_FIELDS = ["file_id", "filename", "bucket", "input_key", "content_base64"]

def lambda_handler(event, context):
    print(f"[VALIDATE] Entrada: {json.dumps(event)}")
    missing = [f for f in REQUIRED_FIELDS if f not in event or event[f] in (None, "")]
    if missing:
        raise ValueError(f"Campos faltantes: {missing}")
    event["validation_passed"] = True
    return event