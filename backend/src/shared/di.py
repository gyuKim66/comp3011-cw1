# backend/src/shared/di.py



from __future__ import annotations

from fastapi import Depends
from sqlmodel import Session

from src.shared.db.session import get_session

from src.contexts.locations.domain.repositories import LocationRepository
from src.contexts.locations.infra.repo import SqlLocationRepository

from src.contexts.observations.domain.repositories import ObservationRepository
from src.contexts.observations.infra.repo import SqlObservationRepository

from src.contexts.analytics.domain.repositories import AnalyticsRepository
from src.contexts.analytics.infra.repo import SqlAnalyticsRepository
from src.contexts.analytics.app.services import AnalyticsService


def get_location_repo(
    session: Session = Depends(get_session),
) -> LocationRepository:
    return SqlLocationRepository(session)


def get_observation_repo(
    session: Session = Depends(get_session),
) -> ObservationRepository:
    return SqlObservationRepository(session)

def get_analytics_repo(
    session: Session = Depends(get_session),
) -> AnalyticsRepository:
    return SqlAnalyticsRepository(session)

def get_analytics_service(
    analytics_repo: AnalyticsRepository = Depends(get_analytics_repo),
    location_repo: LocationRepository = Depends(get_location_repo),
) -> AnalyticsService:
    return AnalyticsService(
        analytics_repo=analytics_repo,
        location_repo=location_repo,
    )