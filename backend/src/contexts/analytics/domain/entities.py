# backend/src/contexts/analytics/domain/entities.py

from dataclasses import dataclass


@dataclass(frozen=True)
class TemperatureStats:
    """
    Domain model representing temperature statistics for a location.
    """

    location_id: int
    avg_temp: float | None
    min_temp: float | None
    max_temp: float | None
    count: int