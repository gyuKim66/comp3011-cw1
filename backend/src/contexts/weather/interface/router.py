"""
Author: Dongwook Kim
Created: 2026-02-24

Weather router (placeholder).
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
def ping() -> dict[str, str]:
    return {"weather": "pong"}
