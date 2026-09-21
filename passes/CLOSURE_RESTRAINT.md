# Pass: Closure Restraint

**When:** a response reaches a conclusion, a summary, or any closure that ends the
inquiry with a settled interpretation.

**Principle.** FRR's kernel licenses descent toward a conclusion only relative to a
declared burden, and it warns that a model's structural gravity will impose causal,
temporal, hierarchical, or narrative structure on inputs that do not contain it.
A closure is restrained when it is licensed by a burden and owns the structure it
added.

**The move.** Before letting a conclusion stand, name the `burden_ref` that
licenses it — a contradiction to resolve, a decision to make, a construction to
complete, an error to repair. A no-pressure state is allowed, but a conclusion
drawn from none is premature. Then declare the `imposed_structure`: what causal,
temporal, hierarchical, or narrative structure the conclusion added *beyond* the
sources. For anything added, state its provenance — the source that carries it, or
an explicit note that it is imposed and unsourced. Naming imposed structure is not
forbidden; hiding it is.

**Record.** Emit a `closure-restraint-record`
(`runtime/schemas/closure-restraint-record.schema.md`) and validate it with
`scripts/validate_closure_restraint.py`. A non-empty `imposed_structure` requires
`provenance_refs`; assurance never reaches `VERIFIED`.

**Boundary.** A passing record proves the closure was posed against a burden and its
imposed structure declared. It does not prove the conclusion is true, and it does
not forbid a conclusion — it forbids an *unlicensed, structure-smuggling* one.

**Lineage.** This pass adapts the anti-closure and structure-sealing insight of the
CSIR / RICC representation-isolation proposal — that fragmented input is silently
rebuilt into causal and narrative systems — to FRR's evaluative form. FRR does not
strip structure from inputs (that is a runtime transformer's job, not a reasoning
discipline); it makes a reasoner *own* the structure a conclusion imposes. See
`field/IMPOSED_STRUCTURE.md`.
