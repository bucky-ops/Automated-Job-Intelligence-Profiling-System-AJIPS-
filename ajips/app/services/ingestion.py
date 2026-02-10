from __future__ import annotations

from functools import lru_cache
from typing import Optional

import requests
from bs4 import BeautifulSoup

from ajips.app.services.constants import CACHE_TTL_SECONDS, MAX_CACHE_SIZE
from ajips.core.logging_config import get_logger

logger = get_logger(__name__)


@lru_cache(maxsize=MAX_CACHE_SIZE)
def fetch_job_posting(url: str, timeout_s: int = 10) -> Optional[str]:
    """
    Fetch job posting from URL with caching.

    Args:
        url: URL to job posting
        timeout_s: Request timeout in seconds

    Returns:
        Cleaned job posting text or None

    Raises:
        ValueError: If fetch fails
    """
    try:
        logger.info(f"Fetching job posting from URL", extra={"url": url[:50]})

        response = requests.get(url, timeout=timeout_s)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove script, style, and noscript tags
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = " ".join(soup.stripped_strings)

        if text:
            logger.info(f"Successfully fetched job posting", extra={"url": url[:50], "chars": len(text)})
            return text

        logger.warning(f"Empty content from URL", extra={"url": url[:50]})
        return None

    except requests.RequestException as exc:
        logger.error(f"Failed to fetch URL: {str(exc)}", extra={"url": url[:50]})
        raise ValueError(f"Failed to fetch job posting from URL: {str(exc)}") from exc
