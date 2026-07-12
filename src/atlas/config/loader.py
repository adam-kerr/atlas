"""Configuration loading with YAML defaults and environment overrides."""

import os
from pathlib import Path
from typing import Any

import yaml

from atlas.config.models import AtlasSettings

ENV_PREFIX = "ATLAS_"


def _coerce(value: str) -> Any:
    """Use YAML scalar rules for booleans, numbers, nulls, and strings."""
    return yaml.safe_load(value)


def _environment_overrides(environment: dict[str, str]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for name, value in environment.items():
        if not name.startswith(ENV_PREFIX):
            continue
        path = name.removeprefix(ENV_PREFIX).lower().split("__")
        target = result
        for part in path[:-1]:
            target = target.setdefault(part, {})
        target[path[-1]] = _coerce(value)
    return result


def _merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_settings(
    path: Path | str = Path("config/atlas.yaml"),
    *,
    environment: dict[str, str] | None = None,
) -> AtlasSettings:
    """Load Atlas settings from YAML, then apply `ATLAS_` overrides."""
    config_path = Path(path)
    raw: dict[str, Any] = {}
    if config_path.exists():
        loaded = yaml.safe_load(config_path.read_text(encoding="utf-8"))
        if loaded is not None and not isinstance(loaded, dict):
            raise ValueError(f"Configuration root must be a mapping: {config_path}")
        raw = loaded or {}
    overrides = _environment_overrides(environment if environment is not None else dict(os.environ))
    return AtlasSettings.model_validate(_merge(raw, overrides))
