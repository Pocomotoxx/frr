# Closure Restraint Record Schema

The enforced field set, the `assurance_level` enum, and the `structure` vocabulary
are defined once in `closure-restraint-record.schema.json`, the single source
`scripts/validate_closure_restraint.py` reads. This prose documents intent and
rules and does not restate those lists, so the two cannot drift.

## Purpose

Define an append-only record that restrains closure. FRR's kernel holds that
descent toward a conclusion is licensed only relative to a declared burden, and
that a model's structural gravity will impose causal, temporal, hierarchical, or
narrative structure on inputs that do not contain it. When a response reaches a
conclusion, this record binds that closure to its licensing burden and forces it
to declare what structure it added beyond the sources — and, for any it added,
where that structure came from. The record carries a `record_type` of
`closure-restraint-record`. It enforces the shape of that restraint; it does not
judge whether the conclusion is correct.

## Enforced fields

The record enforces `record_type`, `conclusion_ref`, `burden_ref`,
`imposed_structure`, and `assurance_level`, and adds `provenance_refs` when
`imposed_structure` is non-empty. `conclusion_ref` locates the closure under check;
`burden_ref` names the declared burden that licenses the descent.

## Shape

```json
{
  "record_type": "closure-restraint-record",
  "conclusion_ref": "locator of the conclusion / closure under check",
  "burden_ref": "the declared burden that licenses the descent (a contradiction, a decision, a construction, an error to repair)",
  "imposed_structure": ["CAUSAL", "TEMPORAL", "HIERARCHY", "NARRATIVE"],
  "provenance_refs": ["for each imposed structure: the source that carries it, or an explicit note that it is imposed and unsourced"],
  "assurance_level": "DECLARED|UNVERIFIABLE"
}
```

## Rules (enforced by the validator)

- `conclusion_ref` and `burden_ref` must be non-empty. A closure with no declared
  burden is premature: FRR permits a no-pressure state, but not a conclusion drawn
  from none.
- `imposed_structure` is a list drawn from the `structure` vocabulary (`CAUSAL`,
  `TEMPORAL`, `HIERARCHY`, `NARRATIVE`); an empty list means the conclusion added no
  structure beyond the sources.
- A non-empty `imposed_structure` requires a non-empty `provenance_refs`: any
  causal, temporal, hierarchical, or narrative structure the conclusion asserts must
  state where it came from. Naming it as imposed-and-unsourced is a valid
  provenance entry — it surfaces the smuggled structure for review rather than
  hiding it.
- `assurance_level` is `DECLARED` or `UNVERIFIABLE`, never `VERIFIED`.

The validator checks this record shape and these invariants only. A passing record
proves the closure was posed against a burden and its imposed structure declared,
not that the conclusion is true.
