from typing import List, Optional

from pydantic import BaseModel, Field


class JobPostingInput(BaseModel):
    url: Optional[str] = None
    text: Optional[str] = None


class AnalyzeRequest(BaseModel):
    job_posting: JobPostingInput
    resume_text: Optional[str] = None


class FocusArea(BaseModel):
    name: str
    weight: float
    skills: List[str]


class CritiqueItem(BaseModel):
    severity: str = Field(..., pattern="^(info|warning|critical)$")
    message: str


class AnalyzeResponse(BaseModel):
    title: Optional[str]
    focus_areas: List[FocusArea]
    explicit_skills: List[str]
    hidden_skills: List[str]
    critiques: List[CritiqueItem]
    resume_alignment: Optional[float] = None
    summary: str
