import json
import re

def lambda_handler(event, context):
    print(f"[VALIDATE] Entrada: {json.dumps(event)}")
    
    # Validar amount > 0
    if "amount" not in event or type(event["amount"]) not in (int, float) or event["amount"] <= 0:
        raise ValueError("El campo 'amount' debe ser un número mayor a 0.")
        
    # Validar country con 2-letter ISO format
    if "country" not in event or not isinstance(event["country"], str) or len(event["country"]) != 2:
        raise ValueError("El campo 'country' debe tener un formato ISO de 2 letras.")
        
    # Validar account format (ej. "1234-5678")
    if "account" not in event or not isinstance(event["account"], str) or not re.match(r"^\d{4}-\d{4}$", event["account"]):
        raise ValueError("El campo 'account' debe tener el formato 'XXXX-XXXX'.")
        
    event["validation_passed"] = True
    return event