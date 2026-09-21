"""Verdict validator: shape and the evidence-before-verdict invariants."""

import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.schema_loader import load_schema
from scripts.validate_verdict import validate


def _valid_record() -> dict:
    return {
        "record_type": "verdict-record",
        "goal_ref": "goal:place-the-mug-on-the-shelf",
        "criteria": [
            {"criterion": "mug is on the shelf", "status": "PASS", "evidence_ref": "after-image sha256:ab..12"},
            {"criterion": "shelf undamaged", "status": "UNVERIFIABLE"},
        ],
        "verdict": "PARTIAL",
        "assurance_level": "DECLARED",
    }


class VerdictTests(unittest.TestCase):
    def test_baseline_valid_record_passes(self):
        self.assertEqual(validate(_valid_record()), [])

    def test_each_required_field_is_enforced(self):
        for field in load_schema("verdict-record")["record"]["required"]:
            record = _valid_record()
            del record[field]
            self.assertTrue(validate(record), f"removing {field} was not caught")

    def test_criteria_must_be_non_empty(self):
        record = _valid_record()
        record["criteria"] = []
        self.assertTrue(validate(record))

    def test_pass_criterion_requires_evidence(self):
        record = _valid_record()
        record["criteria"] = [{"criterion": "done", "status": "PASS"}]
        record["verdict"] = "ACHIEVED"
        self.assertTrue(any("evidence_ref" in e for e in validate(record)))

    def test_achieved_requires_all_pass(self):
        record = _valid_record()
        record["verdict"] = "ACHIEVED"  # but one criterion is UNVERIFIABLE
        self.assertTrue(any("ACHIEVED requires" in e for e in validate(record)))

    def test_achieved_with_all_pass_and_evidence_is_valid(self):
        record = _valid_record()
        record["criteria"] = [
            {"criterion": "mug on shelf", "status": "PASS", "evidence_ref": "img:1"},
            {"criterion": "not dropped", "status": "PASS", "evidence_ref": "state:2"},
        ]
        record["verdict"] = "ACHIEVED"
        self.assertEqual(validate(record), [])

    def test_status_and_verdict_enums_are_enforced(self):
        record = _valid_record()
        record["verdict"] = "MAYBE"
        self.assertTrue(validate(record))
        record = _valid_record()
        record["criteria"][0]["status"] = "MEH"
        self.assertTrue(validate(record))

    def test_assurance_never_verified(self):
        record = _valid_record()
        record["assurance_level"] = "VERIFIED"
        self.assertTrue(validate(record))


if __name__ == "__main__":
    unittest.main()
