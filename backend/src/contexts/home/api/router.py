# backend/src/contexts/home/api/router.py

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from src.contexts.home.app.services import get_home_view
from src.contexts.locations.domain.repositories import LocationRepository
from src.contexts.observations.domain.repositories import ObservationRepository
from src.shared.di import get_location_repo, get_observation_repo
from src.shared.db.session import get_session

router = APIRouter(prefix="/home", tags=["home"])


@router.get("", response_model=dict)  # 나중에 HomeResponse로 변경 가능
def home(
    refresh: bool = Query(True),  # TTL 기반 갱신 여부
    session: Session = Depends(get_session),
    location_repo: LocationRepository = Depends(get_location_repo),
    obs_repo: ObservationRepository = Depends(get_observation_repo),
):
    """
    Home endpoint with TTL-based refresh:
    - refresh=True (default): stale or missing observations will be fetched from OWM
    - refresh=False: use DB only
    """
    return get_home_view(
        session=session,
        location_repo=location_repo,
        obs_repo=obs_repo,
        refresh=refresh,
    ).model_dump()