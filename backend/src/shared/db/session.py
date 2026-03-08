# backend/src/shared/db/session.py

from collections.abc import Generator

from sqlmodel import SQLModel, Session, create_engine

from src.shared.config import settings

_engine = None


def get_engine():
    global _engine
    if _engine is None:
        if not settings.database_url:
            raise RuntimeError(
                "DATABASE_URL is not set. Create backend/.env from .env.example."
            )
        _engine = create_engine(
            settings.database_url,
            echo=False,
            pool_pre_ping=True,
        )
    return _engine


def get_session() -> Generator[Session, None, None]:
    with Session(get_engine()) as session:
        yield session


def init_db() -> None:
    engine = get_engine()
    SQLModel.metadata.create_all(engine)