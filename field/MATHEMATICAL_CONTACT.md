# Mathematical Contact

When an intuition begins acquiring mathematical form, identify what work the
mathematics performs. Six kinds of work (numbers, algebra, geometry, probability,
analysis, dynamics) — not an exhaustive or canonical division:

1. **Quantity** — counting, magnitude, dimension, multiplicity, scale, measurement.
2. **Relation** — operations, equivalence, composition, symmetry, order, algebraic
   constraint.
3. **Shape** — space, neighborhood, boundary, fibre, basin, topology, curvature.
4. **Uncertainty** — distributions, likelihoods, stochastic transitions, entropy,
   inference.
5. **Limit** — convergence, continuity, approximation, asymptotics, stability,
   singular behavior.
6. **Evolution** — trajectories, recurrences, flows, state transitions,
   bifurcations, control.

Do not require every idea to use all six. Use them to determine what kind of formal
claim is being attempted. **Do not let mathematics doing one job silently perform
another.** For example: a path count is not automatically a probability; an
equivalence class is not automatically a physical basin; a geometrical minimum is
not automatically a dynamical attractor; an asymptotic limit is not necessarily
reached in finite time; recurrence is not convergence; visual rotation is not
rotational dynamics; reversing orientation is not reversing physical causation;
compressing states into one representation does not prove they physically merged;
predictive closure is not causal power; an observationally sufficient state is not
sufficient for control.

## Forms also run both ways

Measure a known structure, or ask what structures could have produced a
measurement. Compose operations forward, or factor a completed relation. Derive
global geometry from local constraints, or infer constraints from a global form.
Propagate a distribution forward, or infer hidden causes from observations.
Determine asymptotics from a process, or infer governing behavior from asymptotics.
Predict later states, or reconstruct the family of histories compatible with the
present. Backward inference generally yields a set or distribution of antecedents,
not a unique past, unless the transformation is demonstrably invertible.

## Domain-relative formalization

A form that travels across domains should not carry one domain's substance into
another. Let each domain supply its own objects, admissible transformations,
equivalence criteria, observables, interventions, measures, spatial structure, and
temporal rules. A cross-domain form preserves relations while allowing its material
interpretation to change. A useful abstract pattern —
`multiplicity → relational organization → effective unity → further movement` —
may be trajectories in one domain and histories, proofs, computations,
configurations, interventions, or distributions in another. Do not conclude they
are physically identical because one silhouette organizes them.

## Effective states and the weave test

When several histories or configurations become one state, identify the criterion
producing that unity. With `b_D : ℋ_D → ℬ_D` mapping histories to behaviors,
`h₁ ∼_D h₂ ⇔ b_D(h₁) = b_D(h₂)`, effective states `𝒮_D = ℋ_D / ∼_D`, and quotient
map `q_D : ℋ_D → 𝒮_D`, the fibre `q_D⁻¹(s)` contains everything `s` represents — a
set, a predecessor tree, a basin, a manifold, a recurrent component, a family of
proofs, or observationally indistinguishable configurations. Where continued
transformations matter, test whether the equivalence is a **congruence**:
`h₁ ∼_D h₂ ⇒ T_a(h₁) ∼_D T_a(h₂)` for every relevant `T_a`. If it fails, the
compression may erase distinctions later behavior needs.

A pattern in several domains is not yet a common mechanism. Compare two routes —
construct-then-translate vs. translate-then-construct, `F_S ∘ q_D ≅ q_E ∘ F_H`
("point, then translate ≟ translate, then point"). Exact equality may be too
strict; the standard may be isomorphism, behavioral equivalence, approximation
within a tolerance, or preservation of a chosen invariant. A disagreement reveals
the boundary of the abstraction. When such a compression carries weight, make it
checkable: emit a **compression-fidelity record** (`passes/COMPRESSION_FIDELITY.md`).
