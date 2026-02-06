from __future__ import annotations

HIDDEN_SKILL_MAP = {
    "kubernetes": ["helm", "rbac", "service mesh"],
    "aws": ["iam", "vpc", "cloudwatch"],
    "python": ["testing", "packaging", "type hints"],
    "react": ["state management", "component design"],
    "sql": ["query optimization", "data modeling"],
}


def infer_hidden_skills(explicit_skills: list[str]) -> list[str]:
    inferred = []
    for skill in explicit_skills:
        inferred.extend(HIDDEN_SKILL_MAP.get(skill, []))
    return sorted(set(inferred))
