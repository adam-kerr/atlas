"""Typed configuration for Atlas."""

from atlas.config.loader import load_settings
from atlas.config.models import AtlasSettings

__all__ = ["AtlasSettings", "load_settings"]
