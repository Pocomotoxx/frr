"""Validate a compression-fidelity record: discriminative pressure, not proof.

A compression — a summary, an equivalence class, a merge, a "same as", an
effective state — earns the right to represent many things as one only if the
distinctions it erases stay irrelevant to the behavior, domain, horizon, and
tolerance it claims to preserve. This validator enforces that shape: a fully
specified scope, a trivial-collapse check that passed, at least one disconfirming
probe, a probe that separated the merged cases naming what returned, and a verdict
that cannot be FAITHFUL once anything separated. Assurance never reaches VERIFIED.

Structure only: it does not judge whether the compression is correct, only that a
fidelity test was posed and is internally consistent.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.schema_loader import enum, required as required_fields

SCHEMA = "compression-fidelity-record"
REQUIRED = required_fields(SCHEMA, "record")
PRESERVED_BEHAVIOR = enum(SCHEMA, "record", "preserved_behavior")
TRIVIAL_COLLAPSE = enum(SCHEMA, "record", "trivial_collapse_check")
VERDICT = enum(SCHEMA, "record", "verdict")
ASSURANCE = enum(SCHEMA, "record", "assurance_level")
SCOPE_REQUIRED = required_fields(SCHEMA, "scope")
PROBE_REQUIRED = required_fields(SCHEMA, "probe")
APPLIED_PRESSURE = enum(SCHEMA, "probe", "applied_pressure")


def _text(value: object) -> str:
    return str(value).strip() if value is not None else ""


def validate(record: dict) -> list[str]:
    if not isinstance(record, dict):
        return ["record must be an object"]
    errors = [f"missing required field: {name}" for name in sorted(REQUIRED - set(record))]
    if errors:
        return errors

    if record["record_type"] != "compression-fidelity-record":
        errors.append("record_type must be compression-fidelity-record")
    if not _text(record.get("claim_ref")):
        errors.append("claim_ref must be a non-empty string")
    if record.get("preserved_behavior") not in PRESERVED_BEHAVIOR:
        errors.append("preserved_behavior must be one of " + ", ".join(sorted(PRESERVED_BEHAVIOR)))
    if record.get("assurance_level") not in ASSURANCE:
        errors.append("assurance_level must be DECLARED or UNVERIFIABLE (never VERIFIED)")

    scope = record.get("scope")
    if not isinstance(scope, dict):
        errors.append("scope must be an object")
    else:
        for field in sorted(SCOPE_REQUIRED - set(scope)):
            errors.append(f"scope missing {field}")
        for field in sorted(SCOPE_REQUIRED & set(scope)):
            if not _text(scope.get(field)):
                errors.append(f"scope.{field} must be a non-empty string")

    if record.get("trivial_collapse_check") not in TRIVIAL_COLLAPSE:
        errors.append("trivial_collapse_check must be PASS or FAIL")
    elif record.get("trivial_collapse_check") == "FAIL":
        errors.append(
            "trivial_collapse_check must be PASS; a criterion satisfied by merging "
            "everything lacks discriminative pressure and the compression is inadmissible"
        )

    probes = record.get("probes")
    any_separated = False
    if not isinstance(probes, list) or not probes:
        errors.append("probes must be a non-empty list (at least one disconfirming probe)")
    else:
        for index, probe in enumerate(probes):
            if not isinstance(probe, dict):
                errors.append(f"probe[{index}] must be an object")
                continue
            for field in sorted(PROBE_REQUIRED - set(probe)):
                errors.append(f"probe[{index}] missing {field}")
            if probe.get("applied_pressure") not in APPLIED_PRESSURE:
                errors.append(f"probe[{index}] applied_pressure must be one of " + ", ".join(sorted(APPLIED_PRESSURE)))
            separated = probe.get("separated")
            if not isinstance(separated, bool):
                errors.append(f"probe[{index}] separated must be a boolean")
            elif separated:
                any_separated = True
                if not _text(probe.get("returned_distinction")):
                    errors.append(f"probe[{index}] separated is true, so returned_distinction must be named")

    verdict = record.get("verdict")
    if verdict not in VERDICT:
        errors.append("verdict must be FAITHFUL, NEEDS_REPAIR, or REJECTED")
    elif verdict == "FAITHFUL" and any_separated:
        errors.append(
            "verdict FAITHFUL is not allowed once a probe separated the merged cases; "
            "the erased distinction returned, so verdict must be NEEDS_REPAIR or REJECTED"
        )

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_compression_fidelity.py RECORD.json")
        return 2
    errors = validate(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")))
    print("Compression fidelity validation: " + ("PASS" if not errors else "FAIL"))
    if errors:
        print(*[f"- {error}" for error in errors], sep="\n")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
