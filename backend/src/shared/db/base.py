# backend/src/shared/db/base.py
from sqlmodel import SQLModel

# Import all ORM models so metadata is populated
from src.contexts.locations.infra.orm import Location  # noqa
from src.contexts.observations.infra.orm import Observation  # noqa

metadata = SQLModel.metadata