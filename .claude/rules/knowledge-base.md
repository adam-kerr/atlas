# Knowledge-base maintenance

The Atlas knowledge base is product infrastructure. It records stable concepts,
workflows, contracts, and failure patterns for maintainers and future retrieval.
Read `knowledge/_meta/maintenance-guide.md` before changing it.

## Structure

```text
knowledge/
├── entities/         # What is this component or concept?
├── guides/           # How does this workflow operate?
├── troubleshooting/ # What should I check when it fails?
├── contracts/        # Exact machine-facing interfaces and values
└── _meta/            # Standards, glossary, and maintenance guidance
```

## Update triggers

| Change | Required knowledge update |
| --- | --- |
| Configuration model or default | Configuration guide and relevant contract |
| CLI command or argument | CLI guide and command contract |
| Model, voice, or integration interface | Relevant entity and architecture guide |
| Provider adapter | Provider guide or entity |
| New user workflow | Create or update a guide |
| New recurring failure | Add a troubleshooting runbook |
| Exact enum, schema, or command surface | Update the canonical contract |

## Rules

- Add `tags` and `synonyms` frontmatter to searchable documents.
- Keep exact values in contracts; link to them instead of duplicating them in prose.
- Do not include source line numbers, secrets, or transient incident details.
- Prefer cross-links over repeated explanations.
- Keep every file listed in its section index and in `knowledge/INDEX.md`.
- Verify links and indexes after every knowledge-base change.
