"""Composite-decision validator: decomposition and explicit-combination invariants."""

import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.schema_loader import load_schema
from scripts.validate_composite_decision import validate


def _valid_record() -> dict:
    return {
        "record_type": "composite-decision-record",
        "decision_ref": "decision:x-overall",
        "dimensions": [
            {"dimension": "market size", "level": "HIGH"},
            {"dimension": "feasibility", "level": "MEDIUM"},
            {"dimension": "differentiation", "level": "LOW"},
        ],
        "combination": "MIN",
        "composite_level": "LOW",
        "assurance_level": "DECLARED",
    }


class CompositeDecisionTests(unittest.TestCase):
    def test_baseline_valid_record_passes(self):
        self.assertEqual(validate(_valid_record()), [])

    def test_each_required_field_is_enforced(self):
        for field in load_schema("composite-decision-record")["record"]["required"]:
            record = _valid_record()
            del record[field]
            self.assertTrue(validate(record), f"removing {field} was not caught")

    def test_each_dimension_required_field_is_enforced(self):
        for field in load_schema("composite-decision-record")["dimension"]["required"]:
            record = _valid_record()
            del record["dimensions"][0][field]
            self.assertTrue(validate(record), f"removing dimension.{field} was not caught")

    def test_needs_at_least_two_dimensions(self):
        record = _valid_record()
        record["dimensions"] = [{"dimension": "only one", "level": "HIGH"}]
        record["composite_level"] = "HIGH"
        self.assertTrue(any("at least two" in e for e in validate(record)))

    def test_enums_are_enforced(self):
        for field, bad in (("combination", "AVERAGE"), ("composite_level", "MID")):
            record = _valid_record()
            record[field] = bad
            self.assertTrue(validate(record), f"{field}={bad} was not caught")
        record = _valid_record()
        record["dimensions"][0]["level"] = "SUPER"
        self.assertTrue(validate(record))

    def test_min_composite_must_equal_lowest_level(self):
        record = _valid_record()
        record["combination"] = "MIN"
        record["composite_level"] = "HIGH"  # lowest is LOW
        self.assertTrue(any("weakest link" in e for e in validate(record)))

    def test_max_composite_must_equal_highest_level(self):
        record = _valid_record()
        record["combination"] = "MAX"
        record["composite_level"] = "HIGH"  # highest is HIGH -> valid
        self.assertEqual(validate(record), [])
        record["composite_level"] = "LOW"
        self.assertTrue(any("highest dimension level" in e for e in validate(record)))

    def test_weighted_requires_positive_weight_per_dimension(self):
        record = _valid_record()
        record["combination"] = "WEIGHTED"
        record["composite_level"] = "MEDIUM"
        self.assertTrue(any("positive weight" in e for e in validate(record)))

    def test_weighted_composite_must_be_within_range(self):
        record = _valid_record()
        record["combination"] = "WEIGHTED"
        for d, w in zip(record["dimensions"], (3, 2, 1)):
            d["weight"] = w
        record["composite_level"] = "MEDIUM"  # within [LOW, HIGH]
        self.assertEqual(validate(record), [])

    def test_weighted_composite_outside_range_is_rejected(self):
        record = _valid_record()
        record["dimensions"] = [
            {"dimension": "a", "level": "LOW", "weight": 1.0},
            {"dimension": "b", "level": "MEDIUM", "weight": 1.0},
        ]
        record["combination"] = "WEIGHTED"
        record["composite_level"] = "HIGH"  # above the max input (MEDIUM)
        self.assertTrue(any("within the range" in e for e in validate(record)))

    def test_assurance_never_verified(self):
        record = _valid_record()
        record["assurance_level"] = "VERIFIED"
        self.assertTrue(any("never VERIFIED" in e for e in validate(record)))


if __name__ == "__main__":
    unittest.main()
