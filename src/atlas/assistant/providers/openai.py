"""OpenAI Responses API adapter."""

from openai import OpenAI


class OpenAILanguageModel:
    """Generate provider-neutral text using OpenAI's Responses API."""

    def __init__(self, model: str, *, client: OpenAI | None = None) -> None:
        self._model = model
        self._client = client or OpenAI()

    def generate(self, prompt: str, *, instructions: str) -> str:
        response = self._client.responses.create(
            model=self._model,
            instructions=instructions,
            input=prompt,
        )
        return response.output_text
