"""Redaction helpers and the record-hygiene validator."""

import json
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.redaction import find_secrets, redact
from scripts.validate_record_hygiene import validate as validate_hygiene


class RedactionTests(unittest.TestCase):
    def test_finds_credential_shapes(self):
        self.assertIn("credential", find_secrets("token sk-ABCD1234EFGH5678"))
        self.assertIn("credential", find_secrets("Authorization: Bearer abcdef.ghijkl"))
        self.assertIn("credential", find_secrets("key AIzaSyABCDEFGHIJKLMNOPQRST"))
        self.assertIn("endpoint", find_secrets("see https://api.example.com/v1/x"))
        self.assertIn("secret_assignment", find_secrets("api_key = hunter2secret"))
        self.assertIn("path", find_secrets("stored at /home/user/creds.txt"))

    def test_clean_text_has_no_secrets(self):
        self.assertEqual(find_secrets("the mug is on the shelf; see image sha256:ab12"), [])

    def test_redact_masks_and_is_deterministic(self):
        raw = "call https://api.example.com with sk-ABCD1234EFGH5678"
        once = redact(raw)
        self.assertNotIn("api.example.com", once)
        self.assertNotIn("sk-ABCD1234EFGH5678", once)
        self.assertIn("[REDACTED_ENDPOINT]", once)
        self.assertEqual(once, redact(raw))

    def test_hygiene_validator_rejects_secret_in_record(self):
        record = {"record_type": "x", "note": "endpoint https://svc.internal/v1", "nested": ["ok", "sk-ABCD1234EFGH5678"]}
        errors = validate_hygiene(record)
        self.assertTrue(any("secret-shaped" in e for e in errors))
        self.assertEqual(validate_hygiene({"record_type": "x", "ref": "claim:1", "digest": "sha256:ab12"}), [])

    def test_every_example_record_is_clean(self):
        for path in (ROOT / "examples").glob("*.example.json"):
            record = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(validate_hygiene(record), [], f"{path.name} carries a secret-shaped value")


if __name__ == "__main__":
    unittest.main()
