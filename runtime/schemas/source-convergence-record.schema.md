# Source Convergence Record Schema

The enforced field set and the `convergence` and `assurance_level` enums are
defined once in `source-convergence-record.schema.json`, the single source
`scripts/validate_source_convergence.py` reads. This prose documents intent and
rules and does not restate those lists, so the two cannot drift.

## Purpose

Define an append-only record that binds a claim of *source agreement* to whether
the agreeing sources are genuinely independent. The record carries a `record_type`
of `source-convergence-record`. Several sources using the same phrase may inherit
one origin, benchmark, or assumption; agreement becomes evidence only when the
routes are independent. The record stops an echo chamber from being read as
corroboration.

## Enforced fields

The record enforces `record_type`, `claim_ref`, `source_refs`, `convergence`,
`strengthens_claim`, and `assurance_level`, and adds `shared_origin_ref` when
`convergence` is `SHARED_ORIGIN`. `claim_ref` locates the claim the sources are
said to support; `source_refs` lists the agreeing sources; `strengthens_claim`
states whether this agreement is offered as corroboration.

## Shape

```json
{
  "record_type": "source-convergence-record",
  "claim_ref": "locator of the claim the sources support",
  "source_refs": ["source-1", "source-2"],
  "convergence": "INDEPENDENT|SHARED_ORIGIN|UNKNOWN",
  "shared_origin_ref": "the shared origin/benchmark/assumption (required when SHARED_ORIGIN)",
  "strengthens_claim": false,
  "assurance_level": "DECLARED|UNVERIFIABLE"
}
```

## Rules (enforced by the validator)

- `source_refs` must contain at least two distinct, non-empty entries;
  convergence needs more than one source.
- `strengthens_claim` must be a boolean. When it is `true`, `convergence` must be
  `INDEPENDENT`: only independent agreement corroborates. `SHARED_ORIGIN` or
  `UNKNOWN` agreement is not corroboration.
- `SHARED_ORIGIN` requires a non-empty `shared_origin_ref` naming the inherited
  origin, benchmark, or assumption.
- `assurance_level` is `DECLARED` or `UNVERIFIABLE`, never `VERIFIED`.

The validator checks this record shape and these invariants only. It does not
prove the sources are independent, only that the claim of agreement is scoped to a
stated independence status and internally consistent.
