# backend/src/contexts/observations/infra/orm.py
"""
Author: Dongwook Kim
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, Float, Index, UniqueConstraint, func
from sqlmodel import Field, SQLModel


class Observation(SQLModel, table=True):
    __tablename__ = "observations"

    __table_args__ = (
        UniqueConstraint("location_id", "observed_at", name="uq_observations_location_observed_at"),
        Index("ix_observations_location_observed_at_desc", "location_id", "observed_at"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)

    # FK to locations.id
    location_id: int = Field(foreign_key="locations.id", index=True)

    observed_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )

    temp: float = Field(sa_column=Column(Float, nullable=False))
    feels_like: Optional[float] = Field(default=None, sa_column=Column(Float, nullable=True))
    humidity: Optional[float] = Field(default=None, sa_column=Column(Float, nullable=True))
    pressure: Optional[float] = Field(default=None, sa_column=Column(Float, nullable=True))
    wind_speed: Optional[float] = Field(default=None, sa_column=Column(Float, nullable=True))

    weather_main: Optional[str] = Field(default=None, max_length=64)
    weather_desc: Optional[str] = Field(default=None, max_length=128)
    weather_icon: Optional[str] = Field(default=None, max_length=8)

    rain_1h: Optional[float] = Field(default=None, sa_column=Column(Float, nullable=True))
    snow_1h: Optional[float] = Field(default=None, sa_column=Column(Float, nullable=True))

    source: str = Field(default="openweathermap", max_length=32)

    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    )