# backend/src/contexts/observations/infra/repo.py



from __future__ import annotations

from datetime import datetime
from typing import Optional, Sequence

from sqlalchemy import desc, select
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from .orm import Observation


class ObservationRepo:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, obs: Observation) -> Observation:
        self.session.add(obs)
        self.session.commit()
        self.session.refresh(obs)
        return obs

    def get_latest(self, location_id: int) -> Optional[Observation]:
        stmt = (
            select(Observation)
            .where(Observation.location_id == location_id)
            .order_by(desc(Observation.observed_at))
            .limit(1)
        )
        return self.session.execute(stmt).scalars().first()

    def list_by_location(
        self,
        location_id: int,
        *,
        from_dt: Optional[datetime] = None,
        to_dt: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0,
        newest_first: bool = True,
    ) -> Sequence[Observation]:
        stmt = select(Observation).where(Observation.location_id == location_id)

        if from_dt is not None:
            stmt = stmt.where(Observation.observed_at >= from_dt)
        if to_dt is not None:
            stmt = stmt.where(Observation.observed_at <= to_dt)

        stmt = stmt.order_by(
            desc(Observation.observed_at) if newest_first else Observation.observed_at
        ).offset(offset).limit(limit)

        return list(self.session.execute(stmt).scalars().all())

    def get_by_location_and_observed_at(
        self,
        location_id: int,
        observed_at: datetime,
    ) -> Optional[Observation]:
        stmt = select(Observation).where(
            Observation.location_id == location_id,
            Observation.observed_at == observed_at,
        )
        return self.session.execute(stmt).scalars().first()

    def save_if_not_exists(self, obs: Observation) -> Observation:
        try:
            self.session.add(obs)
            self.session.commit()
            self.session.refresh(obs)
            return obs
        except IntegrityError:
            self.session.rollback()
            existing = self.get_by_location_and_observed_at(obs.location_id, obs.observed_at)
            if existing is None:
                raise
            return existing