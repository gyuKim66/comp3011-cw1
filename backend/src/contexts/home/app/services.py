# src/contexts/home/app/services.py


from __future__ import annotations

import os
from datetime import datetime, timezone, timedelta

from sqlmodel import Session

from src.contexts.home.api.schemas import (
    HomeItemDTO,
    HomeResponse,
    LatestObservationDTO,
    LocationDTO,
)
from src.contexts.locations.app.services import get_default_location, list_locations
from src.contexts.locations.domain.repositories import LocationRepository
from src.contexts.observations.domain.repositories import ObservationRepository
from src.contexts.observations.app.services import fetch_and_store_current_observation


HOME_TTL_MINUTES = int(os.getenv("HOME_TTL_MINUTES", "10"))


def _to_location_dto(loc) -> LocationDTO:
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


def _is_stale(observed_at: datetime | None, *, now: datetime) -> bool:
    if observed_at is None:
        return True
    if observed_at.tzinfo is None:
        observed_at = observed_at.replace(tzinfo=timezone.utc)
    return (now - observed_at) > timedelta(minutes=HOME_TTL_MINUTES)


def _refresh_if_needed(
    *,
    session: Session,
    obs_repo: ObservationRepository,
    location_id: int,
    now: datetime,
) -> None:
    latest = obs_repo.get_latest_by_location_id(location_id)
    if latest is None or _is_stale(latest.observed_at, now=now):
        fetch_and_store_current_observation(session, location_id=location_id)


def get_home_view(
    session: Session,
    location_repo: LocationRepository,
    obs_repo: ObservationRepository,
    *,
    refresh: bool = True,
) -> HomeResponse:
    """
    Build home view model:
    - default: featured-first fallback among active locations
    - list: active locations excluding default
    - latest: latest observation per location (nullable)
    - refresh(TTL): if stale/missing, fetch from OWM and store into DB
    """
    now = datetime.now(timezone.utc)

    default_loc = get_default_location(location_repo)
    active_locs = list_locations(location_repo, active_only=True)

    default_id = default_loc.id if default_loc else None
    list_locs = [l for l in active_locs if l.id != default_id]

    ids: list[int] = []
    if default_id is not None:
        ids.append(default_id)
    ids.extend([l.id for l in list_locs if l.id is not None])

    # ✅ TTL 기반 refresh
    if refresh:
        for loc_id in ids:
            _refresh_if_needed(
                session=session,
                obs_repo=obs_repo,
                location_id=loc_id,
                now=now,
            )

    # refresh 후 최신값 batch 로드
    latest_map = obs_repo.get_latest_for_location_ids(ids)

    default_item = None
    if default_loc is not None and default_loc.id is not None:
        latest = latest_map.get(default_loc.id)
        default_item = HomeItemDTO(
            location=_to_location_dto(default_loc),
            latest=_to_latest_dto(latest) if latest else None,
        )

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