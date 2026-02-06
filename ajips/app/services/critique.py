from __future__ import annotations

from ajips.app.api.schemas import CritiqueItem


def critique_requirements(text: str) -> list[CritiqueItem]:
    critiques: list[CritiqueItem] = []
    if "years" in text.lower() and "entry" in text.lower():
        critiques.append(
            CritiqueItem(
                severity="warning",
                message="Entry-level role mentions years of experience; clarify the expectation.",
            )
        )
    if "cloud" in text.lower() and not any(provider in text.lower() for provider in ("aws", "azure", "gcp")):
        critiques.append(
            CritiqueItem(
                severity="info",
                message="Cloud requirement is unspecified; clarify preferred provider.",
            )
        )
    if not critiques:
        critiques.append(
            CritiqueItem(
                severity="info",
                message="Requirements appear consistent; consider adding role-specific detail.",
            )
        )
    return critiques
