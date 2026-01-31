# app/routers/member_router.py
from typing import List
from fastapi import APIRouter, Depends, Query, Path

from app.schemas.member_schema import DepartmentPublic, DepartmentWithMembers
from app.services.member_service import MemberService
from app.dependencies import get_member_service  # 你要在 dependencies 加這個

router = APIRouter(prefix="/departments", tags=["Departments"])


@router.get("/", response_model=List[DepartmentPublic])
def get_departments(
    locale: str = Query("zh-TW", description="語言代碼 (zh-TW, en-US)"),
    service: MemberService = Depends(get_member_service),
):
    return service.get_departments(locale=locale)


@router.get("/{department_id}/members", response_model=DepartmentWithMembers)
def get_department_members(
    department_id: int = Path(..., ge=1),
    locale: str = Query("zh-TW", description="語言代碼 (zh-TW, en-US)"),
    service: MemberService = Depends(get_member_service),
):
    return service.get_members_by_department(department_id=department_id, locale=locale)