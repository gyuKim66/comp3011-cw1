"""
Author: Dongwook Kim
Created: 2026-02-24

FastAPI application entrypoint.
"""

from fastapi import FastAPI

from src.api.router import api_router
from src.shared.database import init_db


def create_app() -> FastAPI:
    app = FastAPI(title="COMP3011-CW1 API", version="0.1.0")

    @app.on_event("startup")
    def _startup() -> None:
        init_db()

    app.include_router(api_router)
    return app


app = create_app()
