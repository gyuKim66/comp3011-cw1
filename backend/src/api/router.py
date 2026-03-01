# backend/src/api/router.py



from fastapi import APIRouter

from src.contexts.home.api.router import router as home_router
from src.contexts.locations.api.router import router as locations_router
from src.contexts.observations.api.router import router as observations_router
# from src.contexts.analytics.api.router import router as analytics_router

api_router = APIRouter()

api_router.include_router(home_router)
api_router.include_router(locations_router)
api_router.include_router(observations_router)


@api_router.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}
