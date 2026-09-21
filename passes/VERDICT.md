# Pass: Verdict

**When:** a response claims that a goal was achieved, a task succeeded, or a change
improved something — including a self-improvement claim.

**Principle.** Evidence comes before the verdict. A success claim is decided against
**declared success criteria**, each with its own status and, when passing, its own
cited evidence. An advisory or a fluent summary cannot replace a criterion or its
evidence, and a goal is not achieved unless every criterion passes. FRR's field
already holds that improvement is not greater confidence or elegance but doing one
real thing; this pass is where a success claim is pinned to that discipline.

**The move.** State the `goal_ref`, then the `criteria` — the success conditions the
goal is judged by. Give each a `status` (`PASS`, `FAIL`, `UNVERIFIABLE`); a `PASS`
must cite an `evidence_ref` that points at evidence, not at prose. Read the overall
`verdict` off the criteria: `ACHIEVED` only when all pass, otherwise
`NOT_ACHIEVED`, `PARTIAL`, or `UNVERIFIABLE`. Keep execution (what ran), evidence
(what was observed), and verdict (this record) as separate concerns.

**Record.** Emit a `verdict-record`
(`runtime/schemas/verdict-record.schema.md`) and validate it with
`scripts/validate_verdict.py`. A `PASS` criterion requires an `evidence_ref`;
`ACHIEVED` requires every criterion `PASS`; assurance never reaches `VERIFIED`.

**Boundary.** A passing record proves the verdict was posed against declared,
evidence-cited criteria — not that the goal was truly met. A verdict is a reading of
the evidence, never execution-scope proof.

**Lineage.** This pass adapts the "evidence before verdict" contract of the
PhyAgentOS embodied-agent OS — execution / evidence / verdict kept separate, and
advisories that cannot replace criteria or evidence — to FRR's evaluative form. The
agreement between a robotics agent OS and a reasoning discipline on this principle
is independent, not inherited (a source-convergence `INDEPENDENT`). FRR does not run
tasks or capture sensor evidence; it makes a success claim *own* its criteria and
their evidence.
