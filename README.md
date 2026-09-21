# FRR — Fluid Relational Reasoning (v0.4)

A Markdown-based, host-neutral reasoning system. A host reads these files and
reasons by them; the repository supplies the discipline, not the vendor. Start with
[START_HERE.md](START_HERE.md).

FRR treats ideas as **evolving relational objects** and reasons in a *field*, not a
pipeline. It has two layers:

- a **field** ([kernel/](kernel/KERNEL.md), [field/](field/)) — advisory reasoning
  discipline applied by judgment, with no mandatory order;
- **records** ([passes/](passes/README.md), [runtime/schemas/](runtime/schemas),
  [scripts/](scripts)) — the four moments where a load-bearing claim becomes
  checkable, each emitting an evidence-bound record whose assurance never reaches
  `VERIFIED`.

## Map

| Path | What |
|---|---|
| [`FRR.md`](FRR.md) | entry point, purpose, host neutrality |
| [`BOOT.md`](BOOT.md) | how a host loads the field |
| [`kernel/KERNEL.md`](kernel/KERNEL.md) | non-negotiable rules |
| [`field/`](field/) | compact seed, lenses, regimes, residual location, mathematical contact, naming the depth |
| [`passes/`](passes/README.md) | compression fidelity, closure scope, field change, source weave, crystallization |
| [`runtime/schemas/`](runtime/schemas) | the record schemas (JSON source + prose) |
| [`scripts/`](scripts) | validators and tests |
| [`docs/LINEAGE.md`](docs/LINEAGE.md) | v0.3 → v0.4 lineage |

## Validators

Python 3.11+, standard library only. No vendor SDK, no network.

```bash
python -m unittest discover -s scripts/tests
python scripts/validate_compression_fidelity.py RECORD.json
```

## Provenance

FRR v0.4 originates as a public reasoning seed; this repository is a structured,
navigable rendering with a checkable records layer. See [NOTICE](NOTICE).

## Not a promise of final ground

FRR helps an idea acquire enough form for its present purpose without taking away
its ability to keep changing, and it does not let prose stand in for evidence.
