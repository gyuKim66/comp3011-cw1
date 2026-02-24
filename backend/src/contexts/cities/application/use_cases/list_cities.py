"""
Author: Dongwook Kim
Created: 2026-02-24

Use case: list cities.
"""

from src.contexts.cities.application.dtos import CityDTO
from src.contexts.cities.domain.repositories import CityRepository


def list_cities(repo: CityRepository) -> list[CityDTO]:
    items = repo.list()
    return [
        CityDTO(id=c.id, name=c.name, latitude=c.latitude, longitude=c.longitude)
        for c in items
        if c.id is not None
    ]
