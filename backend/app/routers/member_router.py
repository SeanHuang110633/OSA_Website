"""
Member Router
-------------
定義 Members 相關 API 路由
"""

from fastapi import APIRouter, Depends, Query
from typing import Optional

from app.schemas.member_schema import MemberPaginationResponse
from app.services.member_service import MemberService

router = APIRouter(prefix="/members", tags=["Members"])


def get_member_service() -> MemberService:
    """
    先用簡單的 dependency（不注入 DB）
    Step 3 再改成從 dependencies.py 注入 session/repository
    """
    return MemberService()


@router.get("/", response_model=MemberPaginationResponse)
def list_members(
    locale: str = Query("zh-TW"),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=200),
    unit_key: Optional[str] = Query(None),
    query: Optional[str] = Query(None),
    service: MemberService = Depends(get_member_service),
) -> MemberPaginationResponse:
    """成員列表 API（Step 2：假資料版）"""
    return service.get_members(locale=locale, page=page, size=size, unit_key=unit_key, query=query)