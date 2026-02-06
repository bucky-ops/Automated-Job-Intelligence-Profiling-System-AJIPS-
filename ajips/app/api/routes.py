from fastapi import APIRouter

from ajips.app.api.schemas import AnalyzeRequest, AnalyzeResponse
from ajips.core.pipelines.job_profile import build_job_profile

router = APIRouter()


@router.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_job_posting(payload: AnalyzeRequest) -> AnalyzeResponse:
    profile = build_job_profile(payload)
    return profile
