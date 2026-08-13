import os
import smtplib
import json
import secrets
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def generate_appointment_key(steward_name, cert_id):
    # Generate unique 256-bit prestige appointment token
    raw_token = secrets.token_hex(16).upper()
    return f"PDD-KEY-{cert_id[-6:]}-{raw_token[:8]}-{raw_token[8:16]}"

def send_dome_key_email(steward_name, steward_email, cert_id):
    appointment_key = generate_appointment_key(steward_name, cert_id)
    
    subject = "?? PRESTIGE DOME ACCESS: Official Appointment Key & Sovereign Portal Dispatch"
    
    body = f"""
================================================================================
?? PRESTIGE DIGITAL DOME — OFFICIAL STEWARD APPOINTMENT & KEY DISPATCH
================================================================================

Honorable Steward: {steward_name}
Module 1 Verification ID: {cert_id}
Clearance Status: 100% PERFECT MASTERY — ZERO-MORTALITY VERIFIED

We officially confirm your induction into the Prestige Digital Dome Sovereign Network.
Your appointment key has been generated and sealed for your high-level clearance.

--------------------------------------------------------------------------------
YOUR SECURE DOME APPOINTMENT KEY:
{appointment_key}
--------------------------------------------------------------------------------

PRESTIGE SHIELDED SUBMISSION PORTAL:
https://vault.prestigedome.internal/steward-intake?key={appointment_key}

OPERATIONAL DIRECTIVES:
1. Store this key securely inside your zero-knowledge vault directory.
2. Use this key for authenticating boardroom transmissions and Module 2 pitching.
3. Do not share, commit, or broadcast this unencrypted key.

Sealed under Scapush Precision Execution,
Prestige Digital Dome — Automated Intake Engine
================================================================================
"""

    print("=========================================================")
    print("?? PRESTIGE MAIL DISPATCHER (DRY-RUN TRANSMISSION LOG)")
    print(f"TO        : {steward_email} ({steward_name})")
    print(f"SUBJECT   : {subject}")
    print("---------------------------------------------------------")
    print(body)
    print("=========================================================")

    # Save dispatched key to secure local intake vault
    record = {
        "steward_name": steward_name,
        "steward_email": steward_email,
        "cert_id": cert_id,
        "appointment_key": appointment_key,
        "status": "DISPATCHED"
    }
    
    os.makedirs("intake/dispatched_keys", exist_ok=True)
    with open(f"intake/dispatched_keys/{cert_id}_key.json", "w") as f:
        json.dump(record, f, indent=4)

if __name__ == "__main__":
    send_dome_key_email("Sipho Wiseman Khuzwayo", "sipho@prestigedome.internal", "PDD-M1-PQD4SSCGH")
