# backend/src/contexts/analytics/domain/entities.py


from dataclasses import dataclass

@dataclass(frozen=True)
class TemperatureStats:
    location_id: int
    avg_temp: float | None
    min_temp: float | None
    max_temp: float | None
    count: int


@dataclass
class HumidityStats:
    location_id: int
    avg_humidity: float | None
    min_humidity: float | None
    max_humidity: float | None
    count: int


@dataclass(frozen=True)
class TemperatureTrendPoint:
    date: str
    avg_temp: float | None

@dataclass(frozen=True)
class TemperatureTrend:
    location_id: int
    days: int
    data: list[TemperatureTrendPoint]