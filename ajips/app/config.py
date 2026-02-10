"""Production-ready configuration with environment variable support."""

import os
from typing import List, Optional


# Base configuration
class Settings:
    # API
    API_TITLE: str = "AJIPS - Automated Job Intelligence Profiling System"
    API_VERSION: str = "1.1.0"
    API_DESCRIPTION: str = "Analyze job postings with AI-powered insights"

    # CORS: Comma-separated list of allowed origins; defaults to localhost
    CORS_ORIGINS: List[str] = [
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["GET", "POST"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # "json" or "text"

    # Ingestion/SSRF
    INGESTION_TIMEOUT_S: int = 10
    # Comma-separated list of allowed netlocs; empty means allow any non-private hostname
    INGESTION_ALLOWED_NETLOCS: List[str] = [
        "linkedin.com",
        "indeed.com",
        "glassdoor.com",
        "monster.com",
        "ziprecruiter.com",
        "careerbuilder.com",
        "jobs.eu.lever.co",
        "boards.greenhouse.io",
        "jobs.github.com",
        "wellfound.com",
    ]

    @classmethod
    def from_env(cls) -> "Settings":
        """Override settings from environment variables."""
        settings = cls()
        # CORS origins
        cors_origins_env = os.getenv("CORS_ORIGINS")
        if cors_origins_env:
            settings.CORS_ORIGINS = [
                o.strip() for o in cors_origins_env.split(",") if o.strip()
            ]
        # Logging
        log_level = os.getenv("LOG_LEVEL")
        if log_level:
            settings.LOG_LEVEL = log_level.upper()
        log_format = os.getenv("LOG_FORMAT")
        if log_format:
            settings.LOG_FORMAT = log_format.lower()
        # Ingestion
        timeout = os.getenv("INGESTION_TIMEOUT_S")
        if timeout and timeout.isdigit():
            settings.INGESTION_TIMEOUT_S = int(timeout)
        netlocs_env = os.getenv("INGESTION_ALLOWED_NETLOCS")
        if netlocs_env:
            settings.INGESTION_ALLOWED_NETLOCS = [
                n.strip() for n in netlocs_env.split(",") if n.strip()
            ]
        return settings


# Global settings instance
settings = Settings.from_env()
