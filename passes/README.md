# Passes

The field is advisory. A **pass** is a moment where the field's discipline becomes
checkable: when a claim carries weight, the pass asks for a small, evidence-bound
**record** whose validator checks shape and internal consistency. A record's
assurance is `DECLARED` or `UNVERIFIABLE`, never `VERIFIED` — a passing validator
proves the check was posed, not that the world agrees.

Six passes carry a record; two are advisory-only. Activate a pass only when its
corresponding claim is actually made.

| Pass | When | Record |
|---|---|---|
| [Compression Fidelity](COMPRESSION_FIDELITY.md) | a summary / equivalence class / merge / "same as" / effective state | `compression-fidelity-record` |
| [Closure Scope](CLOSURE_SCOPE.md) | a claim that something is open / unresolved / novel | `closure-scope-record` |
| [Field Change](FIELD_CHANGE.md) | a consequential (writing or externally effectful) action | `field-change-record` |
| [Source Weave](SOURCE_WEAVE.md) | cross-source agreement offered as support | `source-convergence-record` |
| [Closure Restraint](CLOSURE_RESTRAINT.md) | a conclusion / summary / closure that ends the inquiry | `closure-restraint-record` |
| [Verdict](VERDICT.md) | a claim that a goal was achieved / a task succeeded / a change improved something | `verdict-record` |
| [Composite Decision](COMPOSITE_DECISION.md) | a multi-factor judgment delivered as one overall rating / score / call | `composite-decision-record` |
| [Crystallization](CRYSTALLIZATION.md) | a structure stabilizes as a definition/model/decision | advisory only |

Records live under `runtime/schemas/*.schema.{json,md}`; validators under
`scripts/validate_*.py`; tests under `scripts/tests/`. The JSON is the single
source the validator reads; the prose `.schema.md` documents intent.
