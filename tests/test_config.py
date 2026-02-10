"""Unit tests for configuration handling."""

import os
from unittest.mock import patch
import pytest

from ajips.app.config import Settings, settings


def test_default_settings():
    s = Settings()
    assert "127.0.0.1:8000" in s.CORS_ORIGINS
    assert "localhost:8000" in s.CORS_ORIGINS
    assert s.LOG_LEVEL == "INFO"
    assert s.LOG_FORMAT == "json"
    assert s.INGESTION_TIMEOUT_S == 10
    assert "linkedin.com" in s.INGESTION_ALLOWED_NETLOCS


@patch.dict(
    os.environ,
    {
        "CORS_ORIGINS": "https://example.com,https://api.example.com",
        "LOG_LEVEL": "debug",
        "LOG_FORMAT": "text",
        "INGESTION_TIMEOUT_S": "15",
        "INGESTION_ALLOWED_NETLOCS": "example.com,api.example.com",
    },
)
def test_settings_from_env():
    s = Settings.from_env()
    assert s.CORS_ORIGINS == ["https://example.com", "https://api.example.com"]
    assert s.LOG_LEVEL == "DEBUG"
    assert s.LOG_FORMAT == "text"
    assert s.INGESTION_TIMEOUT_S == 15
    assert s.INGESTION_ALLOWED_NETLOCS == ["example.com", "api.example.com"]


def test_global_settings_instance():
    # Ensure settings singleton is loaded from env by default
    assert isinstance(settings, Settings)
    assert hasattr(settings, "CORS_ORIGINS")
