# backend/src/contexts/observations/infra/orm.py

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel


class Observation(SQLModel, table=True):
    __tablename__ = "observations"

    id: Optional[int] = Field(default=None, primary_key=True)

    # FK to locations.id
    location_id: int = Field(foreign_key="locations.id", index=True)

    observed_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )

    temp: float
    feels_like: Optional[float] = None
    humidity: Optional[float] = None
    pressure: Optional[float] = None
    wind_speed: Optional[float] = None

    weather_main: Optional[str] = Field(default=None, max_length=64)
    weather_desc: Optional[str] = Field(default=None, max_length=128)
    weather_icon: Optional[str] = Field(default=None, max_length=8)

    rain_1h: Optional[float] = None
    snow_1h: Optional[float] = None

    source: str = Field(default="openweathermap", max_length=32)

    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    )