"""
Seed repository for Locations (DB access only)
Author: Dongwook Kim
"""

from __future__ import annotations

from typing import Iterable, Optional

from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

# ✅ 프로젝트에 맞게 경로 수정
from src.contexts.locations.infra.orm import LocationORM as Location  # 또는 models.Location
from src.shared.db.session import get_session  # 또는 Session(engine) 패턴을 쓰면 교체


class LocationSeedRepo:
    """
    Infra-only repository for seeding locations.
    - 도시별 (name, country_code) 존재 여부 확인
    - 없으면 insert, 있으면 skip
    - (옵션) featured는 특정 1개만 true로 정리
    """

    def __init__(self, session: Session):
        self.session = session

    def find_by_name_country(self, *, name: str, country_code: str) -> Optional[Location]:
        stmt = select(Location).where(Location.name == name, Location.country_code == country_code)
        return self.session.exec(stmt).first()

    def insert_if_missing(self, *, data: dict) -> bool:
        """
        Returns:
            True  -> 새로 insert 함
            False -> 이미 존재해서 skip 함
        """
        exists = self.find_by_name_country(
            name=data["name"],
            country_code=data["country_code"],
        )
        if exists:
            return False

        self.session.add(Location(**data))
        try:
            # flush로 즉시 제약조건/중복 여부 확인(커밋은 바깥에서)
            self.session.flush()
            return True
        except IntegrityError:
            # 동시에 여러 프로세스가 seed할 때의 레이스 조건 방어(선택)
            self.session.rollback()
            return False

    def ensure_only_one_featured(self, *, featured_name: str, featured_country_code: str) -> bool:
        """
        featured 대상 도시가 존재하면:
        - 그 도시는 is_featured=True
        - 나머지는 is_featured=False 로 정리
        Returns:
            True if any change applied, else False
        """
        featured = self.find_by_name_country(name=featured_name, country_code=featured_country_code)
        if not featured:
            return False

        changed = False
        all_rows = self.session.exec(select(Location)).all()
        for row in all_rows:
            should_be = (row.id == featured.id)
            if getattr(row, "is_featured", None) is None:
                # 모델에 is_featured 컬럼이 없다면 아무것도 안 함
                return False
            if row.is_featured != should_be:
                row.is_featured = should_be
                changed = True
        return changed


# ---- 편의 함수: app/seed.py에서 호출하기 쉽게 ----

def insert_locations_if_missing(seed_rows: Iterable[dict]) -> int:
    """
    seed_rows: [{name, country_code, ...}, ...]
    Returns: inserted count
    """
    with get_session() as session:
        repo = LocationSeedRepo(session)

        inserted = 0
        for row in seed_rows:
            if repo.insert_if_missing(data=row):
                inserted += 1

        # commit은 한 번만 (성능 + 트랜잭션 일관성)
        if inserted > 0:
            session.commit()

        return inserted