import pytest

from atlas.assistant import AssistantService


class FakeLanguageModel:
    def __init__(self, response: str = "Hello from Atlas") -> None:
        self.response = response
        self.prompt: str | None = None
        self.instructions: str | None = None

    def generate(self, prompt: str, *, instructions: str) -> str:
        self.prompt = prompt
        self.instructions = instructions
        return self.response


def test_responds_through_injected_model() -> None:
    model = FakeLanguageModel()
    assistant = AssistantService(model, personality="concise")

    response = assistant.respond("  Hello  ")

    assert response == "Hello from Atlas"
    assert model.prompt == "Hello"
    assert model.instructions == "You are Atlas, a helpful voice assistant. Be concise."


def test_rejects_empty_prompt() -> None:
    assistant = AssistantService(FakeLanguageModel(), personality="concise")

    with pytest.raises(ValueError, match="must not be empty"):
        assistant.respond("  ")


def test_rejects_empty_model_response() -> None:
    assistant = AssistantService(FakeLanguageModel("  "), personality="concise")

    with pytest.raises(RuntimeError, match="empty response"):
        assistant.respond("Hello")
