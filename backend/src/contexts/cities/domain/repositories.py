"""
Author: Dongwook Kim
Created: 2026-02-24

Domain-level repository interfaces.
"""

from abc import ABC, abstractmethod
from src.contexts.cities.domain.entities import City


class CityRepository(ABC):
    @abstractmethod
    def create(self, city: City) -> City: ...

    @abstractmethod
    def list(self) -> list[City]: ...

    @abstractmethod
    def get(self, city_id: int) -> City | None: ...
