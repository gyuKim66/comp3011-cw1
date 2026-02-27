"""
Author: Dongwook Kim
Created: 2026-02-24

SQL-backed repository for Cities.
"""

from sqlmodel import select

from src.contexts.locations.domain.entities import City
from src.contexts.locations.domain.repositories import CityRepository
from src.contexts.locations.infra.orm import CityModel
from src.shared.db.session import get_session


class SqlCityRepository(CityRepository):
    def create(self, city: City) -> City:
        with get_session() as session:
            model = CityModel(name=city.name, latitude=city.latitude, longitude=city.longitude)
            session.add(model)
            session.commit()
            session.refresh(model)
            return City(id=model.id, name=model.name, latitude=model.latitude, longitude=model.longitude)

    def list(self) -> list[City]:
        with get_session() as session:
            rows = session.exec(select(CityModel)).all()
            return [City(id=r.id, name=r.name, latitude=r.latitude, longitude=r.longitude) for r in rows]

    def get(self, city_id: int) -> City | None:
        with get_session() as session:
            row = session.get(CityModel, city_id)
            if row is None:
                return None
            return City(id=row.id, name=row.name, latitude=row.latitude, longitude=row.longitude)
