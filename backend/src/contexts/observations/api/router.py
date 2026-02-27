"""
Author: Dongwook Kim
Created: 2026-02-24

observation router (placeholder).
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}
