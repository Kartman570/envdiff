import fnmatch


def compare(left, right, ignore=()):
    changes = []
    for key in sorted(left.keys() | right.keys()):
        if any(fnmatch.fnmatchcase(key, pattern) for pattern in ignore):
            continue
        if key not in left:
            state = "added"
        elif key not in right:
            state = "removed"
        elif left[key] != right[key]:
            state = "changed"
        else:
            continue
        changes.append({"key": key, "state": state})
    return changes
