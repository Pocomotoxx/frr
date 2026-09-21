"""Compression-fidelity validator: shape and the discriminative-pressure invariants."""

import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.schema_loader import load_schema
from scripts.validate_compression_fidelity import validate


def _valid_record() -> dict:
    return {
        "record_type": "compression-fidelity-record",
        "claim_ref": "claim:merge-A-B",
        "preserved_behavior": "PREDICTION",
        "scope": {"domain": "d", "horizon": "one step", "tolerance": "1e-3"},
        "trivial_collapse_check": "PASS",
        "probes": [
            {
                "case_a_ref": "case:a",
                "case_b_ref": "case:b",
                "applied_pressure": "LONGER_HORIZON",
                "separated": False,
            }
        ],
        "verdict": "FAITHFUL",
        "assurance_level": "DECLARED",
    }


class CompressionFidelityTests(unittest.TestCase):
    def test_baseline_valid_record_passes(self):
        self.assertEqual(validate(_valid_record()), [])

    def test_each_required_field_is_enforced(self):
        for field in load_schema("compression-fidelity-record")["record"]["required"]:
            record = _valid_record()
            del record[field]
            self.assertTrue(validate(record), f"removing {field} was not caught")

    def test_scope_must_be_fully_specified(self):
        for field in ("domain", "horizon", "tolerance"):
            record = _valid_record()
            record["scope"][field] = "  "
            self.assertTrue(validate(record), f"empty scope.{field} was not caught")

    def test_trivial_collapse_fail_is_rejected(self):
        record = _valid_record()
        record["trivial_collapse_check"] = "FAIL"
        self.assertTrue(any("discriminative pressure" in e for e in validate(record)))

    def test_probes_must_be_non_empty(self):
        record = _valid_record()
        record["probes"] = []
        self.assertTrue(validate(record))

    def test_separated_probe_must_name_returned_distinction(self):
        record = _valid_record()
        record["probes"][0]["separated"] = True
        record["verdict"] = "NEEDS_REPAIR"
        self.assertTrue(any("returned_distinction" in e for e in validate(record)))
        record["probes"][0]["returned_distinction"] = "transient dynamics"
        self.assertEqual(validate(record), [])

    def test_faithful_verdict_forbidden_once_separated(self):
        record = _valid_record()
        record["probes"][0]["separated"] = True
        record["probes"][0]["returned_distinction"] = "transient dynamics"
        record["verdict"] = "FAITHFUL"
        self.assertTrue(any("FAITHFUL is not allowed" in e for e in validate(record)))

    def test_assurance_never_verified(self):
        record = _valid_record()
        record["assurance_level"] = "VERIFIED"
        self.assertTrue(validate(record))

    def test_enum_values_are_rejected(self):
        for field, bad in (
            ("preserved_behavior", "VIBES"),
            ("verdict", "MAYBE"),
        ):
            record = _valid_record()
            record[field] = bad
            self.assertTrue(validate(record), f"{field}={bad} was not caught")
        record = _valid_record()
        record["probes"][0]["applied_pressure"] = "WISHING"
        self.assertTrue(validate(record))


if __name__ == "__main__":
    unittest.main()
