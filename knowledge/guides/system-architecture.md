---
tags: [guide, architecture, boundaries]
synonyms: [system design, layers]
---

# System architecture

Atlas is composed from three replaceable layers:

```text
voice text output -> assistant orchestration -> integration capabilities
voice playback   <- assistant response
```

Shared configuration and logging support all layers but do not contain domain
behavior. Application entry points compose concrete adapters with neutral
interfaces. See `docs/architecture.md` for the concise repository overview and
the entity documents for layer-specific responsibilities.
