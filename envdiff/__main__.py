import argparse
import json
import sys
from pathlib import Path
from .compare import compare
from .parser import parse
from .validate import validate


def main():
    parser = argparse.ArgumentParser(description="Compare environment keys safely")
    commands = parser.add_subparsers(dest="command", required=True)
    diff = commands.add_parser("diff")
    diff.add_argument("left", type=Path)
    diff.add_argument("right", type=Path)
    diff.add_argument("--ignore", action="append", default=[])
    diff.add_argument("--json", action="store_true")
    check = commands.add_parser("check")
    check.add_argument("file", type=Path)
    check.add_argument("schema", type=Path)
    check.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "diff":
            result = compare(parse(args.left.read_text()), parse(args.right.read_text()), args.ignore)
        else:
            result = validate(parse(args.file.read_text()), json.loads(args.schema.read_text()))
    except (OSError, UnicodeError, ValueError, TypeError) as error:
        if isinstance(error, (ValueError, TypeError)):
            message = str(error) if not isinstance(error, json.JSONDecodeError) else "Invalid schema"
        else:
            message = "Could not read an input file"
        print(message, file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for item in result:
            print(item["key"] + ": " + item.get("state", item.get("reason", "")))
    return int(bool(result))


if __name__ == "__main__":
    sys.exit(main())
