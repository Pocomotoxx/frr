"""Deterministic redaction and secret detection for records.

FRR records are metadata: they carry references and locators, not raw content or
credentials. This module keeps that promise checkable. `find_secrets` reports the
credential- and endpoint-shaped values in a string; `redact` masks them while
retaining semantic context. Both are deterministic and dependency-free, so the same
input always yields the same result.

Adapted from the redaction discipline of the PhyAgentOS embodied-agent OS.
"""

from __future__ import annotations

import re

# (category, pattern, replacement) — ordered; endpoint/credential shapes only.
_RULES: list[tuple[str, "re.Pattern[str]", str]] = [
    ("endpoint", re.compile(r"\b(?:https?|wss?)://[^\s<>()]+", re.IGNORECASE), "[REDACTED_ENDPOINT]"),
    ("credential", re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]+", re.IGNORECASE), "Bearer [REDACTED_CREDENTIAL]"),
    ("credential", re.compile(r"\b(?:sk|pk|ghp|github_pat|xox[baprs])[-_][A-Za-z0-9_-]{8,}\b", re.IGNORECASE), "[REDACTED_CREDENTIAL]"),
    ("credential", re.compile(r"\bAIza[0-9A-Za-z_-]{16,}\b"), "[REDACTED_CREDENTIAL]"),
    (
        "secret_assignment",
        re.compile(
            r"\b(?:api[_ -]?key|password|passwd|secret|access[_ -]?token|refresh[_ -]?token)"
            r"\s*[:=]\s*[^\s,;}]+",
            re.IGNORECASE,
        ),
        "[REDACTED_SECRET]",
    ),
    ("path", re.compile(r"(?<![\w.])/(?:etc|home|root|data|var|opt|srv|tmp|Users)(?:/[^\s`]+)+"), "[REDACTED_PATH]"),
    ("path", re.compile(r"\b[A-Za-z]:\\(?:[^\s`]+\\)*[^\s`]+"), "[REDACTED_PATH]"),
]


def find_secrets(value: object) -> list[str]:
    """Return the sorted, de-duplicated categories of secret/endpoint shapes in `value`."""
    text = str(value)
    found = {category for category, pattern, _ in _RULES if pattern.search(text)}
    return sorted(found)


def redact(value: object) -> str:
    """Mask endpoint- and credential-shaped values while retaining semantic context."""
    text = str(value)
    for _category, pattern, replacement in _RULES:
        text = pattern.sub(replacement, text)
    return text
