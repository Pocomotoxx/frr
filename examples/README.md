# Worked Examples

One validated record per pass. Each file passes its validator (checked by
`scripts/tests/test_examples.py`), so these are real fixtures, not prose. They show
the shape a load-bearing claim takes — and, deliberately, that a passing record can
still say the claim is *not* faithful, *not* corroborated, or *has* a wake.

Run any one:

```bash
python scripts/validate_compression_fidelity.py examples/compression-fidelity.example.json
```

## The four records

- **`compression-fidelity.example.json`** — a claim that two coarse-grained Markov
  histories are one effective state. A probe applies a macro-intervention; the two
  separate, so the erased distinction (control-relevant behavior) returned. The
  `verdict` is `NEEDS_REPAIR`, not `FAITHFUL` — the honest outcome. This is the FRR
  point that predictive closure is not control: the states agreed on prediction and
  diverged under intervention.

- **`closure-scope.example.json`** — a contraction bound the current technique does
  not decide. Scope is `OPEN_UNDER_METHOD` with a stated basis, not
  `ESTABLISHED_OPEN`: the method's silence is not a claim about the community's
  state of knowledge, and it is not a disproof.

- **`field-change.example.json`** — retraining a recommender on click logs. The
  target effect (click-through up) is real, and so is a `wake_ref`: a feedback loop
  that reshapes later slates. `field_effect` is `OBSERVED` within an explicit
  boundary — a local success with a named wake.

- **`source-convergence.example.json`** — three sources agree on a criterion, but
  all inherit one 2019 benchmark. `convergence` is `SHARED_ORIGIN` and
  `strengthens_claim` is `false`: agreement here is an echo chamber, not
  corroboration.

- **`closure-restraint.example.json`** — a conclusion that "the reorganization
  caused the employee uncertainty", drawn from four adjacent facts. The record names
  its licensing burden and declares the `imposed_structure` (`CAUSAL`, `NARRATIVE`)
  it added — and its `provenance_refs` say honestly that the causation is imposed
  and unsourced. The conclusion is not forbidden; the smuggling is surfaced.

## What a passing record proves

Only that the check was posed and is internally consistent. Assurance stays at
`DECLARED`; the world has not been consulted. That is the whole discipline: the
claim is admitted for what it is, at the scope actually examined, and no further.
