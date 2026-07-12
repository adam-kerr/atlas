# Architecture

Atlas has three primary layers with one-way conceptual dependencies.

```text
Voice layer          Assistant layer             Integration layer
wake word            conversation state          weather
VAD          ------> routing and reasoning ------> calendar
STT / TTS            tool selection              Home Assistant
playback              response generation         notes and reminders
```

## Boundaries

### Voice

The voice package only handles audio. It produces text and consumes text; it
does not know about tools, language models, or business logic. Wake-word, STT,
and TTS providers must be replaceable behind small Python protocols.

### Assistant

The assistant owns intelligence and orchestration. LangGraph will manage the
conversation graph, but domain interfaces should remain ordinary typed Python
so orchestration libraries do not leak across the codebase.

### Integrations

Each integration exposes a clean capability interface. Provider-specific
clients and credentials remain inside their integration package.

## Initial request flow

```text
input -> route -> optional tool execution -> generate response -> output
```

Configuration and logging are shared infrastructure, not architectural layers.
All significant operations should emit structured events with duration and a
correlation identifier once request processing is introduced.
