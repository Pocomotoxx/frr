"""Validate a field-change record: inspect the wake, not only the target.

A consequential action changes its target, but it may also change the field
behind itself — later observations, datasets, retrieval stores, users, incentives,
or admissible actions — so that a local success can coexist with a harmful wake.
This validator enforces that the inspection was posed within an explicit boundary,
over named channels, with the target effect kept separate from the field effect,
and an observed wake actually described. Assurance never reaches VERIFIED.

Structure only: it does not prove what the action did, only that its field effect
was inspected and internally consistent.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.schema_loader import enum, required as required_fields, string_list

SCHEMA = "field-change-record"
REQUIRED = required_fields(SCHEMA, "record")
FIELD_EFFECT = enum(SCHEMA, "record", "field_effect")
ASSURANCE = enum(SCHEMA, "record", "assurance_level")
CHANNELS = set(string_list(SCHEMA, "record", "channel"))


def _text(value: object) -> str:
    return str(value).strip() if value is not None else ""


def validate(record: dict) -> list[str]:
    if not isinstance(record, dict):
        return ["record must be an object"]
    errors = [f"missing required field: {name}" for name in sorted(REQUIRED - set(record))]
    if errors:
        return errors

    if record["record_type"] != "field-change-record":
        errors.append("record_type must be field-change-record")
    for field in ("action_ref", "boundary", "target_effect"):
        if not _text(record.get(field)):
            errors.append(f"{field} must be a non-empty string")
    if record.get("field_effect") not in FIELD_EFFECT:
        errors.append("field_effect must be NONE_OBSERVED, OBSERVED, or UNVERIFIABLE")
    if record.get("assurance_level") not in ASSURANCE:
        errors.append("assurance_level must be DECLARED or UNVERIFIABLE (never VERIFIED)")

    channels = record.get("field_channels")
    if not isinstance(channels, list) or not channels:
        errors.append("field_channels must be a non-empty list of inspected channels")
    else:
        for channel in channels:
            if channel not in CHANNELS:
                errors.append("field_channels contains an unknown channel: " + str(channel))

    if record.get("field_effect") == "OBSERVED" and not _text(record.get("wake_ref")):
        errors.append("field_effect OBSERVED requires a non-empty wake_ref naming the observed field change")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_field_change.py RECORD.json")
        return 2
    errors = validate(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")))
    print("Field change validation: " + ("PASS" if not errors else "FAIL"))
    if errors:
        print(*[f"- {error}" for error in errors], sep="\n")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
