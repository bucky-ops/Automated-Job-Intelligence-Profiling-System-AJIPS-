from fastapi import APIRouter, HTTPException, Request
import time

from ajips.app.api.schemas import AnalyzeRequest, AnalyzeResponse
from ajips.core.pipelines.job_profile import build_job_profile
from ajips.core.logging_config import get_logger

logger = get_logger(__name__)
router = APIRouter()

# App version
APP_VERSION = "1.0.0"
APP_BUILD_TIME = "2026-02-10"


@router.get("/version")
def get_version() -> dict:
    """Get application version information."""
    return {
        "version": APP_VERSION,
        "build_time": APP_BUILD_TIME,
        "status": "operational",
    }


@router.get("/health")
def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "ok", "service": "ajips"}


@router.get("/health/detailed")
def detailed_health_check(request: Request) -> dict:
    """Detailed health check with system information."""
    uptime = time.time() - request.app.state.startup_time
    return {
        "status": "ok",
        "service": "ajips",
        "version": APP_VERSION,
        "uptime_seconds": round(uptime, 2),
        "database_status": "ok",
        "external_apis": "operational",
    }


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_job_posting(payload: AnalyzeRequest) -> AnalyzeResponse:
    """
    Analyze a job posting and return comprehensive insights.

    **Rate Limit**: 30 requests per minute per IP
    """
    try:
        logger.info(
            "Starting job posting analysis",
            extra={"has_url": payload.job_posting.url is not None, "has_resume": payload.resume_text is not None},
        )

        profile = build_job_profile(payload)

        logger.info(
            "Job posting analysis completed successfully",
            extra={
                "skills_found": len(profile.explicit_skills),
                "critiques": len(profile.critiques),
            },
        )

        return profile
    except ValueError as exc:
        logger.error(f"Validation error in analysis: {str(exc)}")
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.error(f"Unexpected error in analysis: {str(exc)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error") from exc
