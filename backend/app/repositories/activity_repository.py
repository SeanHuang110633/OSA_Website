# app/repositories/activity_repository.py
from typing import List
from sqlmodel import Session, select, col
from app.models.activity_model import Activity

class ActivityRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Activity]:
        """
        取得所有活動 (不分頁)
        條件：未軟刪除
        排序：依照 ID 倒序 (新 -> 舊)
        """
        statement = (
            select(Activity)
            .where(Activity.deleted_at == None)
            .order_by(col(Activity.id).desc())
        )
        
        return self.session.exec(statement).all()