# src/contexts/locations/app/services.py

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


def list_locations(repo: LocationRepository, featured: bool | None = None):
    locations = repo.list()

    if featured is True:
        locations = [l for l in locations if l.is_featured]

    return locations


def get_location(repo: LocationRepository, location_id: int) -> LocationEntity | None:
    return repo.get(location_id)


def get_default_location(repo: LocationRepository) -> LocationEntity | None:
    locations = repo.list()

    # active만
    active = [l for l in locations if l.is_active]
    if not active:
        return None

    # featured 우선
    featured = [l for l in active if l.is_featured]
    pool = featured if featured else active

    # display_order(우선), name(동률 안정화)
    pool.sort(key=lambda l: (l.display_order, l.name))
    return pool[0]