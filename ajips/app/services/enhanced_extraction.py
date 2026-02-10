"""Enhanced extraction services for salary and interview details."""

import re
from typing import Dict, Optional

from .constants import INTERVIEW_STAGES, SALARY_PATTERNS


def extract_salary_range(text: str) -> Optional[Dict]:
    """
    Extract salary range from job posting.

    Args:
        text: Job posting text

    Returns:
        Dict with 'min' and 'max' salary or None
    """
    if not text:
        return None

    text_lower = text.lower()

    for pattern in SALARY_PATTERNS:
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        if matches:
            try:
                if isinstance(matches[0], tuple):
                    min_sal, max_sal = matches[0]
                    # Check if this was a k-format pattern by checking if the original text has 'k'
                    if "k" in text_lower and pattern == SALARY_PATTERNS[0]:
                        min_sal += "k"
                        max_sal += "k"
                else:
                    min_sal = matches[0]
                    max_sal = None
                    # Check if this was a k-format pattern
                    if "k" in text_lower and pattern == SALARY_PATTERNS[1]:
                        min_sal += "k"

                min_val = _parse_salary(min_sal)
                max_val = _parse_salary(max_sal) if max_sal else min_val

                if min_val and max_val:
                    return {"min": min_val, "max": max_val, "currency": "USD"}
            except (ValueError, TypeError):
                continue

    return None


def _parse_salary(salary_str: str) -> Optional[int]:
    """Parse salary string to integer."""
    if not salary_str:
        return None

    salary_str = salary_str.replace(",", "").replace("$", "").strip()

    # Check if ends with 'k'
    if salary_str.lower().endswith("k"):
        try:
            return int(float(salary_str[:-1]) * 1000)
        except ValueError:
            return None

    try:
        return int(float(salary_str))
    except ValueError:
        return None


def extract_interview_stages(text: str) -> Dict:
    """
    Detect interview stages from job posting.

    Args:
        text: Job posting text

    Returns:
        Dict with detected stages and interview details
    """
    if not text:
        return {"stages": [], "estimated_rounds": 0}

    text_lower = text.lower()
    detected_stages = []

    # Detect interview stages
    for stage, keywords in INTERVIEW_STAGES.items():
        for keyword in keywords:
            if keyword in text_lower:
                if stage not in detected_stages:
                    detected_stages.append(stage)
                break

    # Estimate number of rounds
    rounds_match = re.search(r"(\d+)\s*(?:round|interview|stage)s?", text_lower)
    estimated_rounds = (
        int(rounds_match.group(1)) if rounds_match else len(detected_stages) or 3
    )

    return {
        "stages": detected_stages,
        "estimated_rounds": estimated_rounds,
        "total_detected": len(detected_stages),
    }
