from typing import List, Optional
from fastapi import HTTPException
from app.models.download_model import Download, DownloadAttachment
from app.schemas.download_schema import (
    DownloadListView, 
    DownloadPaginationResponse, 
    CategoryPublic, 
    AttachmentPublic
)
from app.repositories.download_repository import DownloadRepository

class DownloadService:
    def __init__(self, repository: DownloadRepository):
        self.repository = repository # 注入 Repository

    def get_downloads(
        self, 
        locale: str, 
        page: int = 1, 
        page_size: int = 10,
        dl_type: Optional[str] = None,
        category_id: Optional[int] = None,
        query: Optional[str] = None
    ) -> DownloadPaginationResponse:
        """
        取得下載列表，包含分頁與多語系處理
        """
        # 1. 計算分頁位移
        # 公式：$skip = (page - 1) \times page\_size$
        skip = (page - 1) * page_size
        
        # 2. 呼叫 Repository 獲取資料與總筆數
        raw_items, total = self.repository.get_list_with_total(
            skip=skip, 
            limit=page_size,
            dl_type=dl_type,
            category_id=category_id,
            search_query=query
        )

        # 3. 資料轉換 (Mapping)
        items = [self._transform_to_list_view(item, locale) for item in raw_items]

        return DownloadPaginationResponse(
            total=total,
            page=page,
            size=page_size,
            items=items
        )

    def get_categories(self, locale: str) -> List[CategoryPublic]:
        """
        取得所有下載分類 (多語系轉換)，供前端下拉選單使用
        """
        raw_categories = self.repository.get_categories()

        return [
            CategoryPublic(
                id=cat.id,
                slug=cat.slug,
                name=self._get_json_text(cat.names, locale, default="Unknown Category")
            )
            for cat in raw_categories
        ]
    
    # ==========================================
    # Private Helpers (DTO 轉換與邏輯處理)
    # ==========================================

    def _get_json_text(self, data_dict: dict, locale: str, default: str = "Unknown") -> str:
        """
        處理 JSON 欄位的多語系取值小工具
        邏輯：優先找指定語言 -> 找不到找繁中 -> 最後回傳預設值
        參數：
        - data_dict: 多語系 JSON 欄位 (Dict[str, str])
        - locale: 指定語言代碼
        - default: 找不到時的預設值
        """
        if not data_dict:
            return default
        return data_dict.get(locale) or data_dict.get("zh-TW") or default

    def _transform_to_list_view(self, download: Download, locale: str) -> DownloadListView:
        """
        將 Model 物件轉換為 DownloadListView Schema
        """
        # 1. 分類扁平化(扁平化是指，只取必要欄位並轉換語言)
        category_name = self._get_json_text(download.category.names, locale)
        category_dto = CategoryPublic(
            slug=download.category.slug,
            name=category_name
        )

        # 2. 標題與單位扁平化
        title = self._get_json_text(download.title, locale)
        dept = self._get_json_text(download.department, locale) if download.department else None

        # 3. 處理附件清單 (過濾掉已軟刪除的附件)
        # 注意：這是針對版本法規保留需求所實作的邏輯，因為目前的附件也不會真的被刪掉，所以撈出來的時候要在這過濾掉已經過時的法規、表格
        active_attachments = [
            AttachmentPublic(
                id=att.id,
                type=att.type,
                file_format=att.file_format,
                path=att.path,
                title=att.title,
                sort_order=att.sort_order
            )
            for att in download.attachments 
            if att.deleted_at is None  # 核心邏輯：只顯示未刪除的附件
        ]

        return DownloadListView(
            id=download.id,
            type=download.type,
            category=category_dto,
            title=title,
            department=dept,
            published_at=download.published_at,
            attachments=active_attachments
        )