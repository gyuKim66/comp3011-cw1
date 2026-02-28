"""
Author: Dongwook Kim
Created: 2026-02-24

Domain-level repository interfaces.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from src.contexts.locations.domain.entities import LocationEntity


class LocationRepository(ABC):
    @abstractmethod
    def create(self, loc: LocationEntity) -> LocationEntity: ...

    @abstractmethod
    def list(self) -> list[LocationEntity]: ...

    @abstractmethod
    def get(self, location_id: int) -> LocationEntity | None: ...