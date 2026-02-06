from __future__ import annotations

from collections import Counter

SKILL_KEYWORDS = {
    "python",
    "java",
    "javascript",
    "sql",
    "postgresql",
    "mysql",
    "aws",
    "gcp",
    "azure",
    "kubernetes",
    "docker",
    "react",
    "fastapi",
    "spark",
    "airflow",
}


def extract_skills(text: str) -> list[str]:
    tokens = [token.strip(".,;:()[]{}") for token in text.lower().split()]
    counts = Counter(token for token in tokens if token in SKILL_KEYWORDS)
    return [skill for skill, _ in counts.most_common()]
