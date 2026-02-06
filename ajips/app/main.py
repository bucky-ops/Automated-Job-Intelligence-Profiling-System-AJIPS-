from fastapi import FastAPI

from ajips.app.api.routes import router as api_router

app = FastAPI(title="AJIPS", version="0.1.0")
app.include_router(api_router)
