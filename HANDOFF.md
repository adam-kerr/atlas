# Atlas development handoff

## Objective

Build Atlas, a modular, self-hosted Raspberry Pi voice assistant. The project
brief emphasizes three loosely coupled layers:

1. Voice: wake word, VAD, STT, TTS, and playback only.
2. Assistant: conversation, reasoning, planning, memory, tools, and responses.
3. Integrations: provider-neutral capabilities such as weather, calendar, and
   Home Assistant.

Maintainability is the guiding principle. Use Python 3.12+, type hints,
Pydantic, dependency injection, small modules, and composition.

## Repository and Git state

- Local repository: `/Users/adamkerr/dev/atlas`
- GitHub: `https://github.com/adam-kerr/atlas`
- Current branch: `init`
- Base branch: `main`
- `main` has not been modified or committed to.
- All foundation work is currently uncommitted on `init`.
- The requested outcome is a commit on `init` and a pull request targeting
  `main`; do not commit directly to `main`.

## Work completed

- Python package and build configuration in `pyproject.toml`
- Explicit `voice`, `assistant`, and `integrations` package boundaries
- Typed YAML configuration with nested `ATLAS_` environment overrides
- JSON/text logging and a reusable timing context manager
- Typer CLI with `atlas doctor`
- Unit tests for configuration and logging
- Dockerfile and Docker Compose entry point
- Make targets and bootstrap script
- Architecture documentation, README, and initial hardware BOM
- Local virtual environment at `.venv` (ignored by Git)

## Validation status

The following passed before the final CLI adjustment:

- `ruff check .`
- `ruff format --check .`
- `mypy`
- `pytest` — 5 tests passed

The first `atlas doctor` smoke test exposed Typer's single-command collapsing
behavior. An explicit callback was then added to `src/atlas/cli.py` so
`atlas doctor` remains a subcommand. Rerun the full checks now.

## Resume commands

```bash
cd /Users/adamkerr/dev/atlas
git status --short --branch
.venv/bin/ruff check .
.venv/bin/ruff format --check .
.venv/bin/mypy
.venv/bin/pytest
.venv/bin/atlas doctor
git diff --check
```

If all checks pass, review and publish the branch:

```bash
git diff --stat
git diff
git add .
git commit -m "Initialize Atlas project foundation"
git push -u origin init
```

Then open a pull request from `init` to `main`. Suggested title:

```text
Initialize Atlas project foundation
```

Suggested pull-request summary:

```text
## Summary

- establish the Python 3.12 project and architectural package boundaries
- add typed YAML/environment configuration and structured timing-aware logging
- add the initial CLI, tests, Docker workflow, and project documentation

## Validation

- ruff check .
- ruff format --check .
- mypy
- pytest
- atlas doctor
```

## Recommended next milestone

After this foundation PR is reviewed, implement the text-first Milestone 3 CLI
behind small provider-neutral model and tool interfaces. Avoid adding voice or
LangGraph until the basic request/response seam is tested.
