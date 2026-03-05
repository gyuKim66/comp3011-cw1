# src/contexts/locations/app/services.py

from __future__ import annotations

from src.contexts.locations.domain.entities import LocationEntity
from src.contexts.locations.domain.repositories import LocationRepository


class DuplicateLocationError(Exception):
    pass


class FeaturedLimitExceeded(Exception):
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

    # ✅ "이미 등록되어 있으면 복구": (name + country_code) 기준으로 찾기
    # - active면 중복(409)
    # - inactive면 is_active=True로 복구하고 값 업데이트 후 반환
    all_locations = list_locations(repo, active_only=False, featured=None)

    existing_same = None
    for l in all_locations:
        if (l.name or "").strip().lower() == clean_name.lower() and (l.country_code or "").upper() == clean_cc:
            existing_same = l
            break

    if existing_same is not None:
        if existing_same.is_active:
            raise DuplicateLocationError("Location already exists")

        # ✅ inactive였던 location 복구
        updater = getattr(repo, "update", None)
        if updater is None:
            raise RuntimeError("Repository does not support update()")

        # display_order 자동 부여(복구 시에도 맨 아래로)
        if display_order is None:
            active_now = list_locations(repo, active_only=True, featured=None)
            max_order = max([l.display_order for l in active_now], default=-1)
            display_order = max_order + 1

        restored = updater(
            existing_same.id,  # type: ignore[arg-type]
            is_active=True,
            is_featured=is_featured,
            display_order=display_order,
        )
        # restored가 None이면 repo가 이상한 상태이므로 방어
        if restored is None:
            raise RuntimeError("Failed to restore location")
        return restored

    # ✅ 새로 만드는 케이스: active locations 기준 max+1
    active_existing = [l for l in all_locations if l.is_active]
    if display_order is None:
        max_order = max([l.display_order for l in active_existing], default=-1)
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


def get_location(repo: LocationRepository, location_id: int) -> LocationEntity | None:
    return repo.get(location_id)


def get_default_location(repo: LocationRepository) -> LocationEntity | None:
    active = list_locations(repo, active_only=True)
    if not active:
        return None
    featured = [l for l in active if l.is_featured]
    pool = featured if featured else active
    return pool[0]


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
        featured_now = [l for l in featured_now if l.id != location_id]
        if len(featured_now) >= 2:
            raise FeaturedLimitExceeded("Featured locations limit is 2")

    updater = getattr(repo, "update", None)
    if updater is None:
        raise RuntimeError("Repository does not support update()")

    # ✅ 소프트 삭제(비활성화)면 featured도 자동 해제 (일관성 유지)
    if is_active is False:
        is_featured = False

    return updater(
        location_id,
        is_featured=is_featured,
        is_active=is_active,
        display_order=display_order,
    )


def soft_delete_location(repo: LocationRepository, location_id: int) -> LocationEntity | None:
    """
    DELETE API에서 사용할 소프트 삭제 헬퍼.
    - is_active=False
    - is_featured=False (update_location에서 자동 처리)
    """
    return update_location(repo, location_id, is_active=False)