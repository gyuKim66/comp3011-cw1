# src/contexts/locations/api/schemas.py
# Location API schemas.


from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional


class CreateLocationRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    country_code: str = Field(min_length=2, max_length=2, description="ISO 3166-1 alpha-2, e.g., GB, KR")
    lat: float
    lon: float

    is_featured: bool = False
    is_active: bool = True

    display_order: Optional[int] = None
    

class LocationResponse(BaseModel):
    id: int
    name: str
    country_code: str
    lat: float
    lon: float

    is_featured: bool
    display_order: int
    is_active: bool


class UpdateLocationRequest(BaseModel):
    is_featured: Optional[bool] = None
    is_active: Optional[bool] = None
    display_order: Optional[int] = None


class LocationSearchItem(BaseModel):
    name: str
    country_code: str
    lat: float
    lon: float
    state: str | None = None