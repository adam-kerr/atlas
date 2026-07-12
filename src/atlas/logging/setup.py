"""Logging setup and interaction timing helpers."""

import json
import logging
import time
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime
from typing import Any

from atlas.config.models import LoggingSettings


class JsonFormatter(logging.Formatter):
    """Emit stable, machine-readable log records."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, tz=UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "event": record.getMessage(),
        }
        context = getattr(record, "atlas", None)
        if isinstance(context, dict):
            payload.update(context)
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str, separators=(",", ":"))


def configure_logging(settings: LoggingSettings) -> None:
    """Configure the root logger once at application startup."""
    handler = logging.StreamHandler()
    if settings.format == "json":
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(settings.level)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


@contextmanager
def timed_operation(logger: logging.Logger, operation: str, **context: Any) -> Iterator[None]:
    """Log an operation's completion or failure with elapsed time."""
    started = time.perf_counter()
    try:
        yield
    except Exception:
        duration_ms = round((time.perf_counter() - started) * 1000, 2)
        logger.exception(
            f"{operation}_failed",
            extra={"atlas": {**context, "duration_ms": duration_ms}},
        )
        raise
    else:
        duration_ms = round((time.perf_counter() - started) * 1000, 2)
        logger.info(
            f"{operation}_complete",
            extra={"atlas": {**context, "duration_ms": duration_ms}},
        )
