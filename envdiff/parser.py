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
        values[key] = decode(value.strip(), number)
    return values


def decode(value, number):
    if value.startswith(("'", '"')):
        quote = value[0]
        result, escaped, end = [], False, None
        for index, char in enumerate(value[1:], 1):
            if escaped:
                result.append({"n": "\n", "t": "\t"}.get(char, char))
                escaped = False
            elif char == "\\" and quote == '"':
                escaped = True
            elif char == quote:
                end = index
                break
            else:
                result.append(char)
        if end is None or (value[end + 1:].strip()
                           and not value[end + 1:].lstrip().startswith("#")):
            raise ValueError("Invalid quoted value on line %d" % number)
        return "".join(result)
    return re.split(r"\s+#", value, maxsplit=1)[0].rstrip()
