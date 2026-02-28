"""
Author: Dongwook Kim
Created: 2026-02-24

Locations domain entities.
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class LocationEntity:
    id: int | None
    name: str
    country_code: str
    lat: float
    lon: float
    is_active: bool = True
    is_featured: bool = False
    display_order: int = 0