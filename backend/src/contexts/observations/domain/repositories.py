# backend/src/contexts/observations/domain/repositories.py

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable

from src.contexts.observations.domain.entities import ObservationEntity


class ObservationRepository(ABC):
    """
    Domain-level repository interface for observations.
    Infra layer must implement this.
    """

    @abstractmethod
    def get_latest_by_location_id(
        self, location_id: int
    ) -> ObservationEntity | None:
        ...

    @abstractmethod
    def get_latest_for_location_ids(
        self, location_ids: Iterable[int]
    ) -> dict[int, ObservationEntity]:
        """
        Optional batch method for performance.
        Returns {location_id: latest_observation}
        """
        ...