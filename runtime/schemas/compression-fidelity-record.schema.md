# Compression Fidelity Record Schema

The enforced field set and the `preserved_behavior`, `trivial_collapse_check`,
`verdict`, `assurance_level`, and `applied_pressure` enums are defined once in
`compression-fidelity-record.schema.json`, the single source
`scripts/validate_compression_fidelity.py` reads. This prose documents intent and
rules and does not restate those lists, so the two cannot drift.

## Purpose

Define an append-only record that tests whether a **compression** — a summary, an
equivalence class, a merge, a "same as", a node, or any effective state that
represents many things as one — preserves the behavior it claims to preserve.
The record carries a `record_type` of `compression-fidelity-record`. It enforces
the *shape* of a fidelity test; it does not prove the compression is correct.

This adapts the Faithful Compression Pass to the FRR system's enforced-record model:
a compression claim may not stand on prose alone; it must carry a checkable
record whose assurance never reaches VERIFIED.

## Shape

```json
{
  "record_type": "compression-fidelity-record",
  "claim_ref": "locator of the compression/merge claim under test",
  "preserved_behavior": "PREDICTION|OBSERVABLE|INTERVENTION|INVARIANT|COMPOSITION|TASK",
  "scope": {
    "domain": "the domain within which fidelity is claimed",
    "horizon": "the horizon over which it is claimed",
    "tolerance": "the tolerance within which agreement counts"
  },
  "trivial_collapse_check": "PASS|FAIL",
  "probes": [
    {
      "case_a_ref": "one member currently merged by the compression",
      "case_b_ref": "another member currently merged by the compression",
      "applied_pressure": "LONGER_HORIZON|FINER_OBSERVATION|COMPOSITION|INTERVENTION|TRANSLATION",
      "separated": false,
      "returned_distinction": "named distinction that returned (required when separated is true)"
    }
  ],
  "verdict": "FAITHFUL|NEEDS_REPAIR|REJECTED",
  "assurance_level": "DECLARED|UNVERIFIABLE"
}
```

## Enforced fields

The record enforces `record_type`, `claim_ref`, `preserved_behavior`, `scope`,
`trivial_collapse_check`, `probes`, `verdict`, and `assurance_level`; the `scope`
object enforces `domain`, `horizon`, and `tolerance`; each entry of `probes`
enforces `case_a_ref`, `case_b_ref`, `applied_pressure`, and `separated`, and adds
`returned_distinction` when `separated` is true. The `claim_ref` locates the
compression under test.

## Rules (enforced by the validator)

- The `scope` object must fully specify `domain`, `horizon`, and `tolerance`;
  a compression is faithful only relative to a stated scope.
- `trivial_collapse_check` must be `PASS`. A `FAIL` means merging everything into
  one class would already satisfy the criterion, so the criterion lacks
  discriminative pressure and the compression is inadmissible.
- `probes` must be a non-empty list. Each probe pairs two currently merged members
  (`case_a_ref`, `case_b_ref`), applies one `applied_pressure`, and records whether
  they `separated`. A probe whose `separated` is true must name the
  `returned_distinction`.
- `verdict` is `FAITHFUL` only when no probe separated the merged cases. If any
  probe separated them, the erased distinction returned and the `verdict` must be
  `NEEDS_REPAIR` or `REJECTED`.
- `assurance_level` is `DECLARED` or `UNVERIFIABLE`; a fidelity test is a reading
  of the compression, never `VERIFIED` proof of its correctness.

The validator checks this record shape and these invariants only. A `PASS` proves
the test was posed and internally consistent; it does not prove that the
compression preserves the world's behavior.
