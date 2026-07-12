---
paths:
  - "src/**"
  - "config/**"
  - "docker-compose.yml"
---

# Security

- Never commit API keys, tokens, credentials, recordings, or user transcripts.
- Read secrets from environment variables or a secret manager.
- Never log prompts, model responses, or raw audio at INFO level or above.
- Do not include secrets in exception messages or shell command strings.
- Treat model output and integration data as untrusted input.
- Require explicit approval before tools perform external writes or physical actions.
- Keep provider-specific credentials and clients inside their adapter boundary.
