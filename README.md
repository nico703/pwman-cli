# pwman-cli

Kleiner Passwort-Manager für die Kommandozeile. **Kein Anspruch auf Enterprise-Security**, aber solide Basics: PBKDF2 mit Salt + Fernet (symmetrische Verschlüsselung).

> Motivation: Ich wollte KDF-/Key-Handling einmal sauber durchspielen und ein nützliches CLI-Tool bauen.

## Features
- Master-Passwort → Key via PBKDF2 (200k Iterationen) + Salt
- Komplett verschlüsselter JSON-Store
- Subcommands: `add`, `get`, `list`
- Optionaler Passwortgenerator (`--generate`)

## Installation
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Nutzung
```bash
# Liste (erzeugt DB bei Bedarf)
python -m pwman.cli list

# Eintrag hinzufügen (User angeben, Passwort generieren)
python -m pwman.cli add github --user nico --generate --length 18

# Eintrag anzeigen
python -m pwman.cli get github
```

## Speicherort
Standard: `~/.pwman.db` (JSON mit Salt + Cipher). **Passwort wird nie im Klartext gespeichert.**

## Sicherheit / Hinweise
- PBKDF2 (SHA-256) mit 200k Iterationen – ok für ein Lern-/CLI-Tool.
- Fernet kümmert sich um Authenticated Encryption (AES128 + HMAC).
- **TODO:** Clipboard-Integration, Passwort-Policies, TOTP-Felder.

## Tests
```bash
pytest -q
```

## Lizenz
MIT (siehe `pyproject.toml`).
