import argparse, getpass, secrets, string, subprocess
from .storage import get_store, write_store


def gen_password(length=16):
    # simpler Generator; TODO: konfigurierbare Policies
    charset = string.ascii_letters + string.digits + "!$%#@_-"
    return "".join(secrets.choice(charset) for _ in range(length))


def cmd_add(args):
    mpw = getpass.getpass("Master-Passwort: ")
    obj, km, data = get_store(mpw)
    if args.generate:
        pw = gen_password(args.length)
    else:
        pw = getpass.getpass("Neues Passwort: ")
    data["items"][args.name] = {"user": args.user, "password": pw}
    write_store(obj, km, data)
    print(f"✓ Eintrag '{args.name}' gespeichert.")


def cmd_get(args):
    mpw = getpass.getpass("Master-Passwort: ")
    _, _, data = get_store(mpw)
    item = data["items"].get(args.name)
    if not item:
        print("Kein Eintrag gefunden.")
        return
    if getattr(args, "copy", False):
        try:
            # macOS: pbcopy
            p = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
            p.communicate(input=item["password"].encode("utf-8"))
            print("✓ Passwort in die Zwischenablage kopiert.")
        except FileNotFoundError:
            print("pbcopy nicht gefunden. Passwort wird ausgegeben:")
            print(item["password"])
    else:
        print(f"User: {item['user']}\\nPasswort: {item['password']}")


def cmd_list(_):
    mpw = getpass.getpass("Master-Passwort: ")
    _, _, data = get_store(mpw)
    for name in sorted(data["items"].keys()):
        print(name)


def build():
    p = argparse.ArgumentParser(prog="pwman", description="Einfacher Passwort-Manager (CLI)")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", help="Eintrag hinzufügen")
    a.add_argument("name")
    a.add_argument("--user", required=True)
    a.add_argument("--generate", action="store_true")
    a.add_argument("--length", type=int, default=16)
    a.set_defaults(func=cmd_add)

    g = sub.add_parser("get", help="Eintrag anzeigen")
    g.add_argument("name")
    g.set_defaults(func=cmd_get)

    l = sub.add_parser("list", help="Einträge auflisten")
    l.set_defaults(func=cmd_list)

    return p


def main():
    args = build().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
