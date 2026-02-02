from typing import Optional, Dict, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import JSON


class Department(SQLModel, table=True):
    """
    部門資料表（departments）
    用來表示一個單位，例如：學務處、教務處、國際處等
    """
    __tablename__ = "departments"

    # 部門唯一識別 ID（Primary Key）
    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    # 部門名稱
    # JSON 格式，例如：
    # {
    #   "zh-TW": "學務處",
    #   "en-US": "Office of Student Affairs"
    # }
    # 前端可以依語系直接取用
    name: Dict[str, str] = Field(
        sa_type=JSON
    )

    # 排序用欄位（數字越小排序越前面）
    # 常用於前端列表顯示順序
    sort_order: int = Field(
        default=0
    )

    # 是否啟用
    # True  = 顯示 / 使用中
    # False = 停用（但資料仍保留）
    is_active: bool = Field(
        default=True
    )

    # 一對多關聯
    # 一個部門可以有多位成員（Member）
    # back_populates 需與 Member.department 對應
    members: List["Member"] = Relationship(
        back_populates="department"
    )


class Member(SQLModel, table=True):
    """
    部門成員資料表（department_members）
    用來表示每個部門底下的個別成員
    """
    __tablename__ = "department_members"

    # 成員唯一識別 ID（Primary Key）
    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    # 所屬部門 ID（Foreign Key）
    # 對應 departments.id
    department_id: int = Field(
        foreign_key="departments.id"
    )

    # 成員姓名（多語系）
    # JSON 格式，例如：
    # {
    #   "zh-TW": "王小明",
    #   "en-US": "John Wang"
    # }
    name: Dict[str, str] = Field(
        sa_type=JSON
    )

    # 職稱（多語系，可為空）
    # 例如：
    # {
    #   "zh-TW": "副學務長",
    #   "en-US": "Associate Vice President"
    # }
    job_title: Optional[Dict[str, str]] = Field(
        default=None,
        sa_type=JSON
    )

    # 職務說明（多語系 + 條列）
    # 注意：這是一個「字串陣列」的 JSON
    # 例如：
    # {
    #   "zh-TW": ["綜理學務行政", "督導各組業務"],
    #   "en-US": ["Oversee student affairs", "Supervise divisions"]
    # }
    # 前端通常會用 v-for 顯示成 <li>
    job_description: Optional[Dict[str, List[str]]] = Field(
        default=None,
        sa_type=JSON
    )

    # 電子郵件（可選）
    email: Optional[str] = Field(
        default=None
    )

    # 聯絡電話（可選）
    tel: Optional[str] = Field(
        default=None
    )

    # 成員照片路徑
    # 通常儲存相對路徑，例如：
    # /uploads/members/xxx.jpg
    photo_path: Optional[str] = Field(
        default=None
    )

    # 成員狀態
    # 1 = 在職
    # 0 = 離職 / 停用（但資料保留）
    status: int = Field(
        default=1
    )

    # 成員排序用欄位
    # 控制同一部門內的顯示順序
    sort_order: int = Field(
        default=0
    )

    # 多對一關聯
    # 每位成員只屬於一個部門
    department: Optional[Department] = Relationship(
        back_populates="members"
    )