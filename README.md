# Atlas

Atlas is a modular, self-hosted voice assistant designed for Raspberry Pi. It
keeps audio, assistant orchestration, and external integrations loosely coupled
so each can evolve independently.

## Status

Atlas is in its foundation phase. The repository currently provides:

- a Python 3.12 project with strict package boundaries
- typed, environment-aware YAML configuration
- structured JSON logging with timing support
- Docker and local development entry points
- an initial test suite

## Architecture

```text
Voice layer -> Assistant layer -> Integration layer
 audio          reasoning         capabilities
```

- **Voice** converts speech to text and text to speech.
- **Assistant** owns conversation, reasoning, memory, and tool selection.
- **Integrations** expose capabilities through provider-neutral interfaces.

See [docs/architecture.md](docs/architecture.md) for the design boundaries.

## Quick start

Requirements: Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync --dev
uv run atlas doctor
uv run pytest
```

Atlas reads `config/atlas.yaml` by default. Override individual settings with
environment variables using `ATLAS_` and `__` for nesting:

```bash
ATLAS_LLM__PROVIDER=anthropic ATLAS_LOGGING__LEVEL=DEBUG uv run atlas doctor
```

Run the same check in Docker:

```bash
docker compose run --rm atlas doctor
```

## Roadmap

1. Infrastructure and Raspberry Pi setup
2. Project skeleton, configuration, and logging
3. Text-first CLI assistant
4. LangGraph routing, tools, and memory
5. Wake word, speech-to-text, and text-to-speech
6. LEDs, mute controls, and enclosure

The guiding principle is maintainability over novelty.
