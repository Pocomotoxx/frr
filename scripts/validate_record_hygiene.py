"""Validate record hygiene: a record carries references, not raw secrets.

FRR records are metadata. This validator walks every string in a record and flags
any that carries an endpoint- or credential-shaped value — an API key, a bearer
token, a secret assignment, a live URL, or an absolute filesystem path. It applies
to any record type; it is the enforceable form of the record-hygiene discipline in
`field/RECORD_HYGIENE.md`.

Structure only: a clean record proves no secret-shaped value was found, not that the
record's references are correct.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.redaction import find_secrets


def _walk(node: object, path: str, errors: list[str]) -> None:
    if isinstance(node, str):
        categories = find_secrets(node)
        if categories:
            errors.append(f"{path or 'record'} contains a secret-shaped value ({', '.join(categories)}); records carry references, not raw secrets")
    elif isinstance(node, dict):
        for key, value in node.items():
            _walk(value, f"{path}.{key}" if path else str(key), errors)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            _walk(value, f"{path}[{index}]", errors)


def validate(record: object) -> list[str]:
    errors: list[str] = []
    _walk(record, "", errors)
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_record_hygiene.py RECORD.json")
        return 2
    errors = validate(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")))
    print("Record hygiene validation: " + ("PASS" if not errors else "FAIL"))
    if errors:
        print(*[f"- {error}" for error in errors], sep="\n")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
