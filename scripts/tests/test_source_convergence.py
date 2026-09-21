"""Source-convergence validator: shape and the independence invariants."""

import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.schema_loader import load_schema
from scripts.validate_source_convergence import validate


def _valid_record() -> dict:
    return {
        "record_type": "source-convergence-record",
        "claim_ref": "claim:x-supported",
        "source_refs": ["src:A", "src:B"],
        "convergence": "INDEPENDENT",
        "strengthens_claim": True,
        "assurance_level": "DECLARED",
    }


class SourceConvergenceTests(unittest.TestCase):
    def test_baseline_valid_record_passes(self):
        self.assertEqual(validate(_valid_record()), [])

    def test_each_required_field_is_enforced(self):
        for field in load_schema("source-convergence-record")["record"]["required"]:
            record = _valid_record()
            del record[field]
            self.assertTrue(validate(record), f"removing {field} was not caught")

    def test_needs_two_distinct_sources(self):
        record = _valid_record()
        record["source_refs"] = ["src:A"]
        self.assertTrue(validate(record))
        record["source_refs"] = ["src:A", "src:A"]
        self.assertTrue(any("two distinct" in e for e in validate(record)))

    def test_strengthens_requires_independent(self):
        record = _valid_record()
        record["convergence"] = "SHARED_ORIGIN"
        record["shared_origin_ref"] = "both cite benchmark Q"
        record["strengthens_claim"] = True
        self.assertTrue(any("not corroboration" in e for e in validate(record)))
        record["strengthens_claim"] = False
        self.assertEqual(validate(record), [])

    def test_shared_origin_requires_ref(self):
        record = _valid_record()
        record["convergence"] = "SHARED_ORIGIN"
        record["strengthens_claim"] = False
        self.assertTrue(any("shared_origin_ref" in e for e in validate(record)))

    def test_strengthens_must_be_boolean(self):
        record = _valid_record()
        record["strengthens_claim"] = "yes"
        self.assertTrue(validate(record))

    def test_assurance_never_verified(self):
        record = _valid_record()
        record["assurance_level"] = "VERIFIED"
        self.assertTrue(validate(record))

    def test_convergence_enum_is_enforced(self):
        record = _valid_record()
        record["convergence"] = "VIBES"
        self.assertTrue(validate(record))


if __name__ == "__main__":
    unittest.main()
