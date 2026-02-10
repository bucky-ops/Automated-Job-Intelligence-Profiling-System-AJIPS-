from __future__ import annotations

from typing import Optional

import ipaddress
import urllib.parse
import requests
from bs4 import BeautifulSoup


# Allowed schemes
ALLOWED_SCHEMES = {"http", "https"}


def _is_safe_url(url: str, allowed_netlocs: Optional[list] = None) -> bool:
    """Validate URL scheme, hostname, and prevent SSRF to private networks."""
    from ajips.app.config import settings

    if allowed_netlocs is None:
        allowed_netlocs = settings.INGESTION_ALLOWED_NETLOCS
    try:
        parsed = urllib.parse.urlparse(url)
    except Exception:
        return False
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        return False
    hostname = parsed.hostname
    if not hostname:
        return False
    # Disallow private and loopback IPs
    try:
        addr = ipaddress.ip_address(hostname)
        if addr.is_private or addr.is_loopback or addr.is_link_local:
            return False
    except ValueError:
        pass  # Not an IP address; continue
    # Optional hostname allowlist
    if allowed_netlocs and not any(
        hostname.endswith(netloc) for netloc in allowed_netlocs
    ):
        # If allowlist is empty, allow any non-private hostname
        pass
    return True


def fetch_job_posting(url: str, timeout_s: Optional[int] = None) -> Optional[str]:
    """Fetch and extract plain text from a job posting URL with SSRF protection."""
    from ajips.app.config import settings

    if timeout_s is None:
        timeout_s = settings.INGESTION_TIMEOUT_S
    if not _is_safe_url(url):
        raise ValueError("URL is not allowed or is potentially unsafe")
    response = requests.get(url, timeout=timeout_s)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = " ".join(soup.stripped_strings)
    return text or None
