from app.backend.routers.ingest import router as ingest_router
from app.backend.routers.health import router as health_router
from fastapi import FastAPI

app = FastAPI(title="Ads LLM Insights API", version="0.1.0")
app.include_router(health_router)
app.include_router(ingest_router)