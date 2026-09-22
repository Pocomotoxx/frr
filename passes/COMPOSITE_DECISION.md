# Pass: Composite Decision

**When:** a judgment rests on several independent factors and is about to be delivered
as one overall rating, score, or call — "rate this pitch", "how strong is this
candidate", "is this ready".

**Principle.** Do not collapse a multi-factor judgment into one opaque pass. Name the
factors, judge each on its own, and combine them by an explicit, inspectable rule.
Then a shift in priorities is a change to the rule, not a re-argued verdict, and a
weak factor cannot be quietly averaged away. This is the constructive companion to
the Compression Fidelity pass: rather than collapsing many into one and testing
afterwards whether a distinction was lost, this refuses the collapse up front.

**The move.** State the `decision_ref`, then the `dimensions` — at least two atomic
factors, each with a name and a qualitative `level` (`LOW`, `MEDIUM`, `HIGH`). Choose
a `combination`: `MIN` when the whole is only as strong as its weakest link, `MAX`
when any factor suffices, or `WEIGHTED` when the factors count differently — each then
carries a positive `weight`, a declared design coefficient you change deliberately.
Read the `composite_level` off the rule, not off a gut feeling.

**Record.** Emit a `composite-decision-record`
(`runtime/schemas/composite-decision-record.schema.md`) and validate it with
`scripts/validate_composite_decision.py`. `MIN`/`MAX` fix the composite to the extreme
level; `WEIGHTED` keeps it within the range of the dimension levels; assurance never
reaches `VERIFIED`.

**Boundary.** A passing record proves the judgment was decomposed and combined by the
declared rule — not that each dimension level is the right reading of the world. The
weights are a stated policy, not a measurement.

**Lineage.** This pass adapts TypeSafe/Jev's "atomic questions, composed in code"
discipline — decompose a judgment into well-scoped questions and combine the results
with an explicit rule instead of one holistic prompt. TypeSafe is a commercial model
lab, a different tradition landing on the same principle, so the agreement is
independent, not inherited (a source-convergence `INDEPENDENT`). FRR imports the
discipline, not the model: levels stay qualitative, never a calibrated number.
