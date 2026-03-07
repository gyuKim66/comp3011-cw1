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


class HumidityStatsResponse(BaseModel):
    """
    Response schema for humidity statistics.
    """

    location_id: int = Field(..., description="Location ID")

    avg_humidity: float | None = Field(
        None,
        description="Average humidity",
        example=72.1,
    )

    min_humidity: float | None = Field(
        None,
        description="Minimum humidity",
        example=60.0,
    )

    max_humidity: float | None = Field(
        None,
        description="Maximum humidity",
        example=88.0,
    )

    count: int = Field(
        ...,
        description="Number of observations used for statistics",
        example=24,
    )


class TemperatureTrendPointResponse(BaseModel):
    """
    Single point in temperature trend.
    """

    date: str = Field(
        ...,
        description="Date of observation",
        example="2026-03-01",
    )

    avg_temp: float | None = Field(
        None,
        description="Average temperature for the day",
        example=10.3,
    )


class TemperatureTrendResponse(BaseModel):
    """
    Response schema for temperature trend.
    """

    location_id: int = Field(..., description="Location ID")

    days: int = Field(
        ...,
        description="Number of days included in the trend",
        example=7,
    )

    data: list[TemperatureTrendPointResponse] = Field(
        ...,
        description="Daily temperature trend data",
    )