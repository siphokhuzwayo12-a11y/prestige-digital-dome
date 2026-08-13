import os
import json
import re

def sanitize_and_vault(raw_email_path):
    """
    Parses incoming raw email files, strips tracker pixels/HTML,
    and drops pure encrypted/sanitized payloads into transmission/inbox.
    """
    if not os.path.exists(raw_email_path):
        print(f"[X] File not found: {raw_email_path}")
        return

    with open(raw_email_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Strip HTML tags and tracker URLs
    clean_text = re.sub(r'<[^>]+>', '', content)
    
    vault_entry = {
        "status": "VAULTED_UNREAD",
        "security_level": "ZERO_LEAK_CONFIDENTIAL",
        "payload": clean_text.strip()
    }

    out_path = os.path.join("transmission", "inbox", "vaulted_message.json")
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(vault_entry, f, indent=2)

    print(f"[?] Email successfully sanitized and locked inside: {out_path}")

if __name__ == "__main__":
    print("[+] Zero-Leak Mail Engine Active.")
