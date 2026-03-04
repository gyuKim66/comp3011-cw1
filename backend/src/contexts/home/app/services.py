# backend/src/contexts/home/app/services.py


from __future__ import annotations

from datetime import datetime, timezone

from src.contexts.home.api.schemas import HomeResponse, HomeItemDTO, LocationDTO, LatestObservationDTO
from src.contexts.locations.app.services import list_locations
from src.contexts.observations.domain.entities import ObservationEntity


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


def get_home_view(
    *,
    session,
    location_repo,
    obs_repo,
    refresh: bool,
) -> HomeResponse:
    # ✅ 1) active locations 가져오기 (정렬 포함)
    locations = list_locations(location_repo, active_only=True)

    generated_at = datetime.now(timezone.utc)

    if not locations:
        return HomeResponse(generated_at=generated_at, featured=[], list=[])

    # ✅ 2) 각 location의 latest observation 가져오기 (batch)
    loc_ids = [l.id for l in locations if l.id is not None]
    latest_map = obs_repo.get_latest_for_location_ids(loc_ids)

    # ✅ 3) HomeItemDTO 리스트 조립
    items: list[HomeItemDTO] = []
    for loc in locations:
        if loc.id is None:
            continue
        latest = latest_map.get(loc.id)
        items.append(
            HomeItemDTO(
                location=_to_location_dto(loc),
                latest=_to_latest_dto(latest),
            )
        )

    # ✅ 4) featured 2개 구성: is_featured 우선 + 부족하면 앞에서 채움
    featured: list[HomeItemDTO] = []

    featured_candidates = [x for x in items if x.location.is_featured]
    featured_candidates.sort(key=lambda x: (x.location.display_order, x.location.name))

    for x in featured_candidates:
        if len(featured) >= 2:
            break
        featured.append(x)

    if len(featured) < 2:
        for x in items:
            if len(featured) >= 2:
                break
            if any(f.location.id == x.location.id for f in featured):
                continue
            featured.append(x)

    featured_ids = {x.location.id for x in featured}
    rest = [x for x in items if x.location.id not in featured_ids]

    return HomeResponse(
        generated_at=generated_at,
        featured=featured,
        list=rest,
    )