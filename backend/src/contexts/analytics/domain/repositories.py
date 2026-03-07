# backend/src/contexts/analytics/domain/repositories.py


from typing import Protocol

from src.contexts.analytics.domain.entities import TemperatureStats


class AnalyticsRepository(Protocol):
    def get_temperature_stats(
        self,
        location_id: int,
        days: int | None = None,
    ) -> TemperatureStats:
        ...