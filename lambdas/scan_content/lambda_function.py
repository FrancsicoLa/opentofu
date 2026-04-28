import json
import base64

EICAR_SIGNATURE = b"X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"

def lambda_handler(event, context):
    print(f"[SCAN] Escaneando file_id={event.get('file_id')}")
    try:
        contenido_bytes = base64.b64decode(event["content_base64"])
    except Exception as e:
        raise ValueError(f"content_base64 invalido: {e}")
    
    if EICAR_SIGNATURE in contenido_bytes:
        event["is_malicious"] = True
        event["scan_reason"] = "EICAR signature detected"
    else:
        event["is_malicious"] = False
        event["scan_reason"] = "clean"
    
    print(f"[SCAN] Resultado: is_malicious={event['is_malicious']}")
    return event