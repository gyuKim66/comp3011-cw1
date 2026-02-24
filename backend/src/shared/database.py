"""
Author: Dongwook Kim
Created: 2026-02-24

Database engine/session factory (SQLModel).
"""

from sqlmodel import SQLModel, Session, create_engine

from src.shared.config import settings

_engine = None


def get_engine():
    global _engine
    if _engine is None:
        if not settings.database_url:
            raise RuntimeError("DATABASE_URL is not set. Create backend/.env from .env.example.")
        _engine = create_engine(settings.database_url, echo=False)
    return _engine


def get_session() -> Session:
    return Session(get_engine())


def init_db() -> None:
    engine = get_engine()
    SQLModel.metadata.create_all(engine)
