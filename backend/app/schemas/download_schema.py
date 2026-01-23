# backend/app/schemas/download_schema.py
from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from datetime import datetime

# ==========================================
# A. 基礎組件 Schema
# ==========================================

class CategoryPublic(BaseModel):
    """分類顯示用 (扁平化後)"""
    id: int
    slug: str
    name: str  # 已根據 locale 轉換後的名稱

class AttachmentPublic(BaseModel):
    """附件顯示用"""
    id: int
    type: str          # file, link
    file_format: Optional[str] = None
    path: str
    title: Optional[str] = None
    sort_order: int

# ==========================================
# B. 下載項目顯示用 DTO
# ==========================================

class DownloadListView(BaseModel):
    """下載列表顯示用 (包含前端要求的所有欄位)"""
    id: int
    type: str                    # law, table
    category: CategoryPublic     # 關聯的分類資訊
    title: str                   # 已轉換後的標題字串
    department: Optional[str] = None  # 已轉換後的單位名稱
    published_at: Optional[datetime] = None
    
    # 前端需求：顯示所有附件
    attachments: List[AttachmentPublic] = []

# ==========================================
# C. 分頁包裝 Schema
# ==========================================

class DownloadPaginationResponse(BaseModel):
    """分頁回傳格式"""
    total: int
    page: int
    size: int
    items: List[DownloadListView]