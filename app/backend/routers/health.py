from fastapi import APIRouter
from app.backend.core.config import settings

router = APIRouter(prefix="/health", tags=["health"])

@router.get("")
def health():
    return {"status": "ok", "env": settings.env}