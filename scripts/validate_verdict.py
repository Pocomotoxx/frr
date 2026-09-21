"""Validate a verdict record: evidence before verdict.

A claim that a goal was achieved is decided against declared success criteria, each
with its own status and, when passing, its own cited evidence. A criterion cannot
pass on an advisory or on prose; a verdict cannot be ACHIEVED unless every criterion
passes. Assurance never reaches VERIFIED — a verdict is a reading of the evidence
against the criteria, not execution-scope proof.

Structure only: it does not certify the goal was truly met, only that the verdict
was posed against declared, evidence-cited criteria and is internally consistent.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.schema_loader import enum, required as required_fields

SCHEMA = "verdict-record"
REQUIRED = required_fields(SCHEMA, "record")
VERDICT = enum(SCHEMA, "record", "verdict")
ASSURANCE = enum(SCHEMA, "record", "assurance_level")
CRITERION_REQUIRED = required_fields(SCHEMA, "criterion")
STATUS = enum(SCHEMA, "criterion", "status")


def _text(value: object) -> str:
    return str(value).strip() if value is not None else ""


def validate(record: dict) -> list[str]:
    if not isinstance(record, dict):
        return ["record must be an object"]
    errors = [f"missing required field: {name}" for name in sorted(REQUIRED - set(record))]
    if errors:
        return errors

    if record["record_type"] != "verdict-record":
        errors.append("record_type must be verdict-record")
    if not _text(record.get("goal_ref")):
        errors.append("goal_ref must be a non-empty string")
    if record.get("verdict") not in VERDICT:
        errors.append("verdict must be ACHIEVED, NOT_ACHIEVED, PARTIAL, or UNVERIFIABLE")
    if record.get("assurance_level") not in ASSURANCE:
        errors.append("assurance_level must be DECLARED or UNVERIFIABLE (never VERIFIED)")

    criteria = record.get("criteria")
    all_pass = True
    if not isinstance(criteria, list) or not criteria:
        errors.append("criteria must be a non-empty list of declared success criteria")
        all_pass = False
    else:
        for index, item in enumerate(criteria):
            if not isinstance(item, dict):
                errors.append(f"criterion[{index}] must be an object")
                all_pass = False
                continue
            for field in sorted(CRITERION_REQUIRED - set(item)):
                errors.append(f"criterion[{index}] missing {field}")
            if not _text(item.get("criterion")):
                errors.append(f"criterion[{index}] criterion must be a non-empty string")
            status = item.get("status")
            if status not in STATUS:
                errors.append(f"criterion[{index}] status must be PASS, FAIL, or UNVERIFIABLE")
            if status != "PASS":
                all_pass = False
            elif not _text(item.get("evidence_ref")):
                errors.append(f"criterion[{index}] is PASS, so it requires a non-empty evidence_ref (not an advisory or prose)")

    if record.get("verdict") == "ACHIEVED" and not all_pass:
        errors.append("verdict ACHIEVED requires every criterion to be PASS; a FAIL or UNVERIFIABLE criterion forbids ACHIEVED")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_verdict.py RECORD.json")
        return 2
    errors = validate(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")))
    print("Verdict validation: " + ("PASS" if not errors else "FAIL"))
    if errors:
        print(*[f"- {error}" for error in errors], sep="\n")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
