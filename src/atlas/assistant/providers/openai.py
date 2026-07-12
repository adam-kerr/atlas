"""OpenAI Responses API adapter."""

from typing import Protocol, cast

from openai import OpenAI


class ModelResponse(Protocol):
    output_text: str


class ResponsesResource(Protocol):
    def create(self, *, model: str, instructions: str, input: str) -> ModelResponse: ...


class OpenAIClient(Protocol):
    responses: ResponsesResource


class OpenAILanguageModel:
    """Generate provider-neutral text using OpenAI's Responses API."""

    def __init__(self, model: str, *, client: OpenAIClient | None = None) -> None:
        self._model = model
        self._client = client or cast(OpenAIClient, OpenAI())

    def generate(self, prompt: str, *, instructions: str) -> str:
        response = self._client.responses.create(
            model=self._model,
            instructions=instructions,
            input=prompt,
        )
        return response.output_text
