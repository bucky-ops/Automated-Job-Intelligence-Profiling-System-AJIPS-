from typing import List, Optional

from pydantic import BaseModel, Field, field_validator, ConfigDict


class JobPostingInput(BaseModel):
    url: Optional[str] = Field(None, description="URL to job posting")
    text: Optional[str] = Field(None, description="Raw job posting text")

    @field_validator("text")
    @classmethod
    def validate_text_length(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if len(v) < 50:
            raise ValueError("Job posting text must be at least 50 characters")
        if len(v) > 50000:
            raise ValueError("Job posting text exceeds 50KB limit")
        return v


class AnalyzeRequest(BaseModel):
    job_posting: JobPostingInput = Field(..., description="Job posting source")
    resume_text: Optional[str] = Field(None, description="Resume for matching analysis", max_length=20000)

    @field_validator("job_posting")
    @classmethod
    def validate_posting_has_content(cls, v: JobPostingInput) -> JobPostingInput:
        if not v.text and not v.url:
            raise ValueError("Provide either job_posting.text or job_posting.url")
        return v

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "job_posting": {
                    "text": "Senior Python Developer - We are looking for a Python/FastAPI expert with 5+ years experience in AWS and Docker..."
                },
                "resume_text": "John Doe - Python Developer with 7 years experience in AWS, Docker, Kubernetes, and Django..."
            }
        }
    )


class FocusArea(BaseModel):
    name: str
    weight: float
    skills: List[str]


class CritiqueItem(BaseModel):
    severity: str = Field(..., pattern="^(info|warning|critical)$", description="Severity level")
    message: str = Field(..., description="Critique message")


class AnalyzeResponse(BaseModel):
    title: Optional[str] = Field(None, description="Extracted job title")
    focus_areas: List[FocusArea] = Field(default_factory=list, description="Primary focus areas")
    explicit_skills: List[str] = Field(default_factory=list, description="Explicitly mentioned skills")
    hidden_skills: List[str] = Field(default_factory=list, description="Inferred skills")
    critiques: List[CritiqueItem] = Field(default_factory=list, description="Job posting critiques")
    salary_range: Optional[dict] = Field(None, description="Extracted salary range")
    interview_stages: List[str] = Field(default_factory=list, description="Detected interview stages")
    quality_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Job posting quality score")
    resume_alignment: Optional[float] = Field(None, description="Resume alignment percentage")
    summary: str = Field(default="", description="Overall analysis summary")
