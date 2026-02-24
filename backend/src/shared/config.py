"""
Author: Dongwook Kim
Created: 2026-02-24

Configuration loader.
"""

from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "")


settings = Settings()
