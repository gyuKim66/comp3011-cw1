# src/contexts/locations/infra/orm.py

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, func
from sqlmodel import SQLModel, Field


class Location(SQLModel, table=True):
    __tablename__ = "locations"

    id: Optional[int] = Field(default=None, primary_key=True)

    name: str
    country_code: str

    lat: float
    lon: float

    is_active: bool = Field(default=True)
    is_featured: bool = Field(default=False)
    display_order: int = Field(default=0)

    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    )