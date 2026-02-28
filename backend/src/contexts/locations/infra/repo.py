# src/contexts/locations/infra/orm.py

from __future__ import annotations

from sqlmodel import select

from src.contexts.locations.domain.entities import LocationEntity
from src.contexts.locations.domain.repositories import LocationRepository
from src.contexts.locations.infra.orm import Location
from src.shared.db.session import get_session


class SqlLocationRepository(LocationRepository):
    def create(self, loc: LocationEntity) -> LocationEntity:
        with get_session() as session:
            model = Location(
                name=loc.name,
                country_code=loc.country_code,
                lat=loc.lat,
                lon=loc.lon,
                is_active=loc.is_active,
                is_featured=loc.is_featured,
                display_order=loc.display_order,
            )
            session.add(model)
            session.commit()
            session.refresh(model)
            return LocationEntity(
                id=model.id,
                name=model.name,
                country_code=model.country_code,
                lat=model.lat,
                lon=model.lon,
                is_active=model.is_active,
                is_featured=model.is_featured,
                display_order=model.display_order,
            )

    def list(self) -> list[LocationEntity]:
        with get_session() as session:
            rows = session.exec(select(Location).order_by(Location.display_order)).all()
            return [
                LocationEntity(
                    id=r.id,
                    name=r.name,
                    country_code=r.country_code,
                    lat=r.lat,
                    lon=r.lon,
                    is_active=r.is_active,
                    is_featured=r.is_featured,
                    display_order=r.display_order,
                )
                for r in rows
            ]

    def get(self, location_id: int) -> LocationEntity | None:
        with get_session() as session:
            row = session.get(Location, location_id)
            if row is None:
                return None
            return LocationEntity(
                id=row.id,
                name=row.name,
                country_code=row.country_code,
                lat=row.lat,
                lon=row.lon,
                is_active=row.is_active,
                is_featured=row.is_featured,
                display_order=row.display_order,
            )