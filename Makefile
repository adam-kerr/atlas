.PHONY: install check test lint format doctor

install:
	uv sync --dev

check: lint test

test:
	uv run pytest

lint:
	uv run ruff check .
	uv run ruff format --check .
	uv run mypy

format:
	uv run ruff check --fix .
	uv run ruff format .

doctor:
	uv run atlas doctor
