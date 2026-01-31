from __future__ import annotations

from sqlmodel import Session, select
from typing import Optional, List
from app.models.resource import Resource

class ResourceRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_list(
        self,
        *,
        type: Optional[str] = None,
        category_id: Optional[int] = None,
        query: Optional[str] = None,
    ) -> List[Resource]:
        stmt = select(Resource).where(Resource.deleted_at.is_(None))

        # 最基本的 DB 過濾放 repository
        stmt = stmt.where(Resource.is_active == True)

        if type:
            stmt = stmt.where(Resource.type == type)

        if category_id:
            stmt = stmt.where(Resource.category_id == category_id)

        # ⚠️ query：因為 title/content 是 JSON，多語系搜尋要依 locale
        # Repository 先不做複雜 JSON 搜尋（可留給 Service 或下一步再優化）
        # 先回全部讓 Service 做「Python 端 contains」
        stmt = stmt.order_by(Resource.category_id, Resource.sort_order, Resource.id)

        return list(self.session.exec(stmt).all())

    def get_by_id(self, resource_id: int) -> Optional[Resource]:
        stmt = (
            select(Resource)
            .where(Resource.id == resource_id)
            .where(Resource.deleted_at.is_(None))
            .where(Resource.is_active == True)
        )
        return self.session.exec(stmt).first()
