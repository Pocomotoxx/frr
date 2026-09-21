"""Prose, JSON source, and validator cannot drift apart.

For every schema with a JSON source, the prose .schema.md must reference that JSON
source and must name (in backticks) every field the JSON enforces, so the prose can
never document a different contract than the code enforces.
"""

import re
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.schema_loader import SCHEMA_DIR, load_schema


def json_backed_schemas() -> list[str]:
    return sorted(p.name.replace(".schema.json", "") for p in SCHEMA_DIR.glob("*.schema.json"))


class SchemaConsistencyTests(unittest.TestCase):
    def test_there_are_schemas(self):
        self.assertTrue(json_backed_schemas(), "no JSON-backed schemas found")

    def test_prose_points_at_the_json_source(self):
        for name in json_backed_schemas():
            prose = (SCHEMA_DIR / f"{name}.schema.md").read_text(encoding="utf-8")
            self.assertIn(f"{name}.schema.json", prose,
                          f"{name}.schema.md does not reference its JSON source")

    def test_every_enforced_field_is_named_in_the_prose(self):
        for name in json_backed_schemas():
            prose = (SCHEMA_DIR / f"{name}.schema.md").read_text(encoding="utf-8")
            mentioned = set(re.findall(r"`([a-z_]+)`", prose))
            schema = load_schema(name)
            for section in schema:
                block = schema[section]
                if not isinstance(block, dict) or "required" not in block:
                    continue
                for field in block["required"]:
                    self.assertIn(field, mentioned,
                                  f"{name}.schema.md does not document enforced field {field!r}")


if __name__ == "__main__":
    unittest.main()
