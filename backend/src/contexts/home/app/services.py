# src/contexts/home/app/services.py

from __future__ import annotations

from datetime import datetime, timezone

from src.contexts.home.api.schemas import (
    HomeItemDTO,
    HomeResponse,
    LatestObservationDTO,
    LocationDTO,
)
from src.contexts.locations.app.services import get_default_location, list_locations
from src.contexts.locations.domain.repositories import LocationRepository
from src.contexts.observations.domain.repositories import ObservationRepository


def _to_location_dto(loc) -> LocationDTO:
    # loc: LocationEntity
    return LocationDTO(
        id=loc.id,  # type: ignore[arg-type]
        name=loc.name,
        country_code=loc.country_code,
        lat=loc.lat,
        lon=loc.lon,
        is_active=loc.is_active,
        is_featured=loc.is_featured,
        display_order=loc.display_order,
    )


def _to_latest_dto(obs) -> LatestObservationDTO:
    # obs: ObservationEntity
    return LatestObservationDTO(
        observed_at=obs.observed_at,
        temp=obs.temp,
        feels_like=obs.feels_like,
        humidity=obs.humidity,
        pressure=obs.pressure,
        wind_speed=obs.wind_speed,
        weather_main=obs.weather_main,
        weather_desc=obs.weather_desc,
        weather_icon=obs.weather_icon,
        rain_1h=obs.rain_1h,
        snow_1h=obs.snow_1h,
        source=obs.source,
    )


def get_home_view(
    location_repo: LocationRepository,
    obs_repo: ObservationRepository,
) -> HomeResponse:
    """
    Build home view model:
    - default: featured-first fallback among active locations
    - list: active locations excluding default
    - latest: latest observation per location (nullable)
    """
    now = datetime.now(timezone.utc)

    default_loc = get_default_location(location_repo)
    active_locs = list_locations(location_repo, active_only=True)

    default_id = default_loc.id if default_loc else None
    list_locs = [l for l in active_locs if l.id != default_id]

    # latest를 배치로 가져오기 (간단 구현: 내부에서 loc_id별로 호출해도 OK)
    ids = []
    if default_id is not None:
        ids.append(default_id)
    ids.extend([l.id for l in list_locs if l.id is not None])

    latest_map = obs_repo.get_latest_for_location_ids(ids)

    # default item
    default_item = None
    if default_loc is not None and default_loc.id is not None:
        latest = latest_map.get(default_loc.id)
        default_item = HomeItemDTO(
            location=_to_location_dto(default_loc),
            latest=_to_latest_dto(latest) if latest else None,
        )

    # list items
    items: list[HomeItemDTO] = []
    for loc in list_locs:
        if loc.id is None:
            continue
        latest = latest_map.get(loc.id)
        items.append(
            HomeItemDTO(
                location=_to_location_dto(loc),
                latest=_to_latest_dto(latest) if latest else None,
            )
        )

    return HomeResponse(
        generated_at=now,
        default=default_item,
        list=items,
    )