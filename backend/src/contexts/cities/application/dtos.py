"""
Author: Dongwook Kim
Created: 2026-02-24

Cities application DTOs.
"""

from pydantic import BaseModel, Field


class CreateCityDTO(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    latitude: float
    longitude: float


class CityDTO(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
