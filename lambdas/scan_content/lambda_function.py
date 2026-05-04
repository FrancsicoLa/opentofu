import json

def lambda_handler(event, context):
    print(f"[RISK ASSESS] Analizando transacción: {event.get('transaction_id')}")
    
    amount = event.get("amount", 0)
    country = event.get("country", "")
    
    # Compute risk_level
    if amount > 10000 or country != "MX":
        event["risk_level"] = "high"
        event["scan_reason"] = "High amount or foreign transaction"
    else:
        event["risk_level"] = "low"
        event["scan_reason"] = "Standard transaction"
        
    print(f"[RISK ASSESS] Resultado: risk_level={event['risk_level']}")
    return event