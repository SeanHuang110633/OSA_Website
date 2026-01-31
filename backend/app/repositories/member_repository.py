# app/repositories/member_repository.py
from typing import List, Optional
from sqlmodel import Session, select, col
from app.models.member_model import Department, DepartmentMember


class MemberRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_departments(self) -> List[Department]:
        statement = (
            select(Department)
            .where(Department.deleted_at == None)
            .where(Department.is_active == True)
            .order_by(col(Department.sort_order).asc(), col(Department.id).asc())
        )
        return self.session.exec(statement).all()

    def get_department_by_id(self, department_id: int) -> Optional[Department]:
        statement = (
            select(Department)
            .where(Department.id == department_id)
            .where(Department.deleted_at == None)
            .where(Department.is_active == True)
        )
        return self.session.exec(statement).first()

    def get_members_by_department(
        self,
        department_id: int,
        status: Optional[int] = 1,  # 依你們約定：1 在職
    ) -> List[DepartmentMember]:
        statement = (
            select(DepartmentMember)
            .where(DepartmentMember.department_id == department_id)
            .where(DepartmentMember.deleted_at == None)
        )

        if status is not None:
            statement = statement.where(DepartmentMember.status == status)

        statement = statement.order_by(
            col(DepartmentMember.sort_order).asc(),
            col(DepartmentMember.id).asc()
        )

        return self.session.exec(statement).all()