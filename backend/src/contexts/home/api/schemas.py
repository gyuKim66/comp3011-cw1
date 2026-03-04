# backend/src/contexts/home/api/schemas.py


from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class LocationDTO(BaseModel):
    id: int
    name: str
    country_code: str
    lat: float
    lon: float
    is_active: bool
    is_featured: bool
    display_order: int


class LatestObservationDTO(BaseModel):
    observed_at: datetime
    temp: float
    feels_like: Optional[float] = None
    humidity: Optional[float] = None
    pressure: Optional[float] = None
    wind_speed: Optional[float] = None
    weather_main: Optional[str] = None
    weather_desc: Optional[str] = None
    weather_icon: Optional[str] = None
    rain_1h: Optional[float] = None
    snow_1h: Optional[float] = None
    source: str


class HomeItemDTO(BaseModel):
    location: LocationDTO
    latest: Optional[LatestObservationDTO] = None


class HomeResponse(BaseModel):
    generated_at: datetime
    featured: list[HomeItemDTO]   # ✅ 최대 2개
    list: list[HomeItemDTO]