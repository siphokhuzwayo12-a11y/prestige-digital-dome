import os
import sys
import argparse
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

SALT = b'PrestigeDomeSovereignSalt2026'

def derive_key(passphrase: str) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=100_000
    )
    return kdf.derive(passphrase.encode())

def encrypt_file(file_path: str, key: bytes):
    if file_path.endswith('.enc'):
        return
    with open(file_path, 'rb') as f:
        data = f.read()
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, data, None)
    with open(file_path + '.enc', 'wb') as f:
        f.write(nonce + ciphertext)
    os.remove(file_path)
    print(f"[+] Encrypted and locked: {file_path}")

def decrypt_file(file_path: str, key: bytes):
    if not file_path.endswith('.enc'):
        return
    with open(file_path, 'rb') as f:
        content = f.read()
    nonce = content[:12]
    ciphertext = content[12:]
    aesgcm = AESGCM(key)
    try:
        data = aesgcm.decrypt(nonce, ciphertext, None)
        original_path = file_path[:-4]
        with open(original_path, 'wb') as f:
            f.write(data)
        os.remove(file_path)
        print(f"[+] Decrypted and restored: {original_path}")
    except Exception as e:
        print(f"[-] Decryption failed for {file_path}: {e}")

def process_vault(action: str, passphrase: str, directory: str = "vault"):
    key = derive_key(passphrase)
    for root, _, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            if action == "encrypt" and not file.endswith('.enc'):
                encrypt_file(full_path, key)
            elif action == "decrypt" and file.endswith('.enc'):
                decrypt_file(full_path, key)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prestige Vault AES-256 Envelope Encryptor")
    parser.add_argument("action", choices=["encrypt", "decrypt"], help="Action to execute")
    parser.add_argument("--passphrase", required=True, help="Steward master passphrase")
    args = parser.parse_args()
    process_vault(args.action, args.passphrase)
