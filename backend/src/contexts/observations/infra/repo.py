# backend/src/contexts/observations/infra/repo.py



from __future__ import annotations

from datetime import datetime
from typing import Iterable, Optional, Sequence

from sqlalchemy import desc, select
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from .orm import Observation

from src.contexts.observations.domain.repositories import ObservationRepository
from src.contexts.observations.domain.entities import ObservationEntity


class SqlObservationRepository(ObservationRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_entity(self, orm: Observation) -> ObservationEntity:
        return ObservationEntity(
            id=orm.id,
            location_id=orm.location_id,
            observed_at=orm.observed_at,
            temp=orm.temp,
            feels_like=orm.feels_like,
            humidity=orm.humidity,
            pressure=orm.pressure,
            wind_speed=orm.wind_speed,
            weather_main=orm.weather_main,
            weather_desc=orm.weather_desc,
            weather_icon=orm.weather_icon,
            rain_1h=orm.rain_1h,
            snow_1h=orm.snow_1h,
            source=orm.source,
            created_at=orm.created_at,
        )

    def get_latest_by_location_id(
        self, location_id: int
    ) -> ObservationEntity | None:
        stmt = (
            select(Observation)
            .where(Observation.location_id == location_id)
            .order_by(desc(Observation.observed_at))
            .limit(1)
        )
        orm = self.session.execute(stmt).scalars().first()
        if orm is None:
            return None
        return self._to_entity(orm)

    def get_latest_for_location_ids(
        self, location_ids: Iterable[int]
    ) -> dict[int, ObservationEntity]:
        result: dict[int, ObservationEntity] = {}
        for loc_id in location_ids:
            latest = self.get_latest_by_location_id(loc_id)
            if latest is not None:
                result[loc_id] = latest
        return result

    # 이하 write/기타 메서드는 그대로 유지 가능
    def save(self, obs: Observation) -> Observation:
        self.session.add(obs)
        self.session.commit()
        self.session.refresh(obs)
        return obs

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
            existing = self.get_by_location_and_observed_at(
                obs.location_id, obs.observed_at
            )
            if existing is None:
                raise
            return existing