"""Provider-neutral assistant interfaces."""

from collections.abc import Mapping
from typing import Protocol


class LanguageModel(Protocol):
    """Generate text without exposing provider-specific response types."""

    def generate(self, prompt: str, *, instructions: str) -> str: ...


class Tool(Protocol):
    """Expose an integration capability without provider-specific details."""

    @property
    def name(self) -> str: ...

    @property
    def description(self) -> str: ...

    def invoke(self, arguments: Mapping[str, object]) -> str: ...
