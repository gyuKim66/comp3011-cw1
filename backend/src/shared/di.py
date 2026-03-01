# backend/src/shared/di.py



from __future__ import annotations

from fastapi import Depends
from sqlmodel import Session

from src.shared.db.session import get_session

from src.contexts.locations.domain.repositories import LocationRepository
from src.contexts.locations.infra.repo import SqlLocationRepository

from src.contexts.observations.domain.repositories import ObservationRepository
from src.contexts.observations.infra.repo import SqlObservationRepository


def get_location_repo(
    session: Session = Depends(get_session),
) -> LocationRepository:
    return SqlLocationRepository(session)


def get_observation_repo(
    session: Session = Depends(get_session),
) -> ObservationRepository:
    return SqlObservationRepository(session)