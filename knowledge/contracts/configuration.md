---
tags: [contract, configuration]
synonyms: [settings schema, yaml keys]
---

# Configuration contract

Environment overrides use `ATLAS_<SECTION>__<FIELD>`.

| Section | Field | Default |
| --- | --- | --- |
| `voice` | `wake_word` | `atlas` |
| `voice` | `stt_provider` | `whisper` |
| `voice` | `tts_provider` | `piper` |
| `llm` | `provider` | `openai` |
| `llm` | `model` | `gpt-5.6-luna` |
| `llm` | `reasoning_effort` | `none` |
| `llm` | `verbosity` | `low` |
| `llm` | `max_output_tokens` | `300` |
| `llm` | `timeout_seconds` | `30` |
| `llm` | `max_retries` | `1` |
| `assistant` | `personality` | `concise` |
| `integrations` | `weather` | `false` |
| `integrations` | `calendar` | `false` |
| `integrations` | `home_assistant` | `false` |
| `logging` | `level` | `INFO` |
| `logging` | `format` | `json` |

The executable source of truth is `src/atlas/config/models.py`.
