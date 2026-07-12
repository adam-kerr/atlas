---
tags: [guide, configuration, yaml, environment]
synonyms: [settings, atlas config, environment overrides]
---

# Configuration

Atlas loads YAML from `config/atlas.yaml` by default, applies nested `ATLAS_`
environment overrides, then validates the merged data with strict Pydantic
models. Double underscores separate nested keys.

Use `atlas doctor` after editing configuration. Unknown keys and invalid values
fail validation rather than being ignored.

Exact keys and defaults live in the [configuration contract](../contracts/configuration.md).
