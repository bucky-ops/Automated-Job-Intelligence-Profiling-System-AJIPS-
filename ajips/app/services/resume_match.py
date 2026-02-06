from __future__ import annotations


def compute_resume_alignment(resume_text: str, explicit_skills: list[str]) -> float:
    resume_tokens = {token.strip(".,;:()[]{}") for token in resume_text.lower().split()}
    if not explicit_skills:
        return 0.0
    matches = sum(1 for skill in explicit_skills if skill in resume_tokens)
    return round(matches / len(explicit_skills), 2)
