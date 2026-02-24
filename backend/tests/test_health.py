"""
Author: Dongwook Kim
Created: 2026-02-24
"""

from fastapi.testclient import TestClient
from src.main import create_app


def test_health() -> None:
    app = create_app()
    client = TestClient(app)
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
