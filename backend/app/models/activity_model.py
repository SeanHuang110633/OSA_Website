# app/models/activity_model.py
from typing import Optional, List, Dict
from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import JSON

class Activity(SQLModel, table=True):
    __tablename__ = "activities"

    # 核心識別
    id: Optional[int] = Field(default=None, primary_key=True, schema_extra={"comment": "系統內部唯一編號"})
    external_id: Optional[str] = Field(default=None, max_length=50, sa_column_kwargs={"unique": True}, schema_extra={"comment": "校方系統活動 ID"})

    # 基礎資訊
    title: str = Field(max_length=255, schema_extra={"comment": "活動標題"})
    
    # [修正點]：移除 sa_type=JSON，因為 DB 裡存的是純文字 URL，不是 JSON 格式
    link: Optional[str] = Field(default=None, schema_extra={"comment": "活動官網原始詳細連結"}) 
    
    status: Optional[str] = Field(default=None, max_length=50, schema_extra={"comment": "報名狀態"})

    # 圖片資源
    img_url: Optional[str] = Field(default=None, schema_extra={"comment": "校方原始圖片網址"})
    local_img_path: Optional[str] = Field(default=None, max_length=255, schema_extra={"comment": "伺服器本地端圖片存放路徑"})

    # 統計數據
    views: int = Field(default=0)
    joined: int = Field(default=0)

    # 標籤與分類 (這些才是真的 JSON 欄位)
    target_audience: List[str] = Field(default=[], sa_type=JSON, schema_extra={"comment": "參與對象清單"})
    hour_labels: List[str] = Field(default=[], sa_type=JSON, schema_extra={"comment": "時數類別標籤"})
    sdg_labels: List[str] = Field(default=[], sa_type=JSON, schema_extra={"comment": "SDGs 標籤"})

    # 系統欄位
    content_hash: str = Field(max_length=32, schema_extra={"comment": "MD5 雜湊值"})
    source: str = Field(default="crawler", schema_extra={"comment": "crawler 或 manual"})
    
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = Field(default=None)