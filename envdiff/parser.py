import re


KEY = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\Z")


def parse(text):
    values = {}
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].lstrip()
        key, separator, value = line.partition("=")
        key = key.strip()
        if not separator or not KEY.fullmatch(key):
            raise ValueError("Invalid assignment on line %d" % number)
        if key in values:
            raise ValueError("Duplicate key %s on line %d" % (key, number))
        values[key] = value.strip()
    return values
