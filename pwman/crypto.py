from dataclasses import dataclass
import os, base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet

# bewusst nicht zu niedrig, aber für CLI noch praktikabel
ITERATIONS = 200_000

@dataclass
class KeyMaterial:
    salt: bytes
    key: bytes  # Fernet-Schlüssel (Base64-encoded 32 Byte)

def _derive_key(master_password: str, salt: bytes) -> bytes:
    """Leitet aus Master-Passwort + Salt einen 32-Byte-Key ab und
    kodiert ihn Base64-urlsafe für Fernet.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS,
    )
    raw = kdf.derive(master_password.encode("utf-8"))
    return base64.urlsafe_b64encode(raw)


def make_key(master_password: str, salt: bytes | None = None) -> KeyMaterial:
    if salt is None:
        salt = os.urandom(16)
    key = _derive_key(master_password, salt)
    return KeyMaterial(salt=salt, key=key)


def encrypt_json(data: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(data)


def decrypt_json(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)
