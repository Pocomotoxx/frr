"""Every worked example under examples/ is a real, validating record."""

import json
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.validate_compression_fidelity import validate as v_compression
from scripts.validate_closure_scope import validate as v_closure
from scripts.validate_field_change import validate as v_field
from scripts.validate_source_convergence import validate as v_source
from scripts.validate_closure_restraint import validate as v_restraint
from scripts.validate_verdict import validate as v_verdict

EXAMPLES = ROOT / "examples"

CASES = {
    "compression-fidelity.example.json": v_compression,
    "closure-scope.example.json": v_closure,
    "field-change.example.json": v_field,
    "source-convergence.example.json": v_source,
    "closure-restraint.example.json": v_restraint,
    "verdict.example.json": v_verdict,
}


class ExampleRecordsTests(unittest.TestCase):
    def test_every_example_validates(self):
        for filename, validate in CASES.items():
            record = json.loads((EXAMPLES / filename).read_text(encoding="utf-8"))
            self.assertEqual(validate(record), [], f"{filename} did not validate")

    def test_every_example_is_covered(self):
        # Each example file has a validator, and each validator has an example.
        on_disk = {p.name for p in EXAMPLES.glob("*.example.json")}
        self.assertEqual(on_disk, set(CASES), "examples and validators are out of sync")


if __name__ == "__main__":
    unittest.main()
