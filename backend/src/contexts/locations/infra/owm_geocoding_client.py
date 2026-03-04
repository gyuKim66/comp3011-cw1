# backend/src/contexts/locations/infra/owm_geocoding_client.py


from __future__ import annotations

import os
from typing import Any

import httpx


class OpenWeatherGeocodingClient:
    def __init__(self) -> None:
        api_key = os.getenv("OPENWEATHER_API_KEY") or os.getenv("OWM_API_KEY")
        if not api_key:
            raise RuntimeError("OPENWEATHER_API_KEY (or OWM_API_KEY) is not set")
        self.api_key = api_key

    async def search(self, q: str, limit: int = 5) -> list[dict[str, Any]]:
        url = "https://api.openweathermap.org/geo/1.0/direct"
        params = {"q": q, "limit": limit, "appid": self.api_key}

        async with httpx.AsyncClient(timeout=10.0) as client:
            res = await client.get(url, params=params)
            res.raise_for_status()
            data = res.json()

        # data: list of {name, lat, lon, country, state?}
        return data