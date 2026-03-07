# backend/src/contexts/analytics/domain/repositories.py


from typing import Protocol

from src.contexts.analytics.domain.entities import (
    TemperatureStats, 
    HumidityStats,
    TemperatureTrend,
)


class AnalyticsRepository(Protocol):
    def get_temperature_stats(
        self,
        location_id: int,
        days: int | None = None,
    ) -> TemperatureStats:
        ...

    
    def get_humidity_stats(
        self,
        location_id: int,
        days: int | None = None,
    ) -> HumidityStats:
        ...

    
    def get_temperature_trend(
        self,
        location_id: int,
        days: int,
    ) -> TemperatureTrend:
        ...