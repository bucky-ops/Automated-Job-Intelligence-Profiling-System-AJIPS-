from __future__ import annotations

import re
from typing import List

from ajips.app.api.schemas import CritiqueItem
from ajips.app.services.constants import (
    CLOUD_PROVIDERS,
    COMMON_DATABASES,
    ENTRY_LEVEL_KEYWORDS,
    ENTRY_LEVEL_MAX_YEARS,
    MAX_REALISTIC_YEARS,
    TECH_AGE_LIMITS,
    YEARS_PATTERN,
)
from ajips.core.logging_config import get_logger

logger = get_logger(__name__)


def critique_requirements(text: str) -> List[CritiqueItem]:
    """
    Analyze job requirements and provide critiques on potential issues.
    Checks for:
    - Experience level mismatches
    - Unrealistic skill combinations
    - Vague or ambiguous requirements
    - Missing critical information
    """
    critiques: List[CritiqueItem] = []
    text_lower = text.lower()

    # Check 1: Entry-level with years of experience contradiction
    if re.search(r"\b(entry.?level|junior)\b", text_lower):
        years_match = re.search(YEARS_PATTERN, text_lower)
        if years_match and int(years_match.group(1)) >= ENTRY_LEVEL_MAX_YEARS:
            critiques.append(
                CritiqueItem(
                    severity="warning",
                    message=f"Entry-level role requires {years_match.group(1)}+ years of experience. "
                    "This is contradictory and may discourage qualified candidates.",
                )
            )

    # Check 2: Unrealistic experience requirements
    years_matches = re.findall(YEARS_PATTERN, text_lower)
    if years_matches:
        max_years = max(int(y) for y in years_matches)
        if max_years > MAX_REALISTIC_YEARS:
            critiques.append(
                CritiqueItem(
                    severity="info",
                    message=f"Requires {max_years}+ years of experience. Consider if this is truly necessary "
                    "or if it might exclude qualified candidates.",
                )
            )

    # Check 3: Technology age vs experience requirement
    for tech_name, tech_age in TECH_AGE_LIMITS.items():
        pattern = re.escape(tech_name).replace(r"\.", r"\.").replace(" ", r"\s+")
        if re.search(pattern, text_lower, re.IGNORECASE):
            # Look for years mention near the tech
            context = re.search(pattern + r".*?(\d+)\+?\s*years?", text_lower, re.IGNORECASE)
            if context:
                required_years = int(context.group(1))
                if required_years > tech_age:
                    critiques.append(
                        CritiqueItem(
                            severity="critical",
                            message=f"{tech_name} has only existed for ~{tech_age} years, but the posting "
                            f"requires {required_years}+ years. This is impossible.",
                        )
                    )

    # Check 4: Vague cloud requirements
    if "cloud" in text_lower and not any(provider in text_lower for provider in CLOUD_PROVIDERS):
        critiques.append(
            CritiqueItem(
                severity="info",
                message="Cloud requirement is unspecified. Clarify preferred cloud provider (AWS, Azure, GCP).",
            )
        )
    
    # Check 6: Too many programming languages
    languages = ["python", "java", "javascript", "typescript", "c++", "c#", "go", "rust", "ruby", "php"]
    mentioned_languages = [lang for lang in languages if lang in text_lower]
    if len(mentioned_languages) > 3:
        critiques.append(
            CritiqueItem(
                severity="warning",
                message=f"Requires {len(mentioned_languages)} programming languages ({', '.join(mentioned_languages)}). "
                       "Consider if all are truly necessary or if this might be too broad."
            )
        )
    
    # Check 7: Missing salary information
    if not re.search(r'\$\s*\d+|salary|compensation|pay range', text_lower):
        critiques.append(
            CritiqueItem(
                severity="info",
                message="No salary or compensation information provided. Including salary range increases "
                       "application rates and attracts more qualified candidates."
            )
        )
    
    # Check 8: Missing remote/location information
    if not re.search(r'\b(remote|hybrid|on.?site|location|office)\b', text_lower):
        critiques.append(
            CritiqueItem(
                severity="info",
                message="Work location or remote policy not clearly specified."
            )
        )
    
    # Check 9: Unrealistic full-stack requirements
    if re.search(r'\bfull.?stack\b', text_lower):
        # Count distinct technology categories
        has_frontend = any(fw in text_lower for fw in ["react", "angular", "vue", "frontend", "front-end"])
        has_backend = any(fw in text_lower for fw in ["django", "flask", "spring", "express", "backend", "back-end"])
        has_database = any(db in text_lower for db in ["postgresql", "mysql", "mongodb", "database"])
        has_devops = any(tool in text_lower for tool in ["docker", "kubernetes", "aws", "azure", "devops"])
        has_mobile = any(tech in text_lower for tech in ["ios", "android", "react native", "flutter"])
        
        tech_count = sum([has_frontend, has_backend, has_database, has_devops, has_mobile])
        if tech_count >= 4:
            critiques.append(
                CritiqueItem(
                    severity="warning",
                    message="Full-stack role requires expertise in many areas (frontend, backend, database, "
                           "DevOps, mobile). Consider if this is realistic or if the role should be split."
                )
            )
    
    # Check 10: Buzzword overload
    buzzwords = ["rockstar", "ninja", "guru", "wizard", "unicorn", "10x"]
    found_buzzwords = [word for word in buzzwords if word in text_lower]
    if found_buzzwords:
        critiques.append(
            CritiqueItem(
                severity="warning",
                message=f"Contains buzzwords ({', '.join(found_buzzwords)}) that may be off-putting to "
                       "professional candidates. Consider using standard job titles."
            )
        )
    
    # Check 11: Lack of specific responsibilities
    if len(text) < 200:
        critiques.append(
            CritiqueItem(
                severity="warning",
                message="Job description is very brief. Consider adding more detail about responsibilities, "
                       "team structure, and growth opportunities."
            )
        )
    
    # Check 12: Degree requirements
    if re.search(r'\b(phd|ph\.d\.|doctorate)\b', text_lower) and not re.search(r'\b(research|scientist|professor)\b', text_lower):
        critiques.append(
            CritiqueItem(
                severity="info",
                message="Requires PhD but role doesn't appear to be research-focused. Consider if this "
                       "requirement is necessary or if it might exclude qualified candidates."
            )
        )
    
    # If no issues found, provide positive feedback
    if not critiques:
        critiques.append(
            CritiqueItem(
                severity="info",
                message="Requirements appear well-balanced and clearly specified. Consider adding salary "
                       "range and remote work policy if not already included."
            )
        )
    
    return critiques


