# Record Hygiene

FRR records are **metadata**. They pin a load-bearing claim to its shape and its
evidence *by reference*: a `claim_ref`, an `evidence_ref`, a `basis_ref`, a digest,
a locator. They do not carry the raw material — not the document text, not a live
endpoint, not a credential, not an absolute filesystem path. A record is a handle on
evidence, not a copy of it.

## Why

A record that embeds raw content or a secret stops being a safe, portable metadata
object. It leaks credentials wherever the record travels, it bloats, and it blurs
the line the records layer exists to keep: the claim and its evidence are separate,
and the record names the evidence rather than becoming it. This is the same
discipline that keeps a verdict's `evidence_ref` pointing *at* evidence, and that
lets a source or basis be cited without being reproduced.

## The discipline

For every field of a record, prefer a reference to the thing over the thing:

- an **endpoint** → a source id or a digest, not a live `https://…` URL;
- a **credential** → never; a record never carries an API key, bearer token, or
  secret assignment;
- a **path** → a repository-relative locator, not an absolute `/home/…` or `C:\…`
  path;
- **raw content** → a hash or a pinpoint, not the pasted text.

## The checkable form

`scripts/redaction.py` provides a deterministic `find_secrets` (which categories of
credential/endpoint/path a string carries) and `redact` (masking them while keeping
semantic context). `scripts/validate_record_hygiene.py` walks any record and fails
on a secret-shaped value in any field. Run it on a record before persisting it:

```bash
python scripts/validate_record_hygiene.py RECORD.json
```

A clean result proves no secret-shaped value was found — not that the record's
references are correct. Hygiene is necessary, not sufficient.

## Lineage

Adapted from the redaction discipline of the PhyAgentOS embodied-agent OS, which
redacts credentials, endpoints, and paths from persisted experience while retaining
semantic context.
