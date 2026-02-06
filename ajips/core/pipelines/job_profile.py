from __future__ import annotations

from ajips.app.api.schemas import AnalyzeRequest, AnalyzeResponse
from ajips.app.services.critique import critique_requirements
from ajips.app.services.enrichment import infer_hidden_skills
from ajips.app.services.extraction import extract_skills
from ajips.app.services.ingestion import fetch_job_posting
from ajips.app.services.normalization import normalize_text
from ajips.app.services.profiling import build_focus_areas
from ajips.app.services.resume_match import compute_resume_alignment


def build_job_profile(payload: AnalyzeRequest) -> AnalyzeResponse:
    raw_text = payload.job_posting.text
    if not raw_text and payload.job_posting.url:
        raw_text = fetch_job_posting(payload.job_posting.url)
    if not raw_text:
        raw_text = ""

    normalized = normalize_text(raw_text)
    explicit_skills = extract_skills(normalized)
    hidden_skills = infer_hidden_skills(explicit_skills)
    critiques = critique_requirements(normalized)
    focus_areas = build_focus_areas(explicit_skills)

    resume_alignment = None
    if payload.resume_text:
        resume_alignment = compute_resume_alignment(payload.resume_text, explicit_skills)

    summary = "Generated profile with focus areas and inferred skills."

    return AnalyzeResponse(
        title=None,
        focus_areas=focus_areas,
        explicit_skills=explicit_skills,
        hidden_skills=hidden_skills,
        critiques=critiques,
        resume_alignment=resume_alignment,
        summary=summary,
    )
