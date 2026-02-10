"""
Comprehensive test suite for AJIPS services.
Includes unit, integration, and regression tests.
"""

import pytest
from unittest.mock import patch, MagicMock

from ajips.app.api.schemas import AnalyzeRequest, JobPostingInput
from ajips.app.services.enhanced_extraction import (
    extract_salary_range,
    detect_interview_stages,
)
from ajips.app.services.extraction import extract_skills
from ajips.app.services.ingestion import fetch_job_posting
from ajips.core.pipelines.job_profile import build_job_profile


class TestSalaryExtraction:
    """Test salary range extraction."""

    def test_extract_salary_with_dollar_signs(self):
        """Test extraction of salary in format $50,000 - $100,000"""
        text = "Salary: $50,000 - $100,000 per year"
        result = extract_salary_range(text)
        assert result is not None
        assert result["min"] == 50000
        assert result["max"] == 100000

    def test_extract_salary_with_k_notation(self):
        """Test extraction of salary in format 50k-100k"""
        text = "Compensation: 50k - 100k annually"
        result = extract_salary_range(text)
        assert result is not None
        assert result["min"] == 50000
        assert result["max"] == 100000

    def test_extract_salary_not_found(self):
        """Test when no salary information exists"""
        text = "Great opportunity to join our team"
        result = extract_salary_range(text)
        assert result is None

    def test_extract_single_salary(self):
        """Test extraction when only single salary is mentioned"""
        text = "Salary: $75,000"
        result = extract_salary_range(text)
        assert result is not None
        assert result["min"] == 75000
        assert result["max"] == 75000


class TestInterviewDetection:
    """Test interview stage detection."""

    def test_detect_phone_screen(self):
        """Test detection of phone screening stage"""
        text = "Process includes phone screen, coding challenge, and onsite"
        stages = detect_interview_stages(text)
        assert "phone" in stages

    def test_detect_technical_interview(self):
        """Test detection of technical interview"""
        text = "We will conduct a technical assessment and coding challenge"
        stages = detect_interview_stages(text)
        assert "technical" in stages

    def test_detect_multiple_stages(self):
        """Test detection of multiple interview stages"""
        text = """
        Our interview process:
        1. Phone screening
        2. Technical coding challenge
        3. System design round
        4. Team lunch and culture fit
        """
        stages = detect_interview_stages(text)
        assert len(stages) >= 3
        assert "phone" in stages
        assert "technical" in stages

    def test_detect_no_stages(self):
        """Test when no interview stages are mentioned"""
        text = "Join our amazing team!"
        stages = detect_interview_stages(text)
        assert len(stages) == 0


class TestSkillExtraction:
    """Test skill extraction."""

    def test_extract_skills_from_job_title(self):
        """Test extraction of skills from a realistic job title"""
        text = "Senior Python/Django Developer with AWS and Docker experience"
        skills = extract_skills(text)
        assert "python" in [s.lower() for s in skills]
        assert "django" in [s.lower() for s in skills]
        assert len(skills) >= 3

    def test_extract_skills_multiple_languages(self):
        """Test extraction when multiple languages are mentioned"""
        text = "JavaScript, TypeScript, and React expertise required"
        skills = extract_skills(text)
        skill_names = [s.lower() for s in skills]
        assert any("javascript" in s for s in skill_names)
        assert any("react" in s for s in skill_names)

    def test_extract_minimum_skills(self):
        """Test regression: realistic job postings have minimum skills"""
        test_jobs = [
            "Senior Python Developer",
            "JavaScript React Engineer",
            "DevOps AWS Engineer",
        ]
        for job_text in test_jobs:
            skills = extract_skills(job_text)
            assert len(skills) >= 2, f"Failed for: {job_text}"


