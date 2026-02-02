from typing import List
from fastapi import APIRouter, Depends, Query
from app.schemas.member_schema import DepartmentMemberView
from app.services.member_service import MemberService
from app.dependencies import get_member_service

# 建議：這裡是撈取成員，但回傳結構是以「部門」為單位，
# 若未來有單純撈取「所有成員扁平列表」的需求，可以區分不同路由。
# 目前先維持設定的 prefix="/members" 不然還要改來改去
router = APIRouter(
    prefix="/members",
    tags=["Organization Members"]
)

@router.get(
    "/",
    response_model=List[DepartmentMemberView]
)
def list_department_members(
    locale: str = Query(
        "zh-TW",
        description="語言代碼（例如 zh-TW、en-US）"
    ),
    service: MemberService = Depends(get_member_service)
):
    """
    取得所有「啟用中的部門」及其成員資料。
    
    API 行為：
    1. 撈取所有 is_active=True 的部門 (Repository 層處理)
    2. 每個部門包含其 status!=3 (非離職) 的成員 (Repository 層處理)
    3. 根據 locale 轉換多語系欄位 (Service 層處理)

    回傳資料結構 (DepartmentMemberView)：
    [
      {
        "id": 1,
        "name": "學務處",
        "description": "<p>部門介紹...</p>",
        "website_url": "https://...",
        "sort_order": 10,
        "members": [
          {
            "id": 101,
            "name": "王小明",
            "job_title": "副學務長",
            "job_description": ["綜理學務"],
            "status": 1
          }
        ]
      },
      ...
    ]
    """
    # 直接呼叫 Service 層處理好的方法
    return service.get_organized_members(locale=locale)