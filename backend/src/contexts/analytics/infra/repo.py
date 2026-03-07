# backend/src/contexts/analytics/infra/repo.py


from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlmodel import Session

from src.contexts.analytics.domain.entities import TemperatureStats
from src.contexts.observations.infra.orm import Observation


class SqlAnalyticsRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_temperature_stats(
        self,
        location_id: int,
        days: int | None = None,
    ) -> TemperatureStats:
        stmt = (
            select(
                func.avg(Observation.temp).label("avg_temp"),
                func.min(Observation.temp).label("min_temp"),
                func.max(Observation.temp).label("max_temp"),
                func.count(Observation.id).label("count"),
            )
            .where(Observation.location_id == location_id)
        )

        if days is not None:
            cutoff = datetime.now(timezone.utc) - timedelta(days=days)
            stmt = stmt.where(Observation.observed_at >= cutoff)

        row = self.session.execute(stmt).first()

        avg_temp = round(row.avg_temp, 1) if row.avg_temp is not None else None
        min_temp = round(row.min_temp, 1) if row.min_temp is not None else None
        max_temp = round(row.max_temp, 1) if row.max_temp is not None else None
        count = int(row.count or 0)

        return TemperatureStats(
            location_id=location_id,
            avg_temp=avg_temp,
            min_temp=min_temp,
            max_temp=max_temp,
            count=count,
        )