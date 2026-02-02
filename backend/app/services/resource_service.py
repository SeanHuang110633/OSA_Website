from __future__ import annotations

from typing import Optional
from app.repositories.resource_repository import ResourceRepository
from app.schemas.resource_schemas import ResourceListResponse, ResourceListItem, ResourceDetailResponse

class ResourceService:
    def __init__(self, repository: ResourceRepository):
        self.repository = repository

    def _pick_locale(self, val, locale: str) -> Optional[str]:
        if val is None:
            return None
        if isinstance(val, str):
            return val
        if isinstance(val, dict):
            # fallback：locale -> zh-TW -> en-US
            return val.get(locale) or val.get("zh-TW") or val.get("en-US")
        return str(val)

    def get_resources(
        self,
        *,
        locale: str,
        page: int,
        size: int,
        type: Optional[str],
        category_id: Optional[int],
        query: Optional[str],
    ) -> dict:
        rows = self.repository.get_list(
            type=type,
            category_id=category_id,
            query=query,
        )

        # Python 端搜尋（先求正確，之後再做 DB JSON 搜尋優化）
        if query:
            q = query.strip().lower()
            if q:
                def hit(r) -> bool:
                    title = (self._pick_locale(r.title, locale) or "").lower()
                    desc = (self._pick_locale(r.description, locale) or "").lower()
                    content = (self._pick_locale(r.content, locale) or "").lower()
                    return q in title or q in desc or q in content
                rows = [r for r in rows if hit(r)]

        total = len(rows)
        start = (page - 1) * size
        end = start + size
        rows_page = rows[start:end]

        items = [
            ResourceListItem(
                id=r.id,
                category_id=r.category_id,
                type=r.type,  # "link" / "article"
                title=self._pick_locale(r.title, locale) or "",
                description=self._pick_locale(r.description, locale),
                url=self._pick_locale(r.url, locale),
                sort_order=r.sort_order,
                is_active=r.is_active,
            )
            for r in rows_page
        ]

        return ResourceListResponse(items=items, page=page, size=size, total=total).model_dump()

    def get_resource_detail(self, *, resource_id: int, locale: str) -> dict:
        r = self.repository.get_by_id(resource_id)
        if not r:
            # 讓 router 統一處理 404 也行，但這裡丟 ValueError 讓 router 捕捉轉 HTTPException
            raise ValueError("Resource not found")

        dto = ResourceDetailResponse(
            id=r.id,
            category_id=r.category_id,
            type=r.type,
            title=self._pick_locale(r.title, locale) or "",
            description=self._pick_locale(r.description, locale),
            url=self._pick_locale(r.url, locale),
            content=self._pick_locale(r.content, locale),
            sort_order=r.sort_order,
            is_active=r.is_active,
        )
        return dto.model_dump()
