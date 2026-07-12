import json
import logging

from atlas.logging.setup import JsonFormatter, timed_operation


def test_json_formatter_includes_context() -> None:
    record = logging.LogRecord("atlas.test", logging.INFO, "", 0, "request_complete", (), None)
    record.atlas = {"request_id": "abc", "duration_ms": 12.3}

    payload = json.loads(JsonFormatter().format(record))

    assert payload["event"] == "request_complete"
    assert payload["request_id"] == "abc"
    assert payload["duration_ms"] == 12.3


def test_timed_operation_logs_completion(caplog: object) -> None:
    logger = logging.getLogger("atlas.test")

    with timed_operation(logger, "graph_execution", request_id="abc"):
        pass
