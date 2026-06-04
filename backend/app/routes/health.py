from fastapi import APIRouter
from datetime import datetime, timezone

health_router = APIRouter(prefix="/health", tags=["health"])


@health_router.get("")
def health_check():
    """Returns 200 when the service is up."""
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }