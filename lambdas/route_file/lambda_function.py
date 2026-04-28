import json
import boto3

s3 = boto3.client("s3")

def lambda_handler(event, context):
    bucket = event["bucket"]
    source_key = event["input_key"]
    
    dest_prefix = "quarantine/" if event.get("is_malicious") else "clean/"
    dest_key = f"{dest_prefix}{event['file_id']}.json"
    
    print(f"[ROUTE] s3://{bucket}/{source_key} -> s3://{bucket}/{dest_key}")
    
    s3.copy_object(
        Bucket=bucket,
        CopySource={"Bucket": bucket, "Key": source_key},
        Key=dest_key
    )
    s3.delete_object(Bucket=bucket, Key=source_key)
    
    event["final_location"] = f"s3://{bucket}/{dest_key}"
    return event