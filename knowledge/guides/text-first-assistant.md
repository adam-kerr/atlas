---
tags: [guide, assistant, cli, openai]
synonyms: [ask command, text mode, model request]
---

# Text-first assistant

The text-first path proves the request and response boundary before voice or
graph orchestration is added.

```text
CLI prompt -> AssistantService -> LanguageModel protocol -> provider adapter
           <- plain text response <-
```

The OpenAI adapter uses the Responses API and reads credentials from the
environment through the official SDK. Core tests inject a fake language model
and never require network access.

`atlas ask` is stateless. `atlas chat` continues turns with the prior response
identifier while resending Atlas instructions on every turn. Expected provider
failures become concise CLI errors. Successful requests emit token usage as
structured metadata without logging prompts or responses.

See the [CLI contract](../contracts/cli.md) for exact usage.
