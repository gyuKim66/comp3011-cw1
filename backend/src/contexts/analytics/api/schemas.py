# backend/src/contexts/analytics/api/schemas.py

from pydantic import BaseModel, Field


class TemperatureStatsResponse(BaseModel):
    """
    Response schema for temperature statistics.
    """

    location_id: int = Field(..., description="Location ID")

    avg_temp: float | None = Field(
        None,
        description="Average temperature",
        example=18.2,
    )

    min_temp: float | None = Field(
        None,
        description="Minimum temperature",
        example=14.1,
    )

    max_temp: float | None = Field(
        None,
        description="Maximum temperature",
        example=22.5,
    )

    count: int = Field(
        ...,
        description="Number of observations used for statistics",
        example=24,
    )