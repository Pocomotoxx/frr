# Verdict Record Schema

The enforced field set, the `verdict` and `assurance_level` enums, and the
criterion `status` enum are defined once in `verdict-record.schema.json`, the
single source `scripts/validate_verdict.py` reads. This prose documents intent and
rules and does not restate those lists, so the two cannot drift.

## Purpose

Define an append-only record for a claim that a goal was achieved or a task
succeeded — including a claim that a self-improvement improved something. Evidence
comes before the verdict: the verdict is decided against **declared success
criteria**, each with its own status and, when passing, its own cited evidence.
Advisories and prose cannot replace a criterion or its evidence. The record carries
a `record_type` of `verdict-record`. It enforces the shape of that judgment; it does
not certify that the goal was truly met.

## Enforced fields

The record enforces `record_type`, `goal_ref`, `criteria`, `verdict`, and
`assurance_level`. Each entry of `criteria` enforces `criterion` and `status`, and
adds `evidence_ref` when `status` is `PASS`. `goal_ref` locates the goal the verdict
is about.

## Shape

```json
{
  "record_type": "verdict-record",
  "goal_ref": "locator of the goal or task the verdict is about",
  "criteria": [
    { "criterion": "a declared success criterion", "status": "PASS|FAIL|UNVERIFIABLE", "evidence_ref": "evidence locator (required when PASS)" }
  ],
  "verdict": "ACHIEVED|NOT_ACHIEVED|PARTIAL|UNVERIFIABLE",
  "assurance_level": "DECLARED|UNVERIFIABLE"
}
```

## Rules (enforced by the validator)

- `goal_ref` must be non-empty, and `criteria` must contain at least one criterion;
  a verdict with no declared criterion is not admissible.
- Each criterion has a `status` of `PASS`, `FAIL`, or `UNVERIFIABLE`. A `PASS`
  criterion requires a non-empty `evidence_ref`: a criterion cannot pass on an
  advisory or on prose, only on cited evidence.
- `verdict` `ACHIEVED` requires every criterion to be `PASS`. If any criterion is
  `FAIL` or `UNVERIFIABLE`, the verdict must be `NOT_ACHIEVED`, `PARTIAL`, or
  `UNVERIFIABLE` — not `ACHIEVED`.
- `assurance_level` is `DECLARED` or `UNVERIFIABLE`, never `VERIFIED`. A verdict is
  a reading of the evidence against the criteria, not execution-scope proof.

The validator checks this record shape and these invariants only. A passing record
proves the verdict was posed against declared, evidence-cited criteria — not that
the goal was truly achieved.

## Three records, kept separate

Following the source contract, keep **execution** (what ran), **evidence** (what was
observed), and **verdict** (whether each criterion is satisfied) as separate
concerns. This record is the *verdict*; its `evidence_ref` values point at evidence,
they do not contain it.
