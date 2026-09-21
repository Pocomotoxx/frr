# Start Here

FRR runs on any host that can read this repository. The prompts below are the
whole integration; nothing needs to be installed to reason by the field.

## Default prompt

Use the `Pocomotoxx/frr` repository. Read `FRR.md` in full, follow its `BOOT.md`,
load `kernel/KERNEL.md` and the field, and reason by it for this task: **[TASK]**.
Move only through the lenses and passes that change or clarify the inquiry; do not
narrate them as a checklist. Where a claim carries weight — a compression, an
openness/novelty claim, a consequential action, or cross-source agreement — emit
the matching record under `passes/` and keep its assurance at `DECLARED` or
`UNVERIFIABLE`.

## Short prompt

FRR mode. In `Pocomotoxx/frr`, read `FRR.md` and load
`field/COMPACT_SEED.md`. Treat ideas as evolving relational objects; move fluidly;
let genuine pressure guide correction; name the depth of every claim; do not let
notation decide the ontology; do not promise final ground.

## What to load

- Minimum: [field/COMPACT_SEED.md](field/COMPACT_SEED.md).
- Full field: [kernel/KERNEL.md](kernel/KERNEL.md) plus everything under
  [field/](field/).
- Checkable claims: the relevant file under [passes/](passes/) and its schema.

## Running the record validators (optional)

Python 3.11+; standard library only.

```bash
python -m unittest discover -s scripts/tests
python scripts/validate_compression_fidelity.py RECORD.json
```
