from typing import List
from sqlmodel import Session, select, col
from sqlalchemy.orm import selectinload, with_loader_criteria
from app.models.member_model import Department, Member

class MemberRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_departments_with_members(self) -> List[Department]:
        """
        取得「未刪除且啟用」的部門，並預先載入「未刪除且在職」的成員。
        """
        statement = (
            select(Department)
            # 1. 過濾部門本身 (Department 過濾)
            .where(Department.deleted_at.is_(None))
            .where(Department.is_active == True)
            
            # 2. 排序部門
            .order_by(col(Department.sort_order).asc())
            
            .options(
                # 3. 預先載入 members
                selectinload(Department.members),
                
                # 4. 針對載入的 Member 進行全域過濾
                # 這會確保 SQL 在 JOIN 或 SELECT 成員時，自動加上 AND members.deleted_at IS NULL
                # 這裡同時過濾掉了「已刪除」和「非在職(status!=1)」的成員 (視需求調整 status)
                with_loader_criteria(
                    Member, 
                    (Member.deleted_at.is_(None)) & (Member.status == 1)
                )
            )
        )
        
        return self.session.exec(statement).all()