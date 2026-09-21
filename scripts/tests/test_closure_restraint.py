"""Closure-restraint validator: shape and the burden / structure-provenance invariants."""

import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.schema_loader import load_schema
from scripts.validate_closure_restraint import validate


def _valid_record() -> dict:
    return {
        "record_type": "closure-restraint-record",
        "conclusion_ref": "conclusion:the-reorg-caused-the-uncertainty",
        "burden_ref": "the user asked for the cause of the employee uncertainty",
        "imposed_structure": ["CAUSAL"],
        "provenance_refs": ["the memo states the reorg was decided 'because of' the revenue fall (para 4)"],
        "assurance_level": "DECLARED",
    }


class ClosureRestraintTests(unittest.TestCase):
    def test_baseline_valid_record_passes(self):
        self.assertEqual(validate(_valid_record()), [])

    def test_each_required_field_is_enforced(self):
        for field in load_schema("closure-restraint-record")["record"]["required"]:
            record = _valid_record()
            del record[field]
            self.assertTrue(validate(record), f"removing {field} was not caught")

    def test_burden_must_be_non_empty(self):
        record = _valid_record()
        record["burden_ref"] = "   "
        self.assertTrue(any("premature" in e for e in validate(record)))

    def test_imposed_structure_requires_provenance(self):
        record = _valid_record()
        record["imposed_structure"] = ["CAUSAL", "TEMPORAL"]
        record.pop("provenance_refs")
        self.assertTrue(any("provenance_refs" in e for e in validate(record)))

    def test_empty_imposed_structure_needs_no_provenance(self):
        record = _valid_record()
        record["imposed_structure"] = []
        record.pop("provenance_refs")
        self.assertEqual(validate(record), [])

    def test_unknown_structure_is_rejected(self):
        record = _valid_record()
        record["imposed_structure"] = ["VIBES"]
        self.assertTrue(any("unknown structure" in e for e in validate(record)))

    def test_assurance_never_verified(self):
        record = _valid_record()
        record["assurance_level"] = "VERIFIED"
        self.assertTrue(validate(record))


if __name__ == "__main__":
    unittest.main()
