"""
Author: Dongwook Kim
Created: 2026-02-24

Top-level API router (no business logic here).
"""

from fastapi import APIRouter

from src.contexts.cities.interface.router import router as cities_router
from src.contexts.weather.interface.router import router as weather_router

api_router = APIRouter()
api_router.include_router(cities_router, prefix="/cities", tags=["cities"])
api_router.include_router(weather_router, prefix="/weather", tags=["weather"])


@api_router.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}
