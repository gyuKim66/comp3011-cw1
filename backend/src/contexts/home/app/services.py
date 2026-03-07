# backend/src/contexts/home/app/services.py

from __future__ import annotations

from datetime import datetime, timezone, timedelta

from src.contexts.home.api.schemas import (
    HomeResponse,
    HomeItemDTO,
    LocationDTO,
    LatestObservationDTO,
)
from src.contexts.locations.app.services import list_locations
from src.contexts.observations.domain.entities import ObservationEntity

# ✅ 존재하는 함수로 바꾸기
from src.contexts.observations.app.services import fetch_and_store_current_observation

FRESHNESS_MINUTES = 10


def _to_location_dto(loc) -> LocationDTO:
    return LocationDTO(
        id=loc.id or 0,
        name=loc.name,
        country_code=loc.country_code,
        lat=loc.lat,
        lon=loc.lon,
        is_active=loc.is_active,
        is_featured=loc.is_featured,
        display_order=loc.display_order,
    )


def _to_latest_dto(obs: ObservationEntity | None) -> LatestObservationDTO | None:
    if obs is None:
        return None
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


def _is_stale(obs: ObservationEntity | None, *, now: datetime) -> bool:
    if obs is None:
        return True
    return obs.observed_at < (now - timedelta(minutes=FRESHNESS_MINUTES))


def get_home_view(
    *,
    session,
    location_repo,
    obs_repo,
    refresh: bool,
) -> HomeResponse:
    locations = list_locations(location_repo, active_only=True)
    now = datetime.now(timezone.utc)

    if not locations:
        return HomeResponse(generated_at=now, featured=[], list=[])

    loc_ids = [l.id for l in locations if l.id is not None]

    # 1) 현재 latest 읽기
    latest_map = obs_repo.get_latest_for_location_ids(loc_ids)

    # 2) stale 판정 → 갱신 대상 추리기
    stale_ids = [loc_id for loc_id in loc_ids if refresh or _is_stale(latest_map.get(loc_id), now=now)]

    # 3) stale이면 OWM 재조회 후 DB 저장
    if stale_ids:
        for loc_id in stale_ids:
            try:
                fetch_and_store_current_observation(session, location_id=loc_id)
            except Exception:
                # Home은 계속 응답 내려주되, 실패한 location은 기존 latest 유지
                pass

        # 4) 저장 후 latest 다시 읽기
        latest_map = obs_repo.get_latest_for_location_ids(loc_ids)

    # 5) DTO 조립
    items: list[HomeItemDTO] = []
    for loc in locations:
        if loc.id is None:
            continue
        latest = latest_map.get(loc.id)
        items.append(HomeItemDTO(location=_to_location_dto(loc), latest=_to_latest_dto(latest)))

    featured_candidates = [x for x in items if x.location.is_featured]
    featured_candidates.sort(key=lambda x: x.location.display_order)
    featured = featured_candidates[:2]

    featured_ids = {x.location.id for x in featured}
    rest = [x for x in items if x.location.id not in featured_ids]

    return HomeResponse(generated_at=now, featured=featured, list=rest)