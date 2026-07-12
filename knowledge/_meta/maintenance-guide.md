---
tags: [meta, knowledge-base, maintenance]
synonyms: [kb guide, documentation maintenance]
---

# Knowledge-base maintenance guide

## Authoring workflow

1. Identify the concept, workflow, failure pattern, or exact contract changed.
2. Update the canonical document; do not create a second source of truth.
3. Add cross-links from related documents.
4. Add new files to the section index and `knowledge/INDEX.md`.
5. Verify every relative link resolves and exact values match source code.

## Document types

- **Entity:** identity, responsibilities, boundaries, relationships, and lifecycle.
- **Guide:** goal, prerequisites, flow, decisions, and verification.
- **Troubleshooting:** symptoms, likely causes, diagnosis, resolution, verification.
- **Contract:** exact names, values, inputs, outputs, and compatibility requirements.

Copy the template in the appropriate directory for new documents.

## Retrieval metadata

Every searchable document starts with YAML frontmatter containing concise
`tags` and likely `synonyms`. Use stable domain terms, not temporary ticket names.

## Canonicality

Source code remains canonical for executable behavior. Contracts mirror exact
public surfaces. Human-oriented documents explain meaning and link to contracts.
