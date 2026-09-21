# FRR Boot

## Purpose

Define how a host loads FRR. Loading FRR is not a state machine and does not run
a pipeline; it assembles the reasoning field so the host can move through it by
judgment. This file is deliberately light: FRR resists mandatory sequence.

## Load order

1. Read `FRR.md`, then this file.
2. Load `kernel/KERNEL.md` — the non-negotiable rules.
3. Load the field as the task needs it, not all at once:
   - `field/COMPACT_SEED.md` — the whole discipline in compact form.
   - `field/LENSES.md` — the five relational lenses, each run forward and backward.
   - `field/REGIMES.md` — open play, directed exploration, claim engineering.
   - `field/RESIDUAL.md` — semantic pressure, residuals, and residual location.
   - `field/MATHEMATICAL_CONTACT.md` — what work a formalization performs.
   - `field/NAMING_THE_DEPTH.md` — the depth ladder and claim/argument/mechanism
     separation.
4. When a claim begins to carry weight, load the matching file under `passes/` and
   emit its record.

## The one ordering rule FRR does keep

Order matters between operations even though no operation is mandatory:
`formalize ∘ explore ≠ explore ∘ formalize`, and similarly for searching, testing,
translating, and compressing. Formalizing or searching too early anchors the seed;
compressing before testing erases the distinction that would have changed the
outcome. Let the state of the inquiry and the user's intention select the next
move. Do not perform every named operation merely because it exists.

## Precision is local

Increase precision where a claim begins doing consequential work, without freezing
the rest of the field. Different branches may sit in different regimes at the same
time.

## Records are the only hard gate

The field is advisory. The four record types under `passes/` are the only places
FRR asks for a checkable artifact, and only when the corresponding claim is
actually made. A record's validator checks shape and internal consistency; it
never certifies the claim, and assurance never reaches `VERIFIED`.
