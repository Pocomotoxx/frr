"""Field-change validator: shape and the wake-inspection invariants."""

import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.schema_loader import load_schema
from scripts.validate_field_change import validate


def _valid_record() -> dict:
    return {
        "record_type": "field-change-record",
        "action_ref": "action:retrain-on-user-clicks",
        "boundary": "the recommender's retrieval store and served users, next 7 days",
        "target_effect": "click-through improved on the served slate",
        "field_effect": "NONE_OBSERVED",
        "field_channels": ["RETRIEVAL_STORE", "USERS"],
        "assurance_level": "DECLARED",
    }


class FieldChangeTests(unittest.TestCase):
    def test_baseline_valid_record_passes(self):
        self.assertEqual(validate(_valid_record()), [])

    def test_each_required_field_is_enforced(self):
        for field in load_schema("field-change-record")["record"]["required"]:
            record = _valid_record()
            del record[field]
            self.assertTrue(validate(record), f"removing {field} was not caught")

    def test_boundary_and_target_must_be_non_empty(self):
        for field in ("boundary", "target_effect", "action_ref"):
            record = _valid_record()
            record[field] = "  "
            self.assertTrue(validate(record), f"empty {field} was not caught")

    def test_field_channels_must_be_non_empty_and_known(self):
        record = _valid_record()
        record["field_channels"] = []
        self.assertTrue(validate(record))
        record["field_channels"] = ["TELEPATHY"]
        self.assertTrue(any("unknown channel" in e for e in validate(record)))

    def test_observed_field_effect_requires_wake_ref(self):
        record = _valid_record()
        record["field_effect"] = "OBSERVED"
        self.assertTrue(any("wake_ref" in e for e in validate(record)))
        record["wake_ref"] = "later users now see slates shaped by earlier clicks"
        self.assertEqual(validate(record), [])

    def test_assurance_never_verified(self):
        record = _valid_record()
        record["assurance_level"] = "VERIFIED"
        self.assertTrue(validate(record))

    def test_field_effect_enum_is_enforced(self):
        record = _valid_record()
        record["field_effect"] = "MAYBE"
        self.assertTrue(validate(record))


if __name__ == "__main__":
    unittest.main()