class TestInputValidation:
    """Test input validation."""

    def test_validate_empty_job_posting(self):
        """Test that empty job posting is rejected"""
        with pytest.raises(ValueError):
            AnalyzeRequest(job_posting=JobPostingInput(url=None, text=None))

    def test_validate_short_text(self):
        """Test that very short text is rejected"""
        with pytest.raises(ValueError):
            AnalyzeRequest(job_posting=JobPostingInput(text="Too short"))

    def test_validate_oversized_text(self):
        """Test that oversized text is rejected"""
        huge_text = "x" * 60000
        with pytest.raises(ValueError):
            AnalyzeRequest(job_posting=JobPostingInput(text=huge_text))

    def test_validate_valid_request(self):
        """Test that valid request passes validation"""
        request = AnalyzeRequest(
            job_posting=JobPostingInput(
                text="Senior Python developer with 5+ years experience required for this role"
            )
        )
        assert request is not None


class TestFetchResilience:
    """Test URL fetching resilience."""

    @patch("ajips.app.services.ingestion.requests.get")
    def test_fetch_timeout_handling(self, mock_get):
        """Test handling of request timeout"""
        import requests

        mock_get.side_effect = requests.Timeout("Connection timeout")
        with pytest.raises(ValueError):
            fetch_job_posting("https://example.com/job/123")

    @patch("ajips.app.services.ingestion.requests.get")
    def test_fetch_http_error_handling(self, mock_get):
        """Test handling of HTTP errors"""
        import requests

        response = MagicMock()
        response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
        mock_get.return_value = response
        with pytest.raises(ValueError):
            fetch_job_posting("https://example.com/notfound")

    @patch("ajips.app.services.ingestion.requests.get")
    def test_fetch_successful(self, mock_get):
        """Test successful URL fetch"""
        from bs4 import BeautifulSoup

        response = MagicMock()
        response.text = "<html><body>Python developer job posting</body></html>"
        mock_get.return_value = response

        result = fetch_job_posting("https://example.com/job/123")
        assert result is not None
        assert "python" in result.lower() or "developer" in result.lower()


class TestEndToEnd:
    """End-to-end integration tests."""

    def test_analyze_realistic_job_posting(self):
        """Test analysis of a realistic job posting"""
        job_text = """
        Senior Full-Stack Developer - Remote
        
        We are looking for a Senior Full-Stack Developer with:
        - 5+ years experience with Python, Django, and FastAPI
        - 3+ years with React, TypeScript, and modern frontend tools
        - AWS and Docker experience essential
        - PostgreSQL and Redis proficiency
        - Agile/Scrum experience
        
        We offer:
        - Competitive salary: $120,000-$160,000
        - Remote work flexibility
        - Comprehensive benefits
        
        Interview process:
        1. Phone screening
        2. Technical coding challenge
        3. System design round
        4. Final interview with team
        
        Apply now!
        """

        request = AnalyzeRequest(job_posting=JobPostingInput(text=job_text))
        result = build_job_profile(request)

        # Verify key components
        assert result.explicit_skills
        assert len(result.explicit_skills) >= 5
        assert result.focus_areas
        assert result.title or result.explicit_skills  # Either title or skills
        assert result.interview_stages  # Should detect interview stages
        assert result.salary_range  # Should extract salary

    def test_analyze_entry_level_job(self):
        """Test analysis of entry-level position"""
        job_text = """
        Junior Python Developer

        Entry-level position for recent graduates:
        - Knowledge of Python and Django
        - Understanding of SQL databases
        - Git version control
        - Willing to learn and grow
        
        Location: New York, NY
        Salary: $50,000-$60,000
        """

        request = AnalyzeRequest(job_posting=JobPostingInput(text=job_text))
        result = build_job_profile(request)

        assert result.explicit_skills
        assert result.salary_range
        assert len(result.critiques) >= 0


@pytest.mark.parametrize(
    "job_text",
    [
        "Senior Python/Django Developer with AWS",
        "JavaScript/React/Node.js Full Stack Engineer",
        "Data Scientist - Python, TensorFlow, AWS",
    ],
)
def test_skill_extraction_parametrized(job_text):
    """Parametrized test for skill extraction accuracy"""
    skills = extract_skills(job_text)
    assert len(skills) >= 2, f"Insufficient skills extracted from: {job_text}"
