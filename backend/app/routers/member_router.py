from typing import List
from fastapi import APIRouter, Depends, Query
from app.schemas.member_schema import DepartmentMemberView
from app.services.member_service import MemberService
from app.dependencies import get_member_service

router = APIRouter(prefix="/members", tags=["Organization Members"])

@router.get("/", response_model=List[DepartmentMemberView])
def list_department_members(
    locale: str = Query("zh-TW", description="語言代碼"),
    service: MemberService = Depends(get_member_service)
):
    """取得所有啟用部門及其成員（不在此層做 status 過濾）"""
    return service.get_organized_members(locale=locale)