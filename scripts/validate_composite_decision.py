"""Validate a composite-decision record: decompose, then combine by an explicit rule.

A composite judgment must name at least two atomic factors, judge each on its own
level, and combine them by a declared rule — MIN (weakest link), MAX, or WEIGHTED.
The validator checks that the composite level is the one the declared rule produces
(exact for MIN/MAX, in-range for WEIGHTED), that WEIGHTED dimensions carry a positive
weight, and that assurance never reaches VERIFIED.

Structure only: it does not judge whether each dimension level is the right reading of
the world, only that the composite is decomposed and combined by the declared rule.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.schema_loader import enum, required as required_fields

SCHEMA = "composite-decision-record"
REQUIRED = required_fields(SCHEMA, "record")
COMBINATION = enum(SCHEMA, "record", "combination")
COMPOSITE_LEVEL = enum(SCHEMA, "record", "composite_level")
ASSURANCE = enum(SCHEMA, "record", "assurance_level")
DIMENSION_REQUIRED = required_fields(SCHEMA, "dimension")
LEVEL = enum(SCHEMA, "dimension", "level")

_RANK = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}


def _text(value: object) -> str:
    return str(value).strip() if value is not None else ""


def validate(record: dict) -> list[str]:
    if not isinstance(record, dict):
        return ["record must be an object"]
    errors = [f"missing required field: {name}" for name in sorted(REQUIRED - set(record))]
    if errors:
        return errors

    if record["record_type"] != "composite-decision-record":
        errors.append("record_type must be composite-decision-record")
    if not _text(record.get("decision_ref")):
        errors.append("decision_ref must be a non-empty string")
    if record.get("combination") not in COMBINATION:
        errors.append("combination must be MIN, MAX, or WEIGHTED")
    if record.get("composite_level") not in COMPOSITE_LEVEL:
        errors.append("composite_level must be LOW, MEDIUM, or HIGH")
    if record.get("assurance_level") not in ASSURANCE:
        errors.append("assurance_level must be DECLARED or UNVERIFIABLE (never VERIFIED)")

    combination = record.get("combination")
    dimensions = record.get("dimensions")
    levels: list[int] = []
    if not isinstance(dimensions, list) or len(dimensions) < 2:
        errors.append("dimensions must be a list of at least two atomic factors")
    else:
        for index, item in enumerate(dimensions):
            if not isinstance(item, dict):
                errors.append(f"dimension[{index}] must be an object")
                continue
            for field in sorted(DIMENSION_REQUIRED - set(item)):
                errors.append(f"dimension[{index}] missing {field}")
            if not _text(item.get("dimension")):
                errors.append(f"dimension[{index}] dimension must be a non-empty string")
            level = item.get("level")
            if level not in LEVEL:
                errors.append(f"dimension[{index}] level must be LOW, MEDIUM, or HIGH")
            else:
                levels.append(_RANK[level])
            if combination == "WEIGHTED":
                weight = item.get("weight")
                if not isinstance(weight, (int, float)) or isinstance(weight, bool) or weight <= 0:
                    errors.append(f"dimension[{index}] requires a positive weight under WEIGHTED combination")

    # Combination consistency (only when the levels and composite are well-formed).
    composite = record.get("composite_level")
    if levels and composite in COMPOSITE_LEVEL:
        c = _RANK[composite]
        if combination == "MIN" and c != min(levels):
            errors.append("MIN combination: composite_level must equal the lowest dimension level (the weakest link)")
        elif combination == "MAX" and c != max(levels):
            errors.append("MAX combination: composite_level must equal the highest dimension level")
        elif combination == "WEIGHTED" and not (min(levels) <= c <= max(levels)):
            errors.append("WEIGHTED combination: composite_level must lie within the range of the dimension levels")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_composite_decision.py RECORD.json")
        return 2
    errors = validate(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")))
    print("Composite decision validation: " + ("PASS" if not errors else "FAIL"))
    if errors:
        print(*[f"- {error}" for error in errors], sep="\n")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
