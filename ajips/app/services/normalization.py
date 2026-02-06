from __future__ import annotations

import re


def normalize_text(text: str) -> str:
    collapsed = re.sub(r"\s+", " ", text)
    return collapsed.strip()


def split_sections(text: str) -> dict[str, str]:
    sections = {"body": text}
    for heading in ("Responsibilities", "Qualifications", "Requirements"):
        pattern = rf"{heading}\s*[:\-]"
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            sections[heading.lower()] = text[match.end():].strip()
    return sections
