"""Text-first assistant application service."""

from atlas.assistant.types import LanguageModel, ModelResponse


class AssistantService:
    """Turn user text into an assistant response through an injected model."""

    def __init__(self, model: LanguageModel, *, personality: str) -> None:
        self._model = model
        self._instructions = f"You are Atlas, a helpful voice assistant. Be {personality}."

    def respond(self, text: str, *, previous_response_id: str | None = None) -> ModelResponse:
        prompt = text.strip()
        if not prompt:
            raise ValueError("Prompt must not be empty.")
        response = self._model.generate(
            prompt, instructions=self._instructions, previous_response_id=previous_response_id
        )
        response_text = response.text.strip()
        if not response_text:
            raise RuntimeError("The language model returned an empty response.")
        return ModelResponse(response_text, response.response_id, response.usage)
