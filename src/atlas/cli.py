"""Command-line entry points for Atlas."""

import time
from pathlib import Path
from typing import Annotated

import typer
from dotenv import load_dotenv

from atlas.assistant import AssistantService
from atlas.assistant.errors import ModelProviderError
from atlas.assistant.factory import create_language_model
from atlas.assistant.types import ModelResponse
from atlas.config import AtlasSettings, load_settings
from atlas.logging import configure_logging, get_logger

app = typer.Typer(help="Atlas voice assistant", no_args_is_help=True)


@app.callback()
def main() -> None:
    """Run Atlas commands."""
    load_dotenv()


@app.command()
def doctor(
    config: Annotated[
        Path,
        typer.Option("--config", "-c", help="Path to the Atlas YAML configuration."),
    ] = Path("config/atlas.yaml"),
) -> None:
    """Validate configuration and report whether the foundation is healthy."""
    settings: AtlasSettings = load_settings(config)
    configure_logging(settings.logging)
    logger = get_logger(__name__)
    logger.info(
        "atlas_doctor_complete",
        extra={
            "atlas": {
                "llm_provider": settings.llm.provider,
                "stt_provider": settings.voice.stt_provider,
                "tts_provider": settings.voice.tts_provider,
            }
        },
    )
    typer.echo("Atlas configuration is valid.")


@app.command()
def ask(
    prompt: Annotated[str, typer.Argument(help="Question or request for Atlas.")],
    config: Annotated[
        Path,
        typer.Option("--config", "-c", help="Path to the Atlas YAML configuration."),
    ] = Path("config/atlas.yaml"),
) -> None:
    """Send one text request to the configured language model."""
    settings = load_settings(config)
    configure_logging(settings.logging)
    model = create_language_model(settings.llm)
    assistant = AssistantService(model, personality=settings.assistant.personality)
    response = _request(assistant, prompt)
    typer.echo(response.text)


def _request(
    assistant: AssistantService,
    prompt: str,
    *,
    previous_response_id: str | None = None,
) -> ModelResponse:
    logger = get_logger(__name__)
    started = time.perf_counter()
    try:
        response = assistant.respond(prompt, previous_response_id=previous_response_id)
    except ModelProviderError as error:
        logger.warning(
            "assistant_provider_error",
            extra={
                "atlas": {
                    "error_code": error.code,
                    "duration_ms": round((time.perf_counter() - started) * 1000, 2),
                }
            },
        )
        typer.echo(f"Error: {error.message}", err=True)
        raise typer.Exit(1) from None
    logger.info(
        "assistant_request_complete",
        extra={"atlas": {"duration_ms": round((time.perf_counter() - started) * 1000, 2)}},
    )
    if response.usage is not None:
        logger.info(
            "assistant_usage",
            extra={
                "atlas": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens,
                    "total_tokens": response.usage.total_tokens,
                }
            },
        )
    return response


@app.command()
def chat(
    config: Annotated[
        Path,
        typer.Option("--config", "-c", help="Path to the Atlas YAML configuration."),
    ] = Path("config/atlas.yaml"),
) -> None:
    """Start an interactive text conversation."""
    settings = load_settings(config)
    configure_logging(settings.logging)
    assistant = AssistantService(
        create_language_model(settings.llm), personality=settings.assistant.personality
    )
    previous_response_id: str | None = None
    typer.echo("Atlas chat. Commands: /new, /status, /help, /exit")
    while True:
        try:
            prompt = typer.prompt("You")
        except (EOFError, KeyboardInterrupt):
            typer.echo("\nGoodbye.")
            return
        command = prompt.strip().lower()
        if command in {"/exit", "/quit"}:
            typer.echo("Goodbye.")
            return
        if command == "/new":
            previous_response_id = None
            typer.echo("Started a new conversation.")
            continue
        if command == "/help":
            typer.echo("/new clears context; /status shows state; /exit quits.")
            continue
        if command == "/status":
            state = "active" if previous_response_id else "new"
            typer.echo(f"Conversation: {state}; model: {settings.llm.model}")
            continue
        response = _request(assistant, prompt, previous_response_id=previous_response_id)
        previous_response_id = response.response_id
        typer.echo(f"Atlas: {response.text}")


if __name__ == "__main__":
    app()
