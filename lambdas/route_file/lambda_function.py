import json
import boto3
import os

s3 = boto3.client("s3")

def lambda_handler(event, context):
    print(f"[ROUTE] Routing transaction: {event.get('transaction_id')}")
    
    # El bucket se espera como variable de entorno o como parte del evento original
    # Usaremos una variable de entorno BUCKET_NAME que configuraremos en Terraform
    # o si no está, un placeholder.
    bucket = os.environ.get("BUCKET_NAME", event.get("bucket", "default-bucket"))
    tx_id = event.get("transaction_id", "unknown_tx")
    
    # Determinar prefijo destino basado en risk_level
    is_high_risk = event.get("risk_level") == "high"
    dest_prefix = "review/" if is_high_risk else "approved/"
    dest_key = f"{dest_prefix}{tx_id}.json"
    
    print(f"[ROUTE] Guardando transaccion en s3://{bucket}/{dest_key}")
    
    # Como la instrucción dice "move to s3://bucket/...", 
    # y en este escenario no recibimos un archivo, vamos a guardar el JSON completo
    # en la carpeta destino como si fuera el archivo procesado.
    s3.put_object(
        Bucket=bucket,
        Key=dest_key,
        Body=json.dumps(event),
        ContentType="application/json"
    )
    
    # Eliminamos la logica antigua de copy_object/delete_object porque el 
    # archivo de entrada original no existe en S3 para este escenario.
    # (El evento viene directamente en JSON)
    
    event["final_location"] = f"s3://{bucket}/{dest_key}"
    return event