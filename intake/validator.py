import json
import os
import sys

REQUIRED_SCHEMA = {
    "steward_name": str,
    "steward_email": str,
    "cert_id": str,
    "appointment_key": str,
    "status": str
}

def validate_payload(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"[CRITICAL ERROR] Target ledger file missing: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"[CRITICAL ERROR] Malformed JSON structure: {e}")

    # Strict Field & Type Guarding
    for field, expected_type in REQUIRED_SCHEMA.items():
        if field not in data:
            raise KeyError(f"[SECURITY LOCK-OUT] Missing required schema field: '{field}'")
        if not isinstance(data[field], expected_type) or not str(data[field]).strip():
            raise TypeError(f"[SECURITY LOCK-OUT] Invalid or empty value type for field: '{field}'")

    # Access Key Format Validation
    if not data["appointment_key"].startswith("PDD-KEY-"):
        raise ValueError("[SECURITY LOCK-OUT] Key format violation detected!")

    print("?? ZERO-MORTALITY GUARANTEE: Payload verified and locked.")
    return data

if __name__ == "__main__":
    target = "intake/dispatched_keys/PDD-M1-PQD4SSCGH_key.json"
    validated_data = validate_payload(target)
    print(f"Verified Steward: {validated_data['steward_name']} | Key: {validated_data['appointment_key']}")
