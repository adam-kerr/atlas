---
tags: [entity, assistant, llm, tools]
synonyms: [reasoning layer, orchestration layer]
---

# Assistant layer

The assistant layer turns text requests into text responses. It owns language
model interfaces, conversation, planning, memory, and tool orchestration.

Provider-neutral protocols belong in `src/atlas/assistant/`; vendor adapters
remain below `src/atlas/assistant/providers/`. The layer must not depend on audio
hardware or expose provider response objects to callers.

See [Text-first assistant](../guides/text-first-assistant.md).
