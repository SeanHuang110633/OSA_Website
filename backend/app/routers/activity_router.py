# app/routers/activity_router.py
from typing import List
from fastapi import APIRouter, Depends
from app.schemas.activity_schema import ActivityListView
from app.services.activity_service import ActivityService
from app.dependencies import get_activity_service

# 定義 Router
router = APIRouter(prefix="/activities", tags=["Activities"])

@router.get("/", response_model=List[ActivityListView])
def get_activities(
    # 注入 Service
    service: ActivityService = Depends(get_activity_service)
):
    """
    取得所有活動列表
    - 不分頁，一次回傳全部
    - 圖片路徑已由後端處理 (優先使用本地圖，無則使用預設圖)
    """
    return service.get_activities()