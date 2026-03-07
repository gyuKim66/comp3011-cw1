# backend/src/contexts/analytics/api/router.py

from fastapi import APIRouter, Depends, Query

from src.contexts.analytics.api.schemas import (
    TemperatureStatsResponse,
    HumidityStatsResponse,
    TemperatureTrendResponse,
    TemperatureTrendPointResponse,
)
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


@router.get("/humidity-stats", response_model=HumidityStatsResponse)
def get_humidity_stats(
    location_id: int,
    days: int | None = Query(
        default=None,
        ge=0,
        description="0 means today, N means last N days",
    ),
    service: AnalyticsService = Depends(get_analytics_service),
) -> HumidityStatsResponse:

    stats = service.get_humidity_stats(
        location_id=location_id,
        days=days,
    )

    return HumidityStatsResponse(
        location_id=stats.location_id,
        avg_humidity=stats.avg_humidity,
        min_humidity=stats.min_humidity,
        max_humidity=stats.max_humidity,
        count=stats.count,
    )


@router.get("/temperature-trend", response_model=TemperatureTrendResponse)
def get_temperature_trend(
    location_id: int,
    days: int = Query(
        ...,
        gt=0,
        description="Number of days to include in the trend",
    ),
    service: AnalyticsService = Depends(get_analytics_service),
) -> TemperatureTrendResponse:

    trend = service.get_temperature_trend(
        location_id=location_id,
        days=days,
    )

    return TemperatureTrendResponse(
        location_id=trend.location_id,
        days=trend.days,
        data=[
            TemperatureTrendPointResponse(
                date=point.date,
                avg_temp=point.avg_temp,
            )
            for point in trend.data
        ],
    )