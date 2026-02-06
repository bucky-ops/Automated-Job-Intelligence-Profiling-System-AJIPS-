from __future__ import annotations

from ajips.app.api.schemas import FocusArea

FOCUS_AREA_MAP = {
    "backend": {"python", "java", "sql", "postgresql", "mysql", "fastapi"},
    "cloud": {"aws", "gcp", "azure", "kubernetes", "docker"},
    "frontend": {"javascript", "react"},
    "data": {"spark", "airflow"},
}


def build_focus_areas(explicit_skills: list[str]) -> list[FocusArea]:
    focus_areas: list[FocusArea] = []
    for area, keywords in FOCUS_AREA_MAP.items():
        matched = [skill for skill in explicit_skills if skill in keywords]
        if matched:
            weight = round(len(matched) / max(len(explicit_skills), 1), 2)
            focus_areas.append(FocusArea(name=area, weight=weight, skills=matched))
    if not focus_areas:
        focus_areas.append(FocusArea(name="general", weight=1.0, skills=explicit_skills))
    return focus_areas
