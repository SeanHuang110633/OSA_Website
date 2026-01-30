"""
Member Service
--------------
負責商業邏輯處理（分頁、資料轉換、locale 處理等）
"""

from typing import Optional
from app.schemas.member_schema import MemberPaginationResponse, MemberListItem


class MemberService:
    """Members 服務層：先用假資料版本"""

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
        - locale/unit_key/query 先保留參數，後續接 DB 才會用到
        """
        # TODO(Step 3): 改成從 repository 查 DB
        fake_items = [
            MemberListItem(
                id=1,
                name="王小明",
                title="組員",
                email="ming@example.com",
                ext="1234",
                duty="網站維護 / 活動支援",
                extra="",
                avatar_url=None,
            ),
            MemberListItem(
                id=2,
                name="陳小華",
                title="組長",
                email="hua@example.com",
                ext="5678",
                duty="業務統籌",
                extra="",
                avatar_url=None,
            ),
        ]

        # 先做最簡單：不真的分頁（demo 用），但回傳格式先固定
        return MemberPaginationResponse(items=fake_items, total=len(fake_items))