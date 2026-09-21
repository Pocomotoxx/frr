# Closure Scope Record Schema

The enforced field set and the `assertion_kind`, `closure_scope`, and
`assurance_level` enums are defined once in `closure-scope-record.schema.json`,
the single source `scripts/validate_closure_scope.py` reads. This prose documents
intent and rules and does not restate those lists, so the two cannot drift.

## Purpose

Define an append-only record that binds a claim of *non-resolution* — "this is
open / unresolved" or "this is new" — to the exact scope actually examined. The
record carries a `record_type` of `closure-scope-record`. It stops the most common
overclaim: silently turning "the current reasoning did not resolve it" into "it is
an established open problem", or "I did not find it in a search" into "it is novel".

It enforces the *shape and scope* of such a claim; it does not prove the claim.

## Enforced fields

The record enforces `record_type`, `claim_ref`, `assertion_kind`, `closure_scope`,
`basis_ref`, and `assurance_level`, and adds `field_evidence_ref` when
`closure_scope` is `ESTABLISHED_OPEN`. `claim_ref` locates the assertion;
`basis_ref` locates what was actually examined (the reasoning, method, or search
that grounds the scope).

## Shape

```json
{
  "record_type": "closure-scope-record",
  "claim_ref": "locator of the open/novel assertion",
  "assertion_kind": "UNRESOLVED|NOVEL",
  "closure_scope": "OPEN_IN_INQUIRY|OPEN_UNDER_METHOD|UNLOCATED_IN_SEARCH|ESTABLISHED_OPEN",
  "basis_ref": "what was actually examined (reasoning / method / search routes)",
  "field_evidence_ref": "community-level evidence (required when ESTABLISHED_OPEN)",
  "assurance_level": "DECLARED|UNVERIFIABLE"
}
```

## Calibrated meanings of "open"

- `OPEN_IN_INQUIRY` — the present reasoning has not resolved it.
- `OPEN_UNDER_METHOD` — the current construction or proof technique does not decide it.
- `UNLOCATED_IN_SEARCH` — no match was found under the search routes actually used.
- `ESTABLISHED_OPEN` — reliable field-level evidence shows the community recognizes
  it as unresolved.

## Rules (enforced by the validator)

- `basis_ref` must be a non-empty string; a scope claim without a stated basis is
  not admissible.
- A `NOVEL` `assertion_kind` requires `closure_scope` `ESTABLISHED_OPEN`: absence
  from a search is not novelty. Novelty rests on field-level evidence, never on
  `UNLOCATED_IN_SEARCH` or a merely unresolved inquiry.
- `ESTABLISHED_OPEN` requires a non-empty `field_evidence_ref`.
- `assurance_level` is `DECLARED` or `UNVERIFIABLE`, never `VERIFIED`.

The validator checks this record shape and these invariants only. It does not
mechanically prevent a later record from silently upgrading one scope to another;
that non-upgrade discipline lives in the policy and in review. Absence of a proof
is not a disproof, and absence from a search is not novelty.
