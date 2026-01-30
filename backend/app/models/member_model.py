"""
Member Model
-------------
定義成員（Member）資料表結構
此 Model 將對應資料庫中的 members 表
"""

from typing import Optional
from datetime import datetime

from sqlmodel import SQLModel, Field


class Member(SQLModel, table=True):
    """
    成員資料表（members）

    注意：
    - table=True 代表這是一個資料表
    - 欄位設計以「AboutUs 成員列表」為主
    """

    __tablename__ = "members"

    # ======================
    # Primary Key
    # ======================
    id: Optional[int] = Field(default=None, primary_key=True)

    # ======================
    # Basic Info
    # ======================
    name: str = Field(nullable=False, description="成員姓名")
    title: Optional[str] = Field(default=None, description="職稱")
    email: Optional[str] = Field(default=None, description="電子郵件")
    ext: Optional[str] = Field(default=None, description="分機號碼")

    # ======================
    # Work Info
    # ======================
    duty: Optional[str] = Field(default=None, description="工作職責")
    extra: Optional[str] = Field(default=None, description="備註")

    # ======================
    # Media
    # ======================
    avatar_url: Optional[str] = Field(default=None, description="頭像圖片 URL")

    # ======================
    # Meta
    # ======================
    is_active: bool = Field(default=True, description="是否顯示於前台")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)