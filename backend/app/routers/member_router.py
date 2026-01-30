"""
Member Router
-------------
定義 Members 相關 API 路由

本 Step 3-3：
- GET /members 改成從 DB 撈資料
- dependency：Session -> Repository -> Service
"""

from fastapi import APIRouter, Depends, Query
from typing import Optional

from sqlmodel import Session

from app.core.database import get_session  # 依你專案調整：拿 DB session 的 dependency
from app.schemas.member_schema import MemberPaginationResponse
from app.repositories.member_repository import MemberRepository
from app.services.member_service import MemberService

router = APIRouter(prefix="/members", tags=["Members"])


def get_member_service(session: Session = Depends(get_session)) -> MemberService:
    """
    建立 MemberService（真 DB 版）
    - 這裡是標準依賴注入：session -> repo -> service
    """
    repo = MemberRepository(session)
    return MemberService(repo)


@router.get("/", response_model=MemberPaginationResponse)
def list_members(
    locale: str = Query("zh-TW"),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=200),
    unit_key: Optional[str] = Query(None),
    query: Optional[str] = Query(None),
    service: MemberService = Depends(get_member_service),
) -> MemberPaginationResponse:
    """成員列表 API（Step 3-3：DB 版）"""
    return service.get_members(locale=locale, page=page, size=size, unit_key=unit_key, query=query)