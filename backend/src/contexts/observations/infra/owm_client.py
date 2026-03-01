# backend/src/contexts/observations/infra/owm_client.py



from __future__ import annotations

import os
from typing import Any, Optional

import httpx


class OpenWeatherMapError(RuntimeError):
    pass


class OpenWeatherMapAuthError(OpenWeatherMapError):
    pass


class OpenWeatherMapRateLimitError(OpenWeatherMapError):
    pass


class OpenWeatherMapUpstreamError(OpenWeatherMapError):
    pass


class OpenWeatherMapClient:
    """
    Minimal OpenWeatherMap client for Current Weather API.
    - Fetches current observation by coordinates (lat/lon)
    - Returns raw JSON dict (mapping is handled in service layer)
    """

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        units: Optional[str] = None,
        lang: Optional[str] = None,
        timeout_seconds: float = 10.0,
    ) -> None:
        self.api_key = api_key or os.getenv("OPENWEATHER_API_KEY")
        if not self.api_key:
            raise OpenWeatherMapAuthError("OPENWEATHER_API_KEY is missing")

        self.base_url = (base_url or os.getenv("OPENWEATHER_BASE_URL") or "https://api.openweathermap.org/data/2.5").rstrip(
            "/"
        )
        self.units = units or os.getenv("OPENWEATHER_UNITS") or "metric"
        self.lang = lang or os.getenv("OPENWEATHER_LANG") or "kr"
        self.timeout_seconds = timeout_seconds

    def fetch_current(self, *, lat: float, lon: float) -> dict[str, Any]:
        """
        Current Weather API:
        GET /weather?lat={lat}&lon={lon}&appid={key}&units={units}&lang={lang}
        """
        url = f"{self.base_url}/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": self.units,
            "lang": self.lang,
        }

        try:
            with httpx.Client(timeout=self.timeout_seconds) as client:
                resp = client.get(url, params=params)
        except httpx.TimeoutException as e:
            raise OpenWeatherMapUpstreamError("OpenWeatherMap request timed out") from e
        except httpx.HTTPError as e:
            raise OpenWeatherMapUpstreamError("OpenWeatherMap request failed") from e

        if resp.status_code == 401:
            raise OpenWeatherMapAuthError("OpenWeatherMap unauthorized (check API key)")
        if resp.status_code == 429:
            raise OpenWeatherMapRateLimitError("OpenWeatherMap rate limit exceeded")
        if 500 <= resp.status_code <= 599:
            raise OpenWeatherMapUpstreamError(f"OpenWeatherMap server error: {resp.status_code}")

        # Other non-2xx
        if resp.is_error:
            raise OpenWeatherMapError(f"OpenWeatherMap error: {resp.status_code} - {resp.text}")

        data = resp.json()
        if not isinstance(data, dict):
            raise OpenWeatherMapError("Unexpected OpenWeatherMap response shape (expected JSON object)")
        return data


def fetch_current_weather(lat: float, lon: float) -> dict[str, Any]:
    """
    Convenience function (keeps calling code short).
    Uses env vars: OPENWEATHER_API_KEY, OPENWEATHER_BASE_URL, OPENWEATHER_UNITS, OPENWEATHER_LANG
    """
    return OpenWeatherMapClient().fetch_current(lat=lat, lon=lon)