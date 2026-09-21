# Field Change Record Schema

The enforced field set, the `field_effect` and `assurance_level` enums, and the
`channel` vocabulary are defined once in `field-change-record.schema.json`, the
single source `scripts/validate_field_change.py` reads. This prose documents
intent and rules and does not restate those lists, so the two cannot drift.

## Purpose

Define an append-only record that inspects, for a consequential action, not only
the object it changed but the **field** it may have changed behind itself — the
later observations, datasets, retrieval stores, users, incentives, or admissible
actions that subsequent work will encounter. An action may leave a wake even when
the acting system is reset. The record carries a `record_type` of
`field-change-record`. It enforces the *shape* of that inspection; it does not
prove what the action actually did.

## Enforced fields

The record enforces `record_type`, `action_ref`, `boundary`, `target_effect`,
`field_effect`, `field_channels`, and `assurance_level`, and adds `wake_ref` when
`field_effect` is `OBSERVED`. `action_ref` locates the consequential action;
`boundary` states the bounded field inspected; `target_effect` is the intended,
direct effect, kept separate from the field effect.

## Shape

```json
{
  "record_type": "field-change-record",
  "action_ref": "locator of the consequential action or change",
  "boundary": "the explicit, bounded field inspected",
  "target_effect": "the intended, direct effect of the action",
  "field_effect": "NONE_OBSERVED|OBSERVED|UNVERIFIABLE",
  "field_channels": ["OBSERVATIONS", "DATASET", "RETRIEVAL_STORE", "USERS", "INCENTIVES", "ADMISSIBLE_ACTIONS", "INSTRUMENTS"],
  "wake_ref": "description of the observed field change (required when field_effect is OBSERVED)",
  "assurance_level": "DECLARED|UNVERIFIABLE"
}
```

## Rules (enforced by the validator)

- `action_ref`, `boundary`, and `target_effect` must be non-empty strings. The
  `boundary` must be explicit: do not invoke an indefinitely large environment to
  make every consequence unfalsifiable.
- `field_channels` must be a non-empty list drawn from the `channel` vocabulary —
  the channels actually inspected. `NONE_OBSERVED` is only meaningful once
  channels have been looked at, within the stated boundary.
- `field_effect` `OBSERVED` requires a non-empty `wake_ref` naming the observed
  field change.
- `assurance_level` is `DECLARED` or `UNVERIFIABLE`, never `VERIFIED`.

The validator checks this record shape and these invariants only. A local
`target_effect` success does not imply `NONE_OBSERVED`; a missing wake is
`NONE_OBSERVED` within the stated boundary, not an absolute absence.
