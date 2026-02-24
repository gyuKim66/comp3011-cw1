"""
Author: Dongwook Kim
Created: 2026-02-24

Use case: create city.
"""

from src.contexts.cities.application.dtos import CityDTO, CreateCityDTO
from src.contexts.cities.domain.entities import City
from src.contexts.cities.domain.repositories import CityRepository


def create_city(repo: CityRepository, dto: CreateCityDTO) -> CityDTO:
    city = City(id=None, name=dto.name, latitude=dto.latitude, longitude=dto.longitude)
    created = repo.create(city)
    assert created.id is not None
    return CityDTO(id=created.id, name=created.name, latitude=created.latitude, longitude=created.longitude)
