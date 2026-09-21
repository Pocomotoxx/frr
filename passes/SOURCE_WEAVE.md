# Pass: Source Weave

**When:** the evolving intuition approaches established knowledge, and outside
sources could change its form, lineage, or credibility — especially when
cross-source agreement is offered as support.

**Principle.** Search is not a neutral window onto literature; every query is an
aperture. Do not let the current formulation be the only wording used to search for
its ancestry. Count convergence only when the routes are genuinely independent:
several sources using one phrase may inherit one origin, benchmark, or assumption.

**The move.** Translate the idea into search roles, not synonyms — object, function,
failure, repair, timescale, genealogy, rival formulation, domain translation. Use
four fluid movements: validate the current formulation; search by
function/failure/repair; move genealogically through references and ancestors;
search adversarially for alternatives and limits. A new movement counts only if it
changes the dependency structure of the search. Before a novelty claim, require at
least a direct-formulation, a function/failure, a genealogy, and a rival-formulation
search. Absence from search results is not absence from the literature.

**Record.** When cross-source agreement is offered as corroboration, emit a
`source-convergence-record` (`runtime/schemas/source-convergence-record.schema.md`)
and validate it with `scripts/validate_source_convergence.py`. Agreement
strengthens a claim only when `convergence` is `INDEPENDENT`; a `SHARED_ORIGIN`
names the inherited origin; assurance never reaches `VERIFIED`.

**Boundary.** `UNKNOWN` and `SHARED_ORIGIN` are honest states in which agreement
does not yet strengthen the claim; they never upgrade to `INDEPENDENT` without a
separate determination.
