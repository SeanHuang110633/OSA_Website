"""
Member Service
--------------
負責商業邏輯處理（分頁、資料轉換、locale 處理等）

本 Step 3-3：
- 改成從 repository 取得 members（真 DB）
- 轉換成對外 response schema（MemberListItem）
"""

from typing import Optional

from app.schemas.member_schema import MemberPaginationResponse, MemberListItem
from app.repositories.member_repository import MemberRepository
from app.models.member_model import Member


class MemberService:
    """Members 服務層：DB 版本"""

    def __init__(self, repo: MemberRepository):
        self.repo = repo

    def _to_list_item(self, m: Member) -> MemberListItem:
        """
        將 Member(SQLModel) 轉成 MemberListItem(Pydantic)
        - Optional 欄位若 DB 是 NULL，會自然變成 None
        """
        return MemberListItem(
            id=m.id,
            name=m.name,
            title=m.title,
            email=m.email,
            ext=m.ext,
            duty=m.duty,
            extra=m.extra,
            avatar_url=m.avatar_url,
        )

    def get_members(
        self,
        locale: str = "zh-TW",
        page: int = 1,
        size: int = 20,
        unit_key: Optional[str] = None,
        query: Optional[str] = None,
    ) -> MemberPaginationResponse:
        """
        取得成員列表（分頁）
        - locale 先保留，之後你們若有多語系欄位再用
        """
        members, total = self.repo.get_members_with_total(
            page=page,
            size=size,
            unit_key=unit_key,
            query=query,
        )

        items = [self._to_list_item(m) for m in members]
        return MemberPaginationResponse(items=items, total=total)