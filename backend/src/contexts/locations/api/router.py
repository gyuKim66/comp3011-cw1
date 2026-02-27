"""
Author: Dongwook Kim
Created: 2026-02-24

Locations (Cities) API router.
"""

from fastapi import APIRouter, HTTPException

from src.contexts.locations.api.schemas import CreateCityRequest, CityResponse
from src.contexts.locations.infra.repo import SqlCityRepository
from src.contexts.locations.app.services import create_city, list_cities, get_city

router = APIRouter()


@router.post("", response_model=CityResponse, status_code=201)
def create(dto: CreateCityRequest) -> CityResponse:
    repo = SqlCityRepository()
    city = create_city(repo, dto.name, dto.latitude, dto.longitude)
    return CityResponse(id=city.id or 0, name=city.name, latitude=city.latitude, longitude=city.longitude)


@router.get("", response_model=list[CityResponse])
def list_all() -> list[CityResponse]:
    repo = SqlCityRepository()
    cities = list_cities(repo)
    return [CityResponse(id=c.id or 0, name=c.name, latitude=c.latitude, longitude=c.longitude) for c in cities]


@router.get("/{city_id}", response_model=CityResponse)
def get_one(city_id: int) -> CityResponse:
    repo = SqlCityRepository()
    city = get_city(repo, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return CityResponse(id=city.id or 0, name=city.name, latitude=city.latitude, longitude=city.longitude)