from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlmodel import Session

from src.contexts.locations.api.schemas import (
    CreateLocationRequest,
    LocationResponse,
    UpdateLocationRequest,
    LocationSearchItem,
)
from src.contexts.locations.infra.owm_geocoding_client import OpenWeatherGeocodingClient
from src.contexts.locations.infra.repo import SqlLocationRepository
from src.contexts.locations.app.services import (
    create_location,
    list_locations,
    get_location,
    update_location,
    FeaturedLimitExceeded,
    DuplicateLocationError,
)

from src.shared.db.session import get_session

router = APIRouter(prefix="/locations", tags=["locations"])


@router.post("", response_model=LocationResponse, status_code=201)
def create(
    dto: CreateLocationRequest,
    session: Session = Depends(get_session),
) -> LocationResponse:
    repo = SqlLocationRepository(session)
    try:
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
    except DuplicateLocationError as e:
        raise HTTPException(status_code=409, detail=str(e))

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
def list_all(
    featured: bool | None = None,
    session: Session = Depends(get_session),
) -> list[LocationResponse]:
    repo = SqlLocationRepository(session)
    locations = list_locations(repo, featured=featured)

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


@router.get("/search", response_model=list[LocationSearchItem])
async def search_locations(
    q: str = Query(..., min_length=2),
    limit: int = Query(5, ge=1, le=10),
) -> list[LocationSearchItem]:
    try:
        client = OpenWeatherGeocodingClient()
        rows = await client.search(q=q, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Geocoding failed: {e}")

    result: list[LocationSearchItem] = []
    for r in rows:
        result.append(
            LocationSearchItem(
                name=r.get("name", ""),
                country_code=r.get("country", ""),
                lat=float(r.get("lat")),
                lon=float(r.get("lon")),
                state=r.get("state"),
            )
        )
    return result


@router.get("/{location_id}", response_model=LocationResponse)
def get_one(
    location_id: int,
    session: Session = Depends(get_session),
) -> LocationResponse:
    repo = SqlLocationRepository(session)
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


@router.patch("/{location_id}", response_model=LocationResponse)
def patch_one(
    location_id: int,
    dto: UpdateLocationRequest,
    session: Session = Depends(get_session),
) -> LocationResponse:
    repo = SqlLocationRepository(session)

    try:
        loc = update_location(
            repo,
            location_id,
            is_featured=dto.is_featured,
            is_active=dto.is_active,
            display_order=dto.display_order,
        )
    except FeaturedLimitExceeded as e:
        raise HTTPException(status_code=409, detail=str(e))

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


@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_one(
    location_id: int,
    session: Session = Depends(get_session),
) -> Response:
    repo = SqlLocationRepository(session)

    loc = get_location(repo, location_id)
    if loc is None:
        raise HTTPException(status_code=404, detail="Location not found")

    loc = update_location(
        repo,
        location_id,
        is_active=False,
        is_featured=False,
    )
    if loc is None:
        raise HTTPException(status_code=404, detail="Location not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)