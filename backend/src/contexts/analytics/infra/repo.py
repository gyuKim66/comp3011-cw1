# backend/src/contexts/analytics/infra/repo.py


from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlmodel import Session

from src.contexts.analytics.domain.entities import (
    TemperatureStats,
    HumidityStats,
    TemperatureTrend,
    TemperatureTrendPoint,
)
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
            if days == 0:
                now = datetime.now(timezone.utc)
                cutoff = datetime(
                    year=now.year,
                    month=now.month,
                    day=now.day,
                    tzinfo=timezone.utc,
                )
            else:
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

    def get_humidity_stats(
        self,
        location_id: int,
        days: int | None = None,
    ) -> HumidityStats:
        stmt = (
            select(
                func.avg(Observation.humidity).label("avg_humidity"),
                func.min(Observation.humidity).label("min_humidity"),
                func.max(Observation.humidity).label("max_humidity"),
                func.count(Observation.id).label("count"),
            )
            .where(Observation.location_id == location_id)
        )

        if days is not None:
            if days == 0:
                now = datetime.now(timezone.utc)
                cutoff = datetime(
                    year=now.year,
                    month=now.month,
                    day=now.day,
                    tzinfo=timezone.utc,
                )
            else:
                cutoff = datetime.now(timezone.utc) - timedelta(days=days)

            stmt = stmt.where(Observation.observed_at >= cutoff)

        row = self.session.execute(stmt).first()

        avg_humidity = (
            round(row.avg_humidity, 1) if row.avg_humidity is not None else None
        )
        min_humidity = (
            round(row.min_humidity, 1) if row.min_humidity is not None else None
        )
        max_humidity = (
            round(row.max_humidity, 1) if row.max_humidity is not None else None
        )
        count = int(row.count or 0)

        return HumidityStats(
            location_id=location_id,
            avg_humidity=avg_humidity,
            min_humidity=min_humidity,
            max_humidity=max_humidity,
            count=count,
        )

    def get_temperature_trend(
        self,
        location_id: int,
        days: int,
    ) -> TemperatureTrend:
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)

        stmt = (
            select(
                func.date(Observation.observed_at).label("date"),
                func.avg(Observation.temp).label("avg_temp"),
            )
            .where(Observation.location_id == location_id)
            .where(Observation.observed_at >= cutoff)
            .group_by(func.date(Observation.observed_at))
            .order_by(func.date(Observation.observed_at))
        )

        rows = self.session.execute(stmt).all()

        data = [
            TemperatureTrendPoint(
                date=str(row.date),
                avg_temp=round(row.avg_temp, 1) if row.avg_temp is not None else None,
            )
            for row in rows
        ]

        return TemperatureTrend(
            location_id=location_id,
            days=days,
            data=data,
        )