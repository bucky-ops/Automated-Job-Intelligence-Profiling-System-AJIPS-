"""Centralized configuration and constants for AJIPS."""

from enum import Enum


class SeverityLevel(str, Enum):
    """Critique severity levels."""

    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


# Salary extraction patterns (order matters: more specific patterns first)
SALARY_PATTERNS = [
    # $120k-$160k or 120k-160k or $120k-$160k/year
    r"\$?(\d+(?:,\d{3})*)k\s*(?:to|-|–)\s*\$?(\d+(?:,\d{3})*)k",
    r"\$?(\d+(?:,\d{3})*)k",
    # Standard dollar ranges $120,000-$160,000
    r"\$(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:to|-|–)\s*\$?(\d+(?:,\d{3})*(?:\.\d{2})?)",
    r"\$(\d+(?:,\d{3})*(?:\.\d{2})?)",
]

# Interview stage keywords
INTERVIEW_STAGES = {
    "phone": [
        "phone screen",
        "phone interview",
        "phone call",
        "screening call",
        "phone",
    ],
    "technical": [
        "technical interview",
        "coding interview",
        "technical assessment",
        "coding challenge",
        "code",
        "coding",
        "technical",
    ],
    "system_design": ["system design", "architecture", "design interview", "design"],
    "behavioral": [
        "behavioral interview",
        "culture fit",
        "final round",
        "onsite",
        "culture",
        "behavioral",
    ],
}

# Experience thresholds
MAX_REALISTIC_YEARS = 15
ENTRY_LEVEL_MAX_YEARS = 2

# Cloud providers
CLOUD_PROVIDERS = ("aws", "azure", "gcp", "google cloud", "heroku")

# Common databases
COMMON_DATABASES = ("postgresql", "mysql", "mongodb", "redis", "oracle", "sql server")

# Role templates for skill inference
ROLE_TEMPLATES = {
    "Data Scientist": ["Python", "Pandas", "Statistics", "Machine Learning"],
    "Backend Engineer": ["Python", "Databases", "REST APIs", "Microservices"],
    "Frontend Developer": ["React", "JavaScript", "CSS", "HTML"],
    "DevOps Engineer": ["Docker", "Kubernetes", "AWS", "Linux"],
    "Full Stack Developer": ["React", "Node.js", "Databases", "Docker"],
}

# Technology age limits (in years)
TECH_AGE_LIMITS = {
    "next.js": 5,
    "rust": 15,
    "go": 13,
    "kubernetes": 8,
}
