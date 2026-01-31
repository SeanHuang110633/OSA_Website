from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from app.models.member_model import Department


class MemberRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all_active_members_by_dept(self):
        """
        不在 repository 層做 status 過濾，避免資料被濾光導致 API 回傳空陣列。
        過濾/轉換在 service 層處理（不改 DB 的情況下較安全）。
        """
        statement = (
            select(Department)
            .where(Department.is_active == True)
            .order_by(Department.sort_order.asc())
            .options(selectinload(Department.members))
        )
        return self.session.exec(statement).all()