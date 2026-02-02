# app/models/member_model.py
from typing import Optional, Dict, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import JSON, Text

class Department(SQLModel, table=True):
    """
    部門資料表（departments）
    """
    __tablename__ = "departments"

    id: Optional[int] = Field(default=None, primary_key=True)

    # 名稱 (JSON 多語系) {"zh-TW": "學務處", "en-US": "..."}
    name: Dict[str, str] = Field(default={}, sa_type=JSON)
    
    # 部門簡介 (JSON 多語系, HTML) {"zh-TW": "<p>...</p>", ...}
    description: Optional[Dict[str, str]] = Field(default=None, sa_type=JSON)

    # 聯絡與網站
    email: Optional[str] = Field(default=None)
    
    # 網站連結 (JSON 多語系) {"zh-TW": "https://...", "en-US": "https://..."}
    website_url: Optional[Dict[str, str]] = Field(default=None, sa_type=JSON)

    image_path: Optional[str] = Field(default=None)

    # 排序與狀態
    sort_order: int = Field(default=0)
    is_active: bool = Field(default=True, schema_extra={"comment": "1:啟用, 0:隱藏"})

    # 系統欄位
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = Field(default=None) # 軟刪除時間

    # 關聯：一個部門有多個成員
    members: List["Member"] = Relationship(back_populates="department")


class Member(SQLModel, table=True):
    """
    部門成員資料表（department_members）
    """
    __tablename__ = "department_members"

    id: Optional[int] = Field(default=None, primary_key=True)
    
    # 外鍵
    department_id: int = Field(foreign_key="departments.id")

    # 基本資料 (JSON)
    name: Dict[str, str] = Field(default={}, sa_type=JSON)
    
    # 職稱 (JSON)
    job_title: Optional[Dict[str, str]] = Field(default=None, sa_type=JSON)
    
    # [修正] 職務說明 (JSON Array)
    # 結構範例：{"zh-TW": ["公文傳遞", "場地維護"], "en-US": ["Doc delivery", "Maintenance"]}
    job_description: Optional[Dict[str, List[str]]] = Field(default=None, sa_type=JSON)

    # 聯絡資訊
    email: Optional[str] = Field(default=None)
    tel: Optional[str] = Field(default=None)
    photo_path: Optional[str] = Field(default=None)

    # 狀態：1:在職, 2:留停, 3:離職
    status: int = Field(default=1)
    
    sort_order: int = Field(default=0)

    # 系統欄位
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = Field(default=None) # 軟刪除時間

    # 關聯：成員屬於一個部門
    department: Optional[Department] = Relationship(back_populates="members")