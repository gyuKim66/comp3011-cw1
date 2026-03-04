# src/contexts/locations/app/services.py



from __future__ import annotations

from src.contexts.locations.domain.entities import LocationEntity
from src.contexts.locations.domain.repositories import LocationRepository



class DuplicateLocationError(Exception):
    pass


def create_location(
    repo: LocationRepository,
    name: str,
    country_code: str,
    lat: float,
    lon: float,
    *,
    is_featured: bool = False,
    display_order: int | None = None,
    is_active: bool = True,
) -> LocationEntity:
    clean_name = name.strip()
    clean_cc = country_code.strip().upper()

    # ✅ 중복 방지: active location 중 name+country_code 동일하면 막기
    existing = list_locations(repo, active_only=True, featured=None)
    for l in existing:
        if (l.name or "").strip().lower() == clean_name.lower() and (l.country_code or "").upper() == clean_cc:
            raise DuplicateLocationError("Location already exists")

    # ✅ display_order 자동 부여: active locations 중 max+1 (맨 아래)
    if display_order is None:
        max_order = max([l.display_order for l in existing], default=-1)
        display_order = max_order + 1

    loc = LocationEntity(
        id=None,
        name=clean_name,
        country_code=clean_cc,
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
    locations = repo.list()

    if active_only:
        locations = [l for l in locations if l.is_active]
    if featured is True:
        locations = [l for l in locations if l.is_featured]
    elif featured is False:
        locations = [l for l in locations if not l.is_featured]

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



class FeaturedLimitExceeded(Exception):
    pass


def update_location(
    repo: LocationRepository,
    location_id: int,
    *,
    is_featured: bool | None = None,
    is_active: bool | None = None,
    display_order: int | None = None,
) -> LocationEntity | None:
    # ✅ featured=true로 올릴 때 서버에서도 2개 제한 체크
    if is_featured is True:
        featured_now = list_locations(repo, featured=True, active_only=True)
        # 이미 featured인 자기 자신은 카운트에서 제외
        featured_now = [l for l in featured_now if l.id != location_id]
        if len(featured_now) >= 2:
            raise FeaturedLimitExceeded("Featured locations limit is 2")

    # repo.update가 없다면 여기서 구현 불가 → 지금은 repo.update를 추가했으니 사용
    updater = getattr(repo, "update", None)
    if updater is None:
        raise RuntimeError("Repository does not support update()")

    return updater(
        location_id,
        is_featured=is_featured,
        is_active=is_active,
        display_order=display_order,
    )