---
paths:
  - "src/atlas/**"
  - "docs/**"
---

# Architecture

- Voice handles audio only and exchanges text with the assistant layer.
- Assistant owns conversation, reasoning, model interfaces, tools, and responses.
- Integrations expose provider-neutral capabilities to the assistant.
- Provider SDKs stay behind adapters; do not expose their response types across layers.
- Prefer ordinary typed Python interfaces and dependency injection over framework coupling.
- Keep dependency direction explicit and composition at application boundaries.

See `knowledge/guides/system-architecture.md` for the full system map.
