# Atlas repository guidance

Atlas is a modular, self-hosted Raspberry Pi voice assistant. Preserve the
boundaries between voice, assistant orchestration, and integrations.

Repository rules live in `.claude/rules/`:

- `architecture.md` — package boundaries and dependency direction
- `coding.md` — Python conventions and composition practices
- `testing.md` — required validation and test seams
- `security.md` — secrets, prompts, logging, and external calls
- `knowledge-base.md` — knowledge-base structure and maintenance triggers

Read `knowledge/README.md` before changing domain behavior. Update the relevant
knowledge document in the same change as the code it describes.
