import json, os
from .crypto import make_key, encrypt_json, decrypt_json

DEFAULT_DB = os.path.expanduser("~/.pwman.db")


def load_db(path=DEFAULT_DB):
    if not os.path.exists(path):
        return {"salt": None, "cipher": None}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_db(obj, path=DEFAULT_DB):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)


def get_store(master_password: str, path=DEFAULT_DB):
    obj = load_db(path)
    salt = bytes.fromhex(obj["salt"]) if obj.get("salt") else None
    km = make_key(master_password, salt)

    if obj.get("cipher"):
        try:
            plain = decrypt_json(bytes.fromhex(obj["cipher"]), km.key)
            data = json.loads(plain.decode("utf-8"))
        except Exception:
            raise SystemExit("Master-Passwort falsch oder Datei beschädigt.")
    else:
        data = {"items": {}}

    return obj, km, data


def write_store(obj, km, data, path=DEFAULT_DB):
    obj["salt"] = km.salt.hex()
    cipher = encrypt_json(json.dumps(data).encode("utf-8"), km.key)
    obj["cipher"] = cipher.hex()
    save_db(obj, path)
