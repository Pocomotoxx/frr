# Composite Decision Record Schema

The enforced field set and the `combination`, `composite_level`, and `level` enums
are defined once in `composite-decision-record.schema.json`, the single source
`scripts/validate_composite_decision.py` reads. This prose documents intent and rules
and does not restate those lists, so the two cannot drift.

## Purpose

Define an append-only record that keeps a *composite judgment* honest by refusing to
collapse several independent factors into one holistic verdict. The record carries a
`record_type` of `composite-decision-record`. Instead of rating something in one
opaque pass, it names the factors, judges each on its own, and combines them by an
explicit, inspectable rule — so a shift in priorities is a change to the rule, not a
re-argued judgment.

## Levels are qualitative, not numbers

Each `level` and the `composite_level` are qualitative — `LOW`, `MEDIUM`, `HIGH` —
not calibrated numbers. A `weight` (used only under `WEIGHTED` combination) is a
declared design coefficient the author chooses, not a probability: it says how much a
dimension counts, and you change it deliberately.

## Enforced fields

The record enforces `record_type`, `decision_ref`, `dimensions`, `combination`,
`composite_level`, and `assurance_level`. `decision_ref` locates the composite
judgment; `dimensions` is a list of at least two atomic factors, each enforcing a
named `dimension` and its `level`, plus a positive `weight` when the `combination`
is `WEIGHTED`.

## Shape

```json
{
  "record_type": "composite-decision-record",
  "decision_ref": "locator of the composite judgment",
  "dimensions": [
    { "dimension": "market size", "level": "HIGH" },
    { "dimension": "technical feasibility", "level": "MEDIUM" },
    { "dimension": "differentiation", "level": "LOW" }
  ],
  "combination": "MIN|MAX|WEIGHTED",
  "composite_level": "LOW|MEDIUM|HIGH",
  "assurance_level": "DECLARED|UNVERIFIABLE"
}
```

## Rules (enforced by the validator)

- `dimensions` must contain at least two entries: a decomposition of one factor is
  not a decomposition. Each has a non-empty `dimension` name and a valid `level`.
- `combination` is `MIN`, `MAX`, or `WEIGHTED`, and it fixes how `composite_level`
  relates to the dimension levels:
  - `MIN` — the composite is the *weakest link*: `composite_level` equals the lowest
    dimension level.
  - `MAX` — the composite equals the highest dimension level.
  - `WEIGHTED` — every dimension must carry a positive `weight`, and `composite_level`
    must lie within the range of the dimension levels: a weighted combination cannot
    return a result outside the inputs it combines.
- `assurance_level` is `DECLARED` or `UNVERIFIABLE`, never `VERIFIED`.

The validator checks this record shape and these invariants only. It does not judge
whether each dimension level is the right reading of the world, only that the
composite is decomposed into atomic factors and combined by the declared rule.

## Lineage

Adapts TypeSafe/Jev's "atomic questions, composed in code" discipline. Complements
the Compression Fidelity pass: where that tests whether collapsing many things into
one erased a distinction, this refuses the collapse up front and keeps the
combination explicit. See `passes/COMPOSITE_DECISION.md`.
