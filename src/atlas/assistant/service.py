"""Text-first assistant application service."""

from atlas.assistant.types import LanguageModel


class AssistantService:
    """Turn user text into an assistant response through an injected model."""

    def __init__(self, model: LanguageModel, *, personality: str) -> None:
        self._model = model
        self._instructions = f"You are Atlas, a helpful voice assistant. Be {personality}."

    def respond(self, text: str) -> str:
        prompt = text.strip()
        if not prompt:
            raise ValueError("Prompt must not be empty.")
        response = self._model.generate(prompt, instructions=self._instructions).strip()
        if not response:
            raise RuntimeError("The language model returned an empty response.")
        return response
