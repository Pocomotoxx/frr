# Pass: Field Change

**When:** a consequential (writing or externally effectful) action.

**Principle.** Inspect not only the object the action changed but the field it may
have changed behind itself — later observations, datasets, retrieval stores, users,
incentives, or admissible actions. An action may leave a wake even when the acting
system is reset, and a local success can coexist with a harmful wake outside the
boundary originally measured.

**The move.** Name the action and an explicit boundary — do not invoke an
indefinitely large environment to make every consequence unfalsifiable. Keep the
target effect separate from the field effect. List the channels actually inspected.
Run it both ways: forward, what wake may this leave and who will encounter it;
backward, from a persistent effect, test whether resetting the present state,
history, probe, environment, or translation removes it.

**Record.** Emit a `field-change-record`
(`runtime/schemas/field-change-record.schema.md`) and validate it with
`scripts/validate_field_change.py`. An `OBSERVED` field effect names the `wake_ref`;
assurance never reaches `VERIFIED`.

**Boundary.** `NONE_OBSERVED` means no wake was observed over the named channels
within the stated boundary. It never upgrades to "the action had no field effect".
