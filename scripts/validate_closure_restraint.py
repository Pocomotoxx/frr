"""Validate a closure-restraint record: a conclusion needs a burden and owns its structure.

FRR's kernel licenses descent toward a conclusion only relative to a declared
burden, and warns that a model's structural gravity imposes causal, temporal,
hierarchical, or narrative structure on inputs that lack it. This validator binds a
closure to its licensing burden and forces it to declare what structure it added
beyond the sources; any structure it added must state its provenance. Assurance
never reaches VERIFIED.

Structure only: it does not judge whether the conclusion is correct, only that it
was posed against a burden and its imposed structure declared.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.schema_loader import enum, required as required_fields, string_list

SCHEMA = "closure-restraint-record"
REQUIRED = required_fields(SCHEMA, "record")
ASSURANCE = enum(SCHEMA, "record", "assurance_level")
STRUCTURE = set(string_list(SCHEMA, "record", "structure"))


def _text(value: object) -> str:
    return str(value).strip() if value is not None else ""


def validate(record: dict) -> list[str]:
    if not isinstance(record, dict):
        return ["record must be an object"]
    errors = [f"missing required field: {name}" for name in sorted(REQUIRED - set(record))]
    if errors:
        return errors

    if record["record_type"] != "closure-restraint-record":
        errors.append("record_type must be closure-restraint-record")
    if not _text(record.get("conclusion_ref")):
        errors.append("conclusion_ref must be a non-empty string")
    if not _text(record.get("burden_ref")):
        errors.append("burden_ref must be a non-empty string; a closure with no declared burden is premature")
    if record.get("assurance_level") not in ASSURANCE:
        errors.append("assurance_level must be DECLARED or UNVERIFIABLE (never VERIFIED)")

    imposed = record.get("imposed_structure")
    if not isinstance(imposed, list):
        errors.append("imposed_structure must be a list (empty means no structure added beyond the sources)")
    else:
        for kind in imposed:
            if kind not in STRUCTURE:
                errors.append("imposed_structure contains an unknown structure: " + str(kind))
        if imposed:
            provenance = record.get("provenance_refs")
            if not isinstance(provenance, list) or not any(_text(p) for p in provenance):
                errors.append(
                    "imposed_structure is non-empty, so provenance_refs must name where each "
                    "added structure came from (or that it is imposed and unsourced)"
                )

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_closure_restraint.py RECORD.json")
        return 2
    errors = validate(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")))
    print("Closure restraint validation: " + ("PASS" if not errors else "FAIL"))
    if errors:
        print(*[f"- {error}" for error in errors], sep="\n")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
