# backend/src/contexts/observations/app/services.py



from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from sqlmodel import Session

from src.contexts.locations.infra.orm import Location
from src.contexts.observations.infra.orm import Observation
from src.contexts.observations.infra.owm_client import (
    OpenWeatherMapClient,
    OpenWeatherMapError,
)
from src.contexts.observations.infra.repo import ObservationRepo


class ObservationNotFoundError(RuntimeError):
    pass


class LocationNotFoundError(RuntimeError):
    pass


def _to_utc_datetime_from_unix(ts: int) -> datetime:
    return datetime.fromtimestamp(ts, tz=timezone.utc)


def _get_nested(d: dict[str, Any], *keys: str) -> Optional[Any]:
    cur: Any = d
    for k in keys:
        if not isinstance(cur, dict) or k not in cur:
            return None
        cur = cur[k]
    return cur


def _map_owm_current_to_observation(
    *,
    location_id: int,
    data: dict[str, Any],
    source: str = "openweathermap",
) -> Observation:
    dt_unix = data.get("dt")
    if not isinstance(dt_unix, int):
        raise ObservationNotFoundError("OpenWeatherMap response missing 'dt' (timestamp)")

    main = data.get("main") if isinstance(data.get("main"), dict) else {}
    temp = main.get("temp")
    if not isinstance(temp, (int, float)):
        raise ObservationNotFoundError("OpenWeatherMap response missing 'main.temp'")

    weather0: dict[str, Any] = {}
    weather = data.get("weather")
    if isinstance(weather, list) and weather and isinstance(weather[0], dict):
        weather0 = weather[0]

    wind = data.get("wind") if isinstance(data.get("wind"), dict) else {}
    rain = data.get("rain") if isinstance(data.get("rain"), dict) else {}
    snow = data.get("snow") if isinstance(data.get("snow"), dict) else {}

    return Observation(
        location_id=location_id,
        observed_at=_to_utc_datetime_from_unix(dt_unix),
        temp=float(temp),
        feels_like=_coerce_float(main.get("feels_like")),
        humidity=_coerce_float(main.get("humidity")),
        pressure=_coerce_float(main.get("pressure")),
        wind_speed=_coerce_float(wind.get("speed")),
        weather_main=_coerce_str(weather0.get("main")),
        weather_desc=_coerce_str(weather0.get("description")),
        weather_icon=_coerce_str(weather0.get("icon")),
        rain_1h=_coerce_float(rain.get("1h")),
        snow_1h=_coerce_float(snow.get("1h")),
        source=source,
    )


def _coerce_float(v: Any) -> Optional[float]:
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    return None


def _coerce_str(v: Any) -> Optional[str]:
    if v is None:
        return None
    if isinstance(v, str) and v.strip() != "":
        return v
    return None


def fetch_and_store_current_observation(
    session: Session,
    *,
    location_id: int,
    client: Optional[OpenWeatherMapClient] = None,
) -> Observation:
    """
    Use-case:
    1) Load Location by id
    2) Fetch current weather from OpenWeatherMap
    3) Map response -> Observation
    4) Save with unique constraint (location_id, observed_at)
    """
    location = session.get(Location, location_id)
    if location is None:
        raise LocationNotFoundError(f"Location not found: id={location_id}")

    owm_client = client or OpenWeatherMapClient()

    try:
        data = owm_client.fetch_current(lat=location.lat, lon=location.lon)
    except OpenWeatherMapError:
        # Let API layer decide how to convert to HTTP response / message
        raise

    obs = _map_owm_current_to_observation(location_id=location_id, data=data)

    repo = ObservationRepo(session)
    saved = repo.save_if_not_exists(obs)
    return saved