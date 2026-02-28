"""
Author: Dongwook Kim
Created: 2026-02-24

Locations API router.
"""

from fastapi import APIRouter, HTTPException

from src.contexts.locations.api.schemas import CreateLocationRequest, LocationResponse
from src.contexts.locations.infra.repo import SqlLocationRepository
from src.contexts.locations.app.services import create_location, list_locations, get_location


from sqlmodel import select
from src.shared.db.session import get_session
from src.contexts.locations.infra.orm import Location

router = APIRouter(prefix="/locations", tags=["locations"])

# router = APIRouter()


@router.post("", response_model=LocationResponse, status_code=201)
def create(dto: CreateLocationRequest) -> LocationResponse:
    repo = SqlLocationRepository()
    loc = create_location(
        repo,
        dto.name,
        dto.country_code,
        dto.lat,
        dto.lon,
        is_featured=dto.is_featured,
        display_order=dto.display_order,
        is_active=dto.is_active,
    )
    return LocationResponse(
        id=loc.id or 0,
        name=loc.name,
        country_code=loc.country_code,
        lat=loc.lat,
        lon=loc.lon,
        is_featured=loc.is_featured,
        display_order=loc.display_order,
        is_active=loc.is_active,
    )


@router.get("", response_model=list[LocationResponse])
def list_all(featured: bool | None = None) -> list[LocationResponse]:
    repo = SqlLocationRepository()
    locations = list_locations(repo, featured=featured)  # ✅ 서비스로 위임

    return [
        LocationResponse(
            id=l.id or 0,
            name=l.name,
            country_code=l.country_code,
            lat=l.lat,
            lon=l.lon,
            is_featured=l.is_featured,
            display_order=l.display_order,
            is_active=l.is_active,
        )
        for l in locations
    ]  



@router.get("/{location_id}", response_model=LocationResponse)
def get_one(location_id: int) -> LocationResponse:
    repo = SqlLocationRepository()
    loc = get_location(repo, location_id)
    if loc is None:
        raise HTTPException(status_code=404, detail="Location not found")

    return LocationResponse(
        id=loc.id or 0,
        name=loc.name,
        country_code=loc.country_code,
        lat=loc.lat,
        lon=loc.lon,
        is_featured=loc.is_featured,
        display_order=loc.display_order,
        is_active=loc.is_active,
    )

