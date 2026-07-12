"""Provider-neutral assistant interfaces."""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ModelUsage:
    input_tokens: int
    output_tokens: int
    total_tokens: int


@dataclass(frozen=True)
class ModelResponse:
    text: str
    response_id: str | None = None
    usage: ModelUsage | None = None


class LanguageModel(Protocol):
    """Generate text without exposing provider-specific response types."""

    def generate(
        self, prompt: str, *, instructions: str, previous_response_id: str | None = None
    ) -> ModelResponse: ...


class Tool(Protocol):
    """Expose an integration capability without provider-specific details."""

    @property
    def name(self) -> str: ...

    @property
    def description(self) -> str: ...

    def invoke(self, arguments: Mapping[str, object]) -> str: ...
