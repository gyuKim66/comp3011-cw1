# backend/src/contexts/analytics/app/services.py

from fastapi import HTTPException

from src.contexts.analytics.domain.entities import TemperatureStats
from src.contexts.analytics.domain.repositories import AnalyticsRepository
from src.contexts.locations.domain.repositories import LocationRepository


class AnalyticsService:
    def __init__(
        self,
        analytics_repo: AnalyticsRepository,
        location_repo: LocationRepository,
    ) -> None:
        self.analytics_repo = analytics_repo
        self.location_repo = location_repo

    def get_temperature_stats(
        self,
        location_id: int,
        days: int | None = None,
    ) -> TemperatureStats:
        location = self.location_repo.get(location_id)

        if location is None or not location.is_active:
            raise HTTPException(status_code=404, detail="Location not found")

        return self.analytics_repo.get_temperature_stats(
            location_id=location_id,
            days=days,
        )