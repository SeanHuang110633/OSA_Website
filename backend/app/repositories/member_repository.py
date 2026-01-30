"""
Member Repository
-----------------
負責與資料庫溝通（SQLModel / Query）
本 Step 3-2 目標：
- 提供「成員列表 + 總筆數」查詢方法
- 讓 service 在 Step 3-3 可以直接呼叫
"""

from typing import Optional, Tuple, List

from sqlmodel import Session, select
from sqlalchemy import func

from app.models.member_model import Member


class MemberRepository:
    """Members 查詢層：封裝所有 DB query"""

    def __init__(self, session: Session):
        self.session = session

    def get_members_with_total(
        self,
        page: int = 1,
        size: int = 20,
        unit_key: Optional[str] = None,
        query: Optional[str] = None,
    ) -> Tuple[List[Member], int]:
        """
        取得成員列表 + 總筆數（分頁）

        參數：
        - page/size：分頁控制
        - unit_key：先保留（Step 3-4 若有單位表再接）
        - query：名稱/職稱等關鍵字搜尋（先做 name/title）

        回傳：
        - (members, total)
        """
        skip = (page - 1) * size

        # 基本查詢：只顯示啟用的成員
        stmt = select(Member).where(Member.is_active == True)

        # 關鍵字搜尋：先做 name/title LIKE（之後可擴充 email/duty）
        if query:
            like = f"%{query}%"
            stmt = stmt.where((Member.name.like(like)) | (Member.title.like(like)))

        # TODO(Step 3-4): 若之後有 unit/department 欄位或關聯，再加上 unit_key filter
        # if unit_key:
        #     stmt = stmt.where(Member.unit_key == unit_key)

        # 總筆數查詢：用 subquery 算 count（跟 download 模組同套路）
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = self.session.exec(count_stmt).one()

        # 排序 + 分頁
        stmt = stmt.order_by(Member.id.asc()).offset(skip).limit(size)

        members = self.session.exec(stmt).all()
        return members, total