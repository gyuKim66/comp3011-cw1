# backend/src/contexts/observations/api/router.py



from __future__ import annotations

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from src.shared.db.session import get_session
from src.contexts.observations.app.services import (
    fetch_and_store_current_observation,
    LocationNotFoundError,
    ObservationNotFoundError,
)
from src.contexts.observations.infra.owm_client import (
    OpenWeatherMapAuthError,
    OpenWeatherMapRateLimitError,
    OpenWeatherMapUpstreamError,
    OpenWeatherMapError,
)
from src.contexts.observations.infra.repo import ObservationRepo


router = APIRouter(prefix="/observations", tags=["observations"])


@router.post("/fetch")
def fetch_observation(
    location_id: int = Query(..., description="Location ID"),
    session: Session = Depends(get_session),
):
    """
    Fetch current weather from OpenWeatherMap and store it as an Observation.
    Returns the stored observation (existing one if (location_id, observed_at) already exists).
    """
    try:
        obs = fetch_and_store_current_observation(session, location_id=location_id)
        return obs
    except LocationNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except ObservationNotFoundError as e:
        # Upstream response missing required fields (dt/temp)
        raise HTTPException(status_code=502, detail=str(e)) from e
    except OpenWeatherMapAuthError as e:
        raise HTTPException(status_code=401, detail=str(e)) from e
    except OpenWeatherMapRateLimitError as e:
        raise HTTPException(status_code=429, detail=str(e)) from e
    except OpenWeatherMapUpstreamError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e
    except OpenWeatherMapError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e


@router.get("/latest")
def get_latest_observation(
    location_id: int = Query(..., description="Location ID"),
    session: Session = Depends(get_session),
):
    repo = ObservationRepo(session)
    obs = repo.get_latest(location_id=location_id)
    if obs is None:
        raise HTTPException(status_code=404, detail=f"No observation found for location_id={location_id}")
    return obs


@router.get("")
def list_observations(
    location_id: int = Query(..., description="Location ID"),
    from_dt: Optional[datetime] = Query(None, description="Filter: observed_at >= from_dt (ISO 8601)"),
    to_dt: Optional[datetime] = Query(None, description="Filter: observed_at <= to_dt (ISO 8601)"),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    newest_first: bool = Query(True, description="Order by observed_at desc if true"),
    session: Session = Depends(get_session),
):
    repo = ObservationRepo(session)
    items = repo.list_by_location(
        location_id,
        from_dt=from_dt,
        to_dt=to_dt,
        limit=limit,
        offset=offset,
        newest_first=newest_first,
    )
    return items