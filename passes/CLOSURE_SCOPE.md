# Pass: Closure Scope

**When:** a response asserts that a subject is open, unresolved, novel, or
unlocated.

**Principle.** Match every use of "open" to the exact scope actually examined.
Absence of a proof is not a disproof; absence from a search is not novelty.

**The move.** Bind the claim to what was actually examined, and pick the calibrated
scope: `OPEN_IN_INQUIRY` (the present reasoning has not resolved it),
`OPEN_UNDER_METHOD` (the current technique does not decide it),
`UNLOCATED_IN_SEARCH` (no match under the routes used), or `ESTABLISHED_OPEN`
(field-level evidence of community recognition). Novelty rests on field-level
evidence, never on absence from a search. Do not convert one scope into another
silently.

**Record.** Emit a `closure-scope-record`
(`runtime/schemas/closure-scope-record.schema.md`) and validate it with
`scripts/validate_closure_scope.py`. A `NOVEL` assertion requires `ESTABLISHED_OPEN`
with a `field_evidence_ref`; assurance never reaches `VERIFIED`.

**Boundary.** The record fixes one claim at one scope. The non-upgrade discipline —
one status never silently becomes a stronger one, and none becomes "false" — lives
in this pass and in review, not in the single-record validator.
