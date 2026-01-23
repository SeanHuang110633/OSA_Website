# app/routers/download_router.py
from typing import Optional
from fastapi import APIRouter, Depends, Query, Path
from app.schemas.download_schema import CategoryPublic, DownloadPaginationResponse, DownloadListView
from app.services.download_service import DownloadService
from app.dependencies import get_download_service

# 定義 Router，標籤設為 Downloads 方便在 Swagger UI 分類
router = APIRouter(prefix="/downloads", tags=["Downloads"])

@router.get("/", response_model=DownloadPaginationResponse)
def get_downloads(
    # 1. 語言與分頁參數
    locale: str = Query("zh-TW", description="語言代碼 (zh-TW, en-US)"),
    page: int = Query(1, ge=1, description="頁碼"),
    size: int = Query(10, ge=1, le=100, description="每頁筆數"),
    
    # 2. 前端要求的篩選參數
    type: Optional[str] = Query(None, description="資源類型 (law, table)"),
    category_id: Optional[int] = Query(None, description="分類 ID"),
    query: Optional[str] = Query(None, description="標題模糊搜尋關鍵字"),
    
    # 3. 注入 Service
    service: DownloadService = Depends(get_download_service)
):
    """
    取得下載資源列表 (支援分頁、多語系、類型/分類篩選與模糊搜尋)
    """
    # 邏輯交由 Service 處理，Router 僅負責參數傳遞
    return service.get_downloads(
        locale=locale,
        page=page,
        page_size=size,
        dl_type=type,
        category_id=category_id,
        query=query
    )

@router.get("/categories", response_model=list[CategoryPublic])
def get_categories(
    locale: str = Query("zh-TW", description="語言代碼 (zh-TW, en-US)"),
    service: DownloadService = Depends(get_download_service)
):
    """
    取得下載分類列表 (多語系)
    """
    return service.get_categories(locale=locale)