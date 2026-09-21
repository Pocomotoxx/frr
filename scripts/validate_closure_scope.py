"""Validate a closure-scope record: match the claim to the scope actually examined.

The most common overclaim is a silent upgrade: "the current reasoning did not
resolve it" becomes "an established open problem", or "I did not find it in a
search" becomes "novel". This validator binds a non-resolution claim to a stated
basis and enforces two calibration rules: novelty needs field-level evidence, not
mere absence from a search; and an established-open scope must cite that evidence.
Assurance never reaches VERIFIED.

Structure only: it does not prove the claim is open or novel, only that it is
scoped to what was actually examined and internally consistent.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.schema_loader import enum, required as required_fields

SCHEMA = "closure-scope-record"
REQUIRED = required_fields(SCHEMA, "record")
ASSERTION_KIND = enum(SCHEMA, "record", "assertion_kind")
CLOSURE_SCOPE = enum(SCHEMA, "record", "closure_scope")
ASSURANCE = enum(SCHEMA, "record", "assurance_level")


def _text(value: object) -> str:
    return str(value).strip() if value is not None else ""


def validate(record: dict) -> list[str]:
    if not isinstance(record, dict):
        return ["record must be an object"]
    errors = [f"missing required field: {name}" for name in sorted(REQUIRED - set(record))]
    if errors:
        return errors

    if record["record_type"] != "closure-scope-record":
        errors.append("record_type must be closure-scope-record")
    if not _text(record.get("claim_ref")):
        errors.append("claim_ref must be a non-empty string")
    if not _text(record.get("basis_ref")):
        errors.append("basis_ref must be a non-empty string (state what was actually examined)")
    if record.get("assertion_kind") not in ASSERTION_KIND:
        errors.append("assertion_kind must be UNRESOLVED or NOVEL")
    if record.get("closure_scope") not in CLOSURE_SCOPE:
        errors.append("closure_scope must be one of " + ", ".join(sorted(CLOSURE_SCOPE)))
    if record.get("assurance_level") not in ASSURANCE:
        errors.append("assurance_level must be DECLARED or UNVERIFIABLE (never VERIFIED)")

    scope = record.get("closure_scope")
    if record.get("assertion_kind") == "NOVEL" and scope != "ESTABLISHED_OPEN":
        errors.append(
            "a NOVEL assertion requires closure_scope ESTABLISHED_OPEN; absence from a "
            "search is not novelty"
        )
    if scope == "ESTABLISHED_OPEN" and not _text(record.get("field_evidence_ref")):
        errors.append("ESTABLISHED_OPEN requires a non-empty field_evidence_ref")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_closure_scope.py RECORD.json")
        return 2
    errors = validate(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")))
    print("Closure scope validation: " + ("PASS" if not errors else "FAIL"))
    if errors:
        print(*[f"- {error}" for error in errors], sep="\n")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
