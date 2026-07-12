---
tags: [contract, cli, commands]
synonyms: [command line, atlas commands]
---

# CLI contract

```text
atlas doctor [--config PATH]
atlas ask PROMPT [--config PATH]
```

- `doctor` validates configuration and reports provider selections.
- `ask` sends one non-empty text request through the configured language model
  and prints the plain-text response.

Both commands default to `config/atlas.yaml`. The executable source of truth is
`src/atlas/cli.py`.
