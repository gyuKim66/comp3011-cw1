"""
Author: Dongwook Kim
Created: 2026-02-24

City API schemas.
"""
from pydantic import BaseModel, Field

class CreateCityRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    latitude: float
    longitude: float

class CityResponse(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float