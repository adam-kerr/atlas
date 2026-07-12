import json
import logging

import pytest

from atlas.logging.setup import JsonFormatter, timed_operation


def test_json_formatter_includes_context() -> None:
    record = logging.LogRecord("atlas.test", logging.INFO, "", 0, "request_complete", (), None)
    record.atlas = {"request_id": "abc", "duration_ms": 12.3}

    payload = json.loads(JsonFormatter().format(record))

    assert payload["event"] == "request_complete"
    assert payload["request_id"] == "abc"
    assert payload["duration_ms"] == 12.3


def test_timed_operation_logs_completion(caplog: pytest.LogCaptureFixture) -> None:
    logger = logging.getLogger("atlas.test")

    with (
        caplog.at_level(logging.INFO, logger="atlas.test"),
        timed_operation(logger, "graph_execution", request_id="abc"),
    ):
        pass

    record = caplog.records[-1]
    assert record.getMessage() == "graph_execution_complete"
    assert record.atlas["request_id"] == "abc"
    assert isinstance(record.atlas["duration_ms"], float)
