# src/contexts/home/api/router.py


from __future__ import annotations

from fastapi import APIRouter, Depends

from src.contexts.home.app.services import get_home_view
from src.contexts.locations.domain.repositories import LocationRepository
from src.contexts.observations.domain.repositories import ObservationRepository
from src.shared.di import get_location_repo, get_observation_repo

router = APIRouter(prefix="/home", tags=["home"])


@router.get("", response_model=dict)  # response_model은 다음에 HomeResponse로 바꿔도 됨
def home(
    location_repo: LocationRepository = Depends(get_location_repo),
    obs_repo: ObservationRepository = Depends(get_observation_repo),
):
    return get_home_view(location_repo, obs_repo).model_dump()