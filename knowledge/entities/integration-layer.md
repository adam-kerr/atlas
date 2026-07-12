---
tags: [entity, integrations, tools]
synonyms: [capabilities, external services]
---

# Integration layer

The integration layer exposes capabilities such as weather, calendar, and Home
Assistant through provider-neutral tool interfaces. Credentials, HTTP clients,
and vendor-specific types remain inside each adapter.

Integrations do not decide when they run; the assistant layer owns selection and
approval policy.
