"""
Author: Dongwook Kim
Created: 2026-02-24

Location APP Services
"""

from __future__ import annotations

from src.contexts.locations.domain.entities import LocationEntity
from src.contexts.locations.domain.repositories import LocationRepository


def create_location(
    repo: LocationRepository,
    name: str,
    country_code: str,
    lat: float,
    lon: float,
    *,
    is_featured: bool = False,
    display_order: int = 0,
    is_active: bool = True,
) -> LocationEntity:
    loc = LocationEntity(
        id=None,
        name=name,
        country_code=country_code,
        lat=lat,
        lon=lon,
        is_active=is_active,
        is_featured=is_featured,
        display_order=display_order,
    )
    return repo.create(loc)


def list_locations(repo: LocationRepository) -> list[LocationEntity]:
    return repo.list()


def get_location(repo: LocationRepository, location_id: int) -> LocationEntity | None:
    return repo.get(location_id)