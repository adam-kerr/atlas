---
paths:
  - "src/**"
  - "scripts/**"
  - "tests/**"
---

# Coding conventions

- Target Python 3.12+ and use type hints for public and internal APIs.
- Use Pydantic for validated external configuration and data boundaries.
- Keep modules small, focused, and composable.
- Define provider-neutral `Protocol` interfaces before provider adapters.
- Inject network clients and collaborators so tests do not require external services.
- Reject invalid input at the closest boundary with specific errors.
- Use structured logging and `timed_operation` for significant operations.
- Do not add LangGraph until ordinary Python request, model, and tool seams require it.
