"""
Author: Dongwook Kim
Created: 2026-02-24

Cities domain entities.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class City:
    id: int | None
    name: str
    latitude: float
    longitude: float
