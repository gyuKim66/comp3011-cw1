"""
Author: Dongwook Kim
Created: 2026-02-24

City APP Services
"""

from src.contexts.locations.domain.entities import City
from src.contexts.locations.domain.repositories import CityRepository

def create_city(repo: CityRepository, name: str, latitude: float, longitude: float) -> City:
    return repo.create(City(id=None, name=name, latitude=latitude, longitude=longitude))

def list_cities(repo: CityRepository) -> list[City]:
    return repo.list()

def get_city(repo: CityRepository, city_id: int) -> City | None:
    return repo.get(city_id)