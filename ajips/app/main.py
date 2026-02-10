import os
import time
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from slowapi import Limiter
from slowapi.util import get_remote_address

from ajips.app.api.routes import router as api_router
from ajips.core.logging_config import setup_logging

# Setup logging
logger = setup_logging("ajips")
logger.info("Initializing AJIPS application")

app = FastAPI(
    title="AJIPS - Automated Job Intelligence Profiling System",
    version="1.0.0",
    description="Analyze job postings with AI-powered insights",
)

# Store app startup time
app.state.startup_time = time.time()

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# CORS Configuration
default_origins = ["http://127.0.0.1:8000", "http://localhost:8000"]
origins_env = os.getenv("AJIPS_ALLOWED_ORIGINS")
allowed_origins = (
    [origin.strip() for origin in origins_env.split(",")] if origins_env else default_origins
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests and responses."""
    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(
            f"Request completed",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status": response.status_code,
                "duration_ms": round(process_time * 1000, 2),
            },
        )
        response.headers["X-Response-Time"] = str(process_time)
        response.headers["X-Request-ID"] = getattr(request.state, "request_id", "unknown")
        return response
    except Exception as exc:
        logger.error(f"Request failed", extra={"path": request.url.path, "error": str(exc)})
        raise


# Include API routes
app.include_router(api_router)

# Serve static files (UI)
ui_path = Path(__file__).parent.parent / "ui"
if ui_path.exists():
    app.mount("/static", StaticFiles(directory=str(ui_path)), name="static")

    @app.get("/")
    async def serve_ui():
        """Serve the main UI page"""
        return FileResponse(str(ui_path / "index.html"))
