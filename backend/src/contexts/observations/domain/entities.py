# backend/src/contexts/observations/domain/entities.py



from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ObservationEntity:
    id: int | None
    location_id: int
    observed_at: datetime
    temp: float
    feels_like: Optional[float]
    humidity: Optional[float]
    pressure: Optional[float]
    wind_speed: Optional[float]
    weather_main: Optional[str]
    weather_desc: Optional[str]
    weather_icon: Optional[str]
    rain_1h: Optional[float]
    snow_1h: Optional[float]
    source: str
    created_at: datetime
    