# backend/src/contexts/analytics/api/router.py

from fastapi import APIRouter, Depends, Query

from src.contexts.analytics.api.schemas import TemperatureStatsResponse
from src.contexts.analytics.app.services import AnalyticsService
from src.shared.di import get_analytics_service

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
)


@router.get("/temperature-stats", response_model=TemperatureStatsResponse)
def get_temperature_stats(
    location_id: int,
    days: int | None = Query(
        default=None,
        ge=0,
        description="0 means today, N means last N days",
    ),
    service: AnalyticsService = Depends(get_analytics_service),
) -> TemperatureStatsResponse:

    stats = service.get_temperature_stats(
        location_id=location_id,
        days=days,
    )

    return TemperatureStatsResponse(
        location_id=stats.location_id,
        avg_temp=stats.avg_temp,
        min_temp=stats.min_temp,
        max_temp=stats.max_temp,
        count=stats.count,
    )