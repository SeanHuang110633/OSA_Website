#  app/models/download_model.py
from typing import Optional, Dict, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import JSON, ForeignKey, Column, Index, Text, String

# 1. 定義下載分類模型
class DownloadCategory(SQLModel, table=True):
    __tablename__ = "download_categories"

    id: Optional[int] = Field(default=None, primary_key=True)
    
    # slug: 網址代碼，唯一值
    slug: str = Field(max_length=50, unique=True, schema_extra={"comment": "網址代碼 (如: scholarship)"})
    
    # names: 多語系名稱 {"zh-TW": "獎學金", "en-US": "Scholarships"}
    names: Dict[str, str] = Field(default={}, sa_type=JSON, schema_extra={"comment": "多語系名稱"})

    # is_active: 是否啟用，table 中是 TINYINT(1)，在 Python 中對應 bool
    is_active: bool = Field(default=True, schema_extra={"comment": "1:啟用, 0:停用"})
    
    sort_order: int = Field(default=0)

    # Relationship: 一個分類下有多個下載項目
    downloads: List["Download"] = Relationship(back_populates="category")


# 2. 定義下載主表模型
class Download(SQLModel, table=True):
    __tablename__ = "downloads"

    id: Optional[int] = Field(default=None, primary_key=True)
    
    # 外鍵關聯到分類
    category_id: int = Field(foreign_key="download_categories.id")
    
    # 類型：使用 str 並在註解中說明 ENUM (保持與 event_attachment 相同寫法，但後續可以改成enum)
    type: str = Field(default="other", schema_extra={"comment": "law:法規, tables:表格, other:其他"})
    
    # 標題：多語系 JSON
    title: Dict[str, str] = Field(default={}, sa_type=JSON, schema_extra={"comment": "多語系標題"})
    
    # 負責單位：多語系 JSON
    department: Optional[Dict[str, str]] = Field(default=None, sa_type=JSON, schema_extra={"comment": "發布單位名稱"})

    # 狀態：0:Draft, 1:Published, 2:Archived (後續也可以改成enum)
    status: int = Field(default=1, schema_extra={"comment": "0:Draft, 1:Published, 2:Archived"})
    
    # 發布日期
    published_at: Optional[datetime] = Field(default=None)
    
    # 系統時間欄位
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = Field(default=None) # 軟刪除時間

    # 定義複合索引
    __table_args__ = (
        Index("idx_dl_cat_type", "category_id", "type"),
    )

    # --- 關聯設定 ---
    # 連結回分類
    category: Optional[DownloadCategory] = Relationship(back_populates="downloads")
    
    # 一個下載項目有多個附件，設定級聯刪除
    attachments: List["DownloadAttachment"] = Relationship(
        back_populates="download",
        sa_relationship_kwargs={"cascade": "all, delete-orphan", "order_by": "DownloadAttachment.sort_order"}
    )


# 3. 定義下載附件模型
class DownloadAttachment(SQLModel, table=True):
    __tablename__ = "download_attachments"

    id: Optional[int] = Field(default=None, primary_key=True)
    
    # 外鍵關聯到下載主表
    download_id: int = Field(
        sa_column_args=[ForeignKey("downloads.id", ondelete="CASCADE")]
    )
    
    # 附件類型：file 或 link
    type: str = Field(default="file", schema_extra={"comment": "file:檔案, link:外部連結"})
    
    # 檔案格式：pdf, doc, odf...
    file_format: Optional[str] = Field(default=None, max_length=10)
    
    # 路徑或網址
    path: str = Field(max_length=500, schema_extra={"comment": "檔案路徑或 URL"})
    
    # 顯示名稱
    title: Optional[str] = Field(default=None, max_length=255)
    
    # 排序順序
    sort_order: int = Field(default=0)

    # 軟刪除時間
    deleted_at: Optional[datetime] = Field(default=None) 

    # 定義複合索引
    __table_args__ = (
        Index("idx_dl_format", "download_id", "file_format"),
    )

    # --- 關聯設定 ---
    download: Optional[Download] = Relationship(back_populates="attachments")