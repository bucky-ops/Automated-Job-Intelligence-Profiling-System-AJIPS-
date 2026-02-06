from __future__ import annotations

from typing import Optional

import requests
from bs4 import BeautifulSoup


def fetch_job_posting(url: str, timeout_s: int = 10) -> Optional[str]:
    response = requests.get(url, timeout=timeout_s)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = " ".join(soup.stripped_strings)
    return text or None
