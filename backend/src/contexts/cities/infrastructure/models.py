"""
Author: Dongwook Kim
Created: 2026-02-24

SQLModel tables for Cities.
"""

from typing import Optional
from sqlmodel import SQLModel, Field


class CityModel(SQLModel, table=True):
    __tablename__ = "cities"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    latitude: float
    longitude: float
