"""
Auto seed for locations
Author: Dongwook Kim
"""

from __future__ import annotations

from sqlmodel import Session, select

from src.shared.db.session import get_session  # ✅ 이걸로 통일
from src.contexts.locations.infra.orm import Location  # ✅ Location ORM 경로에 맞게



SEED_LOCATIONS = [
    dict(
        name="London",
        country_code="GB",
        lat=51.5074,
        lon=-0.1278,
        is_active=True,
        is_featured=False,
        display_order=0,
    ),
    dict(
        name="Leeds",
        country_code="GB",
        lat=53.8008,
        lon=-1.5491,
        is_active=True,
        is_featured=True,
        display_order=1,   # featured면 0/1 순서 주면 화면에 좋음
    ),
    dict(
        name="Manchester",
        country_code="GB",
        lat=53.4808,
        lon=-2.2426,
        is_active=True,
        is_featured=False,
        display_order=2,
    ),
    dict(
        name="Seoul",
        country_code="KR",
        lat=37.5665,
        lon=126.9780,
        is_active=True,
        is_featured=False,
        display_order=3,
    ),
]


def seed_locations_if_missing() -> None:
    """
    - 도시별로 (name, country_code) 기준 존재 체크
    - 있으면 skip, 없으면 insert
    - Leeds만 featured=True로 정리(항상 일관성 유지)
    """
    with get_session() as session:
        inserted_any = False

        for row in SEED_LOCATIONS:
            # ✅ autoflush 방어 (pending insert가 있더라도 조회 시 flush 안 함)
            with session.no_autoflush:
                exists = session.exec(
                    select(Location).where(
                        Location.name == row["name"],
                        Location.country_code == row["country_code"],
                    )
                ).first()

            if exists:
                continue

            session.add(Location(**row))
            inserted_any = True

        # ✅ Leeds만 featured=True, 나머지 False로 정리
        leeds = session.exec(
            select(Location).where(Location.name == "Leeds", Location.country_code == "GB")
        ).first()

        if leeds and hasattr(Location, "is_featured"):
            all_locs = session.exec(select(Location)).all()
            for loc in all_locs:
                loc.is_featured = (loc.id == leeds.id)
            inserted_any = True

        if inserted_any:
            session.commit()