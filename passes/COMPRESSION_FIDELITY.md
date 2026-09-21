# Pass: Compression Fidelity

**When:** an idea begins acting as a summary, category, node, equivalence class,
common structure, effective state, merge, or "same as".

**Principle.** A compression is faithful only to the extent that the distinctions
it erases remain irrelevant to the behavior, domain, horizon, and tolerance it
claims to preserve. Coherence without discriminative capacity may be collapse
rather than insight.

**The move.** State what behavior the compression preserves (prediction, an
observable, response to intervention, an invariant, a compositional relationship,
or a task). Run the **trivial-collapse test**: if merging everything into one class
would already satisfy the criterion, the criterion lacks discriminative pressure.
Seek two currently merged cases and change the pressure — extend trajectories,
change the horizon, compose a transformation, observe more finely, intervene, or
translate. If they separate, name exactly which erased distinction returned, and
repair the abstraction at the depth of failure (refine the partition, restore
history, enlarge the macro-dynamics, change the observable, restrict the horizon,
or abandon the claimed unity). Run it both ways: forward, what will it erase;
backward, from a failure of prediction or control, what smallest hidden distinction
would repair it.

**Record.** Emit a `compression-fidelity-record`
(`runtime/schemas/compression-fidelity-record.schema.md`) and validate it with
`scripts/validate_compression_fidelity.py`. `verdict` is `FAITHFUL` only when no
probe separated the merged cases; assurance never reaches `VERIFIED`.

**Boundary.** A passing record proves the fidelity test was posed and internally
consistent. It does not prove the compression preserves the world's behavior.
