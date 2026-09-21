"""Closure-scope validator: shape and the calibrated-open invariants."""

import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.schema_loader import load_schema
from scripts.validate_closure_scope import validate


def _valid_record() -> dict:
    return {
        "record_type": "closure-scope-record",
        "claim_ref": "claim:x-unresolved",
        "assertion_kind": "UNRESOLVED",
        "closure_scope": "OPEN_UNDER_METHOD",
        "basis_ref": "attempted contraction proof, method M",
        "assurance_level": "DECLARED",
    }


class ClosureScopeTests(unittest.TestCase):
    def test_baseline_valid_record_passes(self):
        self.assertEqual(validate(_valid_record()), [])

    def test_each_required_field_is_enforced(self):
        for field in load_schema("closure-scope-record")["record"]["required"]:
            record = _valid_record()
            del record[field]
            self.assertTrue(validate(record), f"removing {field} was not caught")

    def test_basis_ref_must_be_non_empty(self):
        record = _valid_record()
        record["basis_ref"] = "   "
        self.assertTrue(validate(record))

    def test_novel_requires_established_open(self):
        record = _valid_record()
        record["assertion_kind"] = "NOVEL"
        record["closure_scope"] = "UNLOCATED_IN_SEARCH"
        self.assertTrue(any("not novelty" in e for e in validate(record)))

    def test_established_open_requires_field_evidence(self):
        record = _valid_record()
        record["closure_scope"] = "ESTABLISHED_OPEN"
        self.assertTrue(any("field_evidence_ref" in e for e in validate(record)))
        record["field_evidence_ref"] = "survey 2025, Section 4 lists it as open"
        self.assertEqual(validate(record), [])

    def test_valid_novelty_with_field_evidence_passes(self):
        record = _valid_record()
        record["assertion_kind"] = "NOVEL"
        record["closure_scope"] = "ESTABLISHED_OPEN"
        record["field_evidence_ref"] = "no prior art in surveyed venues X, Y, Z"
        self.assertEqual(validate(record), [])

    def test_assurance_never_verified(self):
        record = _valid_record()
        record["assurance_level"] = "VERIFIED"
        self.assertTrue(validate(record))

    def test_enum_values_are_rejected(self):
        for field, bad in (
            ("assertion_kind", "DEFINITELY"),
            ("closure_scope", "OPEN_VIBES"),
        ):
            record = _valid_record()
            record[field] = bad
            self.assertTrue(validate(record), f"{field}={bad} was not caught")


if __name__ == "__main__":
    unittest.main()
