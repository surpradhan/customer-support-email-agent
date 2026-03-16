from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from src.core.config import settings
from src.api.router import router as api_router
from src.api.inbox import router as inbox_router

app = FastAPI(
    title="Customer Support Email Agent",
    version="0.1.0",
    description="LangGraph-powered customer support email agent",
)

@app.get("/health")
async def health_check():
    return {"status": "ok", "environment": settings.APP_ENV}


app.include_router(api_router, prefix="/api/v1")
app.include_router(inbox_router, prefix="/api/v1")

# Serve static files (HTML UI) — must be last
static_dir = Path(__file__).resolve().parent.parent / "static"
app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
