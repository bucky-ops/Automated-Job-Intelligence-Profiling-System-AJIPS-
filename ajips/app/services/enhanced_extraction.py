"""
Enhanced extraction services for salary ranges and interview processes.
"""

import re
from typing import Dict, List, Optional

from ajips.app.services.constants import (
    INTERVIEW_STAGES,
    SALARY_K_PATTERN,
    SALARY_PATTERN,
)


def extract_salary_range(text: str) -> Optional[Dict[str, int]]:
    """
    Extract salary range from job posting.

    Args:
        text: Job posting text

    Returns:
        Dictionary with 'min' and 'max' salary or None if not found
    """
    text_lower = text.lower()

    # Try direct dollar pattern first: $50k - $100k
    dollar_matches = re.findall(r"\$[\d,]+", text_lower)
    if dollar_matches:
        amounts = [int(match.replace("$", "").replace(",", "")) for match in dollar_matches]
        if len(amounts) >= 2:
            return {"min": min(amounts), "max": max(amounts)}
        elif len(amounts) == 1:
            return {"min": amounts[0], "max": amounts[0]}

    # Try K pattern: 50k-100k, 50k per year
    k_pattern = r"(\d+)\s*k(?:\s*[-–]\s*(\d+)\s*k)?(?:\s*(?:per\s+)?year)?(?:\s*(?:annum|per\s+annum))?"
    k_matches = re.findall(k_pattern, text_lower)
    if k_matches:
        for match in k_matches:
            min_k = int(match[0])
            max_k = int(match[1]) if match[1] else min_k
            if max_k > 0:
                return {"min": min_k * 1000, "max": max_k * 1000}

    return None


def detect_interview_stages(text: str) -> List[str]:
    """
    Detect interview stages mentioned in job posting.

    Args:
        text: Job posting text

    Returns:
        List of detected interview stage names
    """
    detected_stages = []
    text_lower = text.lower()

    for stage_name, keywords in INTERVIEW_STAGES.items():
        if any(keyword in text_lower for keyword in keywords):
            detected_stages.append(stage_name)

    # Estimate total rounds if mentioned
    if re.search(r"(\d+)\s*rounds?", text_lower):
        match = re.search(r"(\d+)\s*rounds?", text_lower)
        rounds = int(match.group(1))
        if rounds > len(detected_stages):
            detected_stages.append(f"total_{rounds}_rounds")

    return detected_stages


def estimate_interview_duration(text: str) -> Optional[str]:
    """
    Estimate total interview process duration.

    Args:
        text: Job posting text

    Returns:
        Duration estimate or None
    """
    text_lower = text.lower()

    duration_patterns = [
        (r"(\d+)\s*-\s*(\d+)\s*weeks?", "weeks"),
        (r"(\d+)\s*-\s*(\d+)\s*months?", "months"),
        (r"(\d+)\s*days?", "days"),
    ]

    for pattern, unit in duration_patterns:
        match = re.search(pattern, text_lower)
        if match:
            if unit == "weeks":
                return f"{match.group(1)}-{match.group(2)} weeks"
            elif unit == "months":
                return f"{match.group(1)}-{match.group(2)} months"
            elif unit == "days":
                return f"{match.group(1)} days"

    return None
