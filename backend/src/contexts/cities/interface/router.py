"""
Author: Dongwook Kim
Created: 2026-02-24

Cities router (thin controller).
"""

from fastapi import APIRouter, HTTPException

from src.contexts.cities.application.dtos import CreateCityDTO
from src.contexts.cities.application.use_cases.create_city import create_city
from src.contexts.cities.application.use_cases.list_cities import list_cities
from src.contexts.cities.infrastructure.repositories import SqlCityRepository
from src.contexts.cities.interface.schemas import CityResponse, CreateCityRequest

router = APIRouter()
_repo = SqlCityRepository()


@router.post("", response_model=CityResponse, status_code=201)
def create_city_endpoint(req: CreateCityRequest) -> CityResponse:
    created = create_city(_repo, CreateCityDTO(**req.model_dump()))
    return CityResponse(**created.model_dump())


@router.get("", response_model=list[CityResponse])
def list_cities_endpoint() -> list[CityResponse]:
    items = list_cities(_repo)
    return [CityResponse(**i.model_dump()) for i in items]


@router.get("/{city_id}", response_model=CityResponse)
def get_city_endpoint(city_id: int) -> CityResponse:
    city = _repo.get(city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    assert city.id is not None
    return CityResponse(id=city.id, name=city.name, latitude=city.latitude, longitude=city.longitude)
