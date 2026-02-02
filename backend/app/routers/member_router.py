from typing import List
from fastapi import APIRouter, Depends, Query
from app.schemas.member_schema import DepartmentMemberView
from app.services.member_service import MemberService
from app.dependencies import get_member_service

# 建立成員相關 API Router
# prefix="/members" 代表所有路徑都會是 /api/members/...
# tags 用於 Swagger 文件分類顯示
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
    取得所有「啟用中的部門」及其成員資料

    API 層設計原則說明：
    1. 本層只負責：
       - 接收請求參數（例如 locale）
       - 呼叫 service 層
       - 回傳整理後的資料
    2. 不在 API 層做 status 過濾
       - 避免資料規則分散在多個層級
       - 確保邏輯集中在 service 層
    3. API 回傳資料結構已由 response_model 限制
       - 保證前端拿到的格式穩定
       - 自動產生 Swagger 文件

    locale 說明：
    - 由前端指定語言版本
    - service 層會依 locale 取對應語系欄位
      （例如 Department.name[locale]）

    回傳資料範例（簡化）：
    [
      {
        "department": "學務處",
        "members": [
          {
            "name": "王小明",
            "job_title": "副學務長"
          }
        ]
      }
    ]
    """

    # 呼叫 service 層進行資料整理與語系轉換
    return service.get_organized_members(locale=locale)