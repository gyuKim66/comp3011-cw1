"""
Author: Dongwook Kim
Created: 2026-02-24

Location API schemas.
"""

from pydantic import BaseModel, Field


class CreateLocationRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    country_code: str = Field(min_length=2, max_length=2, description="ISO 3166-1 alpha-2, e.g., GB, KR")
    lat: float
    lon: float

    is_featured: bool = False
    display_order: int = 0
    is_active: bool = True


class LocationResponse(BaseModel):
    id: int
    name: str
    country_code: str
    lat: float
    lon: float

    is_featured: bool
    display_order: int
    is_active: bool