from pwman.crypto import make_key, encrypt_json, decrypt_json


def test_roundtrip():
    km = make_key("test123")
    c = encrypt_json(b'{"x":1}', km.key)
    p = decrypt_json(c, km.key)
    assert p == b'{"x":1}'
