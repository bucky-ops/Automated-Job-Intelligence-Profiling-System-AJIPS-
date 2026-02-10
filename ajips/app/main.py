import logging
import os
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from ajips.app.api.routes import router as api_router
from ajips.app.config import settings

# Configure logging based on LOG_FORMAT env var (json or text)
logger = logging.getLogger()
logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
logHandler = logging.StreamHandler()
if settings.LOG_FORMAT.lower() == "json":
    from pythonjsonlogger import jsonlogger

    formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(name)s %(levelname)s %(message)s"
    )
else:
    formatter = logging.Formatter(fmt="%(asctime)s %(name)s %(levelname)s %(message)s")
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION,
)

# CORS configuration from environment
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# Include API routes
app.include_router(api_router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    import time

    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    logger.info(
        "request_processed",
        extra={
            "method": request.method,
            "url": str(request.url),
            "status_code": response.status_code,
            "process_time_ms": round(process_time, 2),
            "client_ip": request.client.host if request.client else None,
        },
    )
    return response


# Serve static files (UI)
ui_path = Path(__file__).parent.parent / "ui"
if ui_path.exists():
    app.mount("/static", StaticFiles(directory=str(ui_path)), name="static")

    @app.get("/")
    async def serve_ui():
        """Serve the main UI page"""
        return FileResponse(str(ui_path / "index.html"))


@app.get("/version")
def version() -> dict:
    """Version and build info endpoint for health checks."""
    return {"version": settings.API_VERSION, "name": "AJIPS"}