def analyze_job_quality(text: str) -> dict:
    """
    Provide an overall quality score and analysis of the job posting.
    Returns a dictionary with score (0-100) and analysis breakdown.
    """
    score = 100
    issues = []
    
    # Deduct points for various issues
    if len(text) < 200:
        score -= 20
        issues.append("Very brief description")
    
    if not re.search(r'\$\s*\d+|salary|compensation', text.lower()):
        score -= 15
        issues.append("No salary information")
    
    if not re.search(r'\b(remote|hybrid|on.?site)\b', text.lower()):
        score -= 10
        issues.append("No work location policy")
    
    buzzwords = ["rockstar", "ninja", "guru", "wizard", "unicorn"]
    if any(word in text.lower() for word in buzzwords):
        score -= 15
        issues.append("Contains unprofessional buzzwords")
    
    # Check for positive elements
    positives = []
    if re.search(r'\b(benefits|health|insurance|401k|pto|vacation)\b', text.lower()):
        positives.append("Mentions benefits")
    
    if re.search(r'\b(growth|learning|development|training)\b', text.lower()):
        positives.append("Emphasizes growth opportunities")
    
    if re.search(r'\b(team|culture|values|mission)\b', text.lower()):
        positives.append("Describes company culture")
    
    return {
        "score": max(0, score),
        "grade": "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "D" if score >= 60 else "F",
        "issues": issues,
        "positives": positives
    }
