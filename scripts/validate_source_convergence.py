"""Validate a source-convergence record: agreement is not corroboration by default.

Several sources using the same phrase may inherit one origin, benchmark, or
assumption, so agreement across them is evidence only when the routes are
genuinely independent. This validator binds a claim of source agreement to an
independence status, requires at least two distinct sources, lets agreement count
as corroboration only when it is INDEPENDENT, and names the shared origin when it
is not. Assurance never reaches VERIFIED.

Structure only: it does not prove the sources are independent, only that the
agreement claim is scoped and internally consistent.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.schema_loader import enum, required as required_fields

SCHEMA = "source-convergence-record"
REQUIRED = required_fields(SCHEMA, "record")
CONVERGENCE = enum(SCHEMA, "record", "convergence")
ASSURANCE = enum(SCHEMA, "record", "assurance_level")


def _text(value: object) -> str:
    return str(value).strip() if value is not None else ""


def validate(record: dict) -> list[str]:
    if not isinstance(record, dict):
        return ["record must be an object"]
    errors = [f"missing required field: {name}" for name in sorted(REQUIRED - set(record))]
    if errors:
        return errors

    if record["record_type"] != "source-convergence-record":
        errors.append("record_type must be source-convergence-record")
    if not _text(record.get("claim_ref")):
        errors.append("claim_ref must be a non-empty string")
    if record.get("convergence") not in CONVERGENCE:
        errors.append("convergence must be INDEPENDENT, SHARED_ORIGIN, or UNKNOWN")
    if record.get("assurance_level") not in ASSURANCE:
        errors.append("assurance_level must be DECLARED or UNVERIFIABLE (never VERIFIED)")

    sources = record.get("source_refs")
    if not isinstance(sources, list):
        errors.append("source_refs must be a list")
    else:
        distinct = {_text(s) for s in sources if _text(s)}
        if len(distinct) < 2:
            errors.append("source_refs must contain at least two distinct non-empty entries")

    strengthens = record.get("strengthens_claim")
    if not isinstance(strengthens, bool):
        errors.append("strengthens_claim must be a boolean")
    elif strengthens and record.get("convergence") != "INDEPENDENT":
        errors.append(
            "strengthens_claim is true, so convergence must be INDEPENDENT; "
            "shared-origin or unknown agreement is not corroboration"
        )

    if record.get("convergence") == "SHARED_ORIGIN" and not _text(record.get("shared_origin_ref")):
        errors.append("SHARED_ORIGIN requires a non-empty shared_origin_ref")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_source_convergence.py RECORD.json")
        return 2
    errors = validate(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")))
    print("Source convergence validation: " + ("PASS" if not errors else "FAIL"))
    if errors:
        print(*[f"- {error}" for error in errors], sep="\n")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
