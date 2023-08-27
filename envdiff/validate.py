from .parser import KEY


def validate(values, schema):
    errors = []
    if not isinstance(schema, dict):
        raise ValueError("Schema must be an object")
    for key, rule in schema.items():
        if not KEY.fullmatch(key) or not isinstance(rule, dict):
            raise ValueError("Invalid schema entry")
        for bound in ("min", "max"):
            if bound in rule and (type(rule[bound]) is not int):
                raise ValueError("Schema bounds must be integers")
        if "choices" in rule and not isinstance(rule["choices"], list):
            raise ValueError("Schema choices must be a list")
        kind = rule.get("type", "string")
        if kind not in ("string", "integer", "boolean"):
            raise ValueError("Unsupported schema type for " + key)
        if key not in values or values[key] == "":
            if rule.get("required", False):
                errors.append({"key": key, "reason": "required value is missing"})
            continue
        value = values[key]
        if kind == "integer":
            try:
                number = int(value)
            except ValueError:
                errors.append({"key": key, "reason": "expected an integer"})
                continue
            if "min" in rule and number < rule["min"]:
                errors.append({"key": key, "reason": "below minimum"})
            if "max" in rule and number > rule["max"]:
                errors.append({"key": key, "reason": "above maximum"})
        elif kind == "boolean" and value.lower() not in ("true", "false", "1", "0"):
            errors.append({"key": key, "reason": "expected a boolean"})
        if "choices" in rule and value not in rule["choices"]:
            errors.append({"key": key, "reason": "not an allowed choice"})
    return errors
