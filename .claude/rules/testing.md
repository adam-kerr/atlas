---
paths:
  - "src/**"
  - "tests/**"
---

# Testing

Run the full validation suite after code changes:

```bash
.venv/bin/ruff check .
.venv/bin/ruff format --check .
.venv/bin/mypy
.venv/bin/pytest
.venv/bin/atlas doctor
git diff --check
```

- Unit tests must cover success, invalid input, and provider failure boundaries.
- Use fakes for language models, integrations, audio, and other network/hardware seams.
- No unit test may require an API key, network connection, microphone, or Raspberry Pi.
- Add CLI composition tests for user-facing commands.
- Run live provider and hardware smoke tests separately and label them clearly.
