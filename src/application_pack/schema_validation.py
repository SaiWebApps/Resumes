from __future__ import annotations

import re
from importlib import resources
from pathlib import Path
from typing import Any

from .artifacts import load_json
from .contracts import ContractError


def schema_path(name: str) -> Path:
    packaged = resources.files("application_pack").joinpath("schemas", name)
    try:
        if packaged.is_file():
            return Path(str(packaged))
    except (FileNotFoundError, TypeError):
        pass
    checkout = Path(__file__).resolve().parents[2] / "schemas" / name
    if checkout.is_file():
        return checkout
    raise ContractError(f"Schema resource is unavailable: {name}")


def _type_matches(value: Any, expected: str) -> bool:
    return {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "integer": isinstance(value, int) and not isinstance(value, bool),
        "number": isinstance(value, (int, float)) and not isinstance(value, bool),
        "boolean": isinstance(value, bool),
        "null": value is None,
    }.get(expected, True)


def _resolve_local_ref(root: dict[str, Any], ref: str) -> dict[str, Any]:
    if not ref.startswith("#/"):
        raise ContractError(f"Only local schema refs are supported by the portable validator: {ref}")
    value: Any = root
    for token in ref[2:].split("/"):
        value = value[token.replace("~1", "/").replace("~0", "~")]
    if not isinstance(value, dict):
        raise ContractError(f"Schema ref does not resolve to an object: {ref}")
    return value


def _basic_validate(instance: Any, schema: dict[str, Any], root: dict[str, Any], path: str = "$") -> None:
    if "$ref" in schema:
        _basic_validate(instance, _resolve_local_ref(root, schema["$ref"]), root, path)
        return
    for subschema in schema.get("allOf", []):
        if isinstance(subschema, dict):
            _basic_validate(instance, subschema, root, path)
    condition = schema.get("if")
    if isinstance(condition, dict):
        try:
            _basic_validate(instance, condition, root, path)
            matched = True
        except ContractError:
            matched = False
        branch = schema.get("then") if matched else schema.get("else")
        if isinstance(branch, dict):
            _basic_validate(instance, branch, root, path)
    if "const" in schema and instance != schema["const"]:
        raise ContractError(f"{path} must equal {schema['const']!r}")
    if "enum" in schema and instance not in schema["enum"]:
        raise ContractError(f"{path} must be one of {schema['enum']!r}")
    expected = schema.get("type")
    if isinstance(expected, str) and not _type_matches(instance, expected):
        raise ContractError(f"{path} must be of type {expected}")
    if isinstance(expected, list) and not any(_type_matches(instance, item) for item in expected):
        raise ContractError(f"{path} must be one of types {expected}")
    if isinstance(instance, dict):
        for key in schema.get("required", []):
            if key not in instance:
                raise ContractError(f"{path}.{key} is required")
        properties = schema.get("properties", {})
        for key, value in instance.items():
            if key in properties:
                _basic_validate(value, properties[key], root, f"{path}.{key}")
            elif isinstance(schema.get("additionalProperties"), dict):
                _basic_validate(value, schema["additionalProperties"], root, f"{path}.{key}")
            elif schema.get("additionalProperties") is False:
                raise ContractError(f"{path}.{key} is not allowed")
    if isinstance(instance, list):
        if len(instance) < schema.get("minItems", 0):
            raise ContractError(f"{path} requires at least {schema['minItems']} items")
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            raise ContractError(f"{path} allows at most {schema['maxItems']} items")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, value in enumerate(instance):
                _basic_validate(value, item_schema, root, f"{path}[{index}]")
    if isinstance(instance, str):
        if len(instance) < schema.get("minLength", 0):
            raise ContractError(f"{path} requires at least {schema['minLength']} characters")
        if "pattern" in schema and re.fullmatch(schema["pattern"], instance) is None:
            raise ContractError(f"{path} does not match {schema['pattern']!r}")
    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            raise ContractError(f"{path} must be >= {schema['minimum']}")
        if "maximum" in schema and instance > schema["maximum"]:
            raise ContractError(f"{path} must be <= {schema['maximum']}")


def validate_document(instance: Any, schema_name: str) -> None:
    schema = load_json(schema_path(schema_name))
    try:
        import jsonschema
    except ImportError:
        _basic_validate(instance, schema, schema)
        return
    try:
        jsonschema.Draft202012Validator(schema).validate(instance)
    except jsonschema.ValidationError as exc:
        location = "$" + "".join(f"[{part}]" if isinstance(part, int) else f".{part}" for part in exc.absolute_path)
        raise ContractError(f"{schema_name} validation failed at {location}: {exc.message}") from exc
