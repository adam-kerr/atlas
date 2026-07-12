---
tags: [troubleshooting, configuration, doctor]
synonyms: [validation error, invalid atlas yaml]
---

# Configuration validation fails

## Symptoms

`atlas doctor` exits with a Pydantic validation error.

## Diagnosis

Check the named field, then compare YAML and `ATLAS_` overrides with the
[configuration contract](../contracts/configuration.md). Environment values take
precedence over YAML and may be the source of an unexpected value.

## Resolution and verification

Correct or remove the invalid key or override, then rerun `atlas doctor`.
