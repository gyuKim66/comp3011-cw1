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



def list_locations(
    repo: LocationRepository,
    *,
    featured: bool | None = None,
    active_only: bool = True,
):
    """
    List locations with optional filters.

    - active_only=True: return only active locations (default)
    - featured=True: return only featured locations
    - featured=False: return only non-featured locations
    - featured=None: do not filter by featured flag
    Sorting: (display_order, name) for stable UI ordering
    """
    locations = repo.list()

    if active_only:
        locations = [l for l in locations if l.is_active]
    if featured is True:
        locations = [l for l in locations if l.is_featured]
    elif featured is False:
        locations = [l for l in locations if not l.is_featured]

    # 홈/목록에서 순서가 중요하니 정렬도 여기서 통일(선택)
    locations.sort(key=lambda l: (l.display_order, l.name))

    return locations


def get_location(
    repo: LocationRepository, 
    location_id: int
) -> LocationEntity | None:
    return repo.get(location_id)


def get_default_location(repo: LocationRepository) -> LocationEntity | None:
    active = list_locations(repo, active_only=True)  # 정렬까지 포함된 active 리스트
    if not active:
        return None

    featured = [l for l in active if l.is_featured]
    pool = featured if featured else active
    return pool[0]  # 이미 정렬되어 있음