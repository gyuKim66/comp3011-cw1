"""
Author: Dongwook Kim
Created: 2026-02-24

Top-level API router (no business logic here).
"""

from fastapi import APIRouter

from src.contexts.locations.api.router import router as cities_router
from src.contexts.observations.api.router import router as observations_router
from src.contexts.analytics.api.router import router as analytics_router

api_router = APIRouter()
api_router.include_router(cities_router, prefix="/cities", tags=["cities"])
api_router.include_router(observations_router, prefix="/weather", tags=["weather"])


@api_router.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}
