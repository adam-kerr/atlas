---
tags: [troubleshooting, openai, authentication]
synonyms: [missing api key, unauthorized model request]
---

# OpenAI authentication fails

## Symptoms

The text assistant reports a missing or rejected OpenAI API key.

## Diagnosis

Confirm `OPENAI_API_KEY` is present in the Atlas process environment without
printing its value. Confirm the configured provider is `openai` and the model is
available to the API project.

## Resolution and verification

Set a valid project API key through the environment or deployment secret store,
then run a small `atlas ask` request. Never write the key into YAML or commit it.
