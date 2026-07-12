"""Command-line entry points for Atlas."""

from pathlib import Path
from typing import Annotated

import typer

from atlas.assistant import AssistantService
from atlas.assistant.factory import create_language_model
from atlas.config import AtlasSettings, load_settings
from atlas.logging import configure_logging, get_logger, timed_operation

app = typer.Typer(help="Atlas voice assistant", no_args_is_help=True)


@app.callback()
def main() -> None:
    """Run Atlas commands."""


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
    with timed_operation(get_logger(__name__), "assistant_request"):
        response = assistant.respond(prompt)
    typer.echo(response)


if __name__ == "__main__":
    app()
