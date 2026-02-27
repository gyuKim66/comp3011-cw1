"""
Author: Dongwook Kim
Created: 2026-02-24

FastAPI application entrypoint.
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.router import api_router
from src.shared.db.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup 영역
    if os.getenv("DATABASE_URL"):
        # init_db()
        pass
    yield

    # shutdown 영역 (필요하면 여기에 추가)


def create_app() -> FastAPI:
    app = FastAPI(
        title="COMP3011-CW1 API",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


    app.include_router(api_router)
    return app


app = create_app()
