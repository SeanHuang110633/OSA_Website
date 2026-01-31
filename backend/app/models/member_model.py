# app/models/member_model.py
from typing import Optional, Dict, List, Any
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import JSON, ForeignKey, Index


class Department(SQLModel, table=True):
    __tablename__ = "departments"

    id: Optional[int] = Field(default=None, primary_key=True)

    # 多語系欄位
    name: Dict[str, str] = Field(default={}, sa_type=JSON)
    description: Optional[Dict[str, str]] = Field(default=None, sa_type=JSON)

    email: Optional[str] = Field(default=None, max_length=255)
    website_url: Optional[Dict[str, str]] = Field(default=None, sa_type=JSON)

    image_path: Optional[str] = Field(default=None, max_length=500)

    sort_order: int = Field(default=0)
    is_active: bool = Field(default=True)

    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = Field(default=None)

    # Relationship
    members: List["DepartmentMember"] = Relationship(back_populates="department")


class DepartmentMember(SQLModel, table=True):
    __tablename__ = "department_members"

    id: Optional[int] = Field(default=None, primary_key=True)

    department_id: int = Field(
        sa_column_args=[ForeignKey("departments.id", ondelete="RESTRICT")]
    )

    # 多語系欄位
    name: Dict[str, str] = Field(default={}, sa_type=JSON)
    job_title: Optional[Dict[str, str]] = Field(default=None, sa_type=JSON)

    # 注意：seed.sql 裡 job_description 很常是 array，所以這裡用 Any 接住（Service 再整理成 List[str]）
    job_description: Optional[Dict[str, Any]] = Field(default=None, sa_type=JSON)

    email: Optional[str] = Field(default=None, max_length=255)
    tel: Optional[str] = Field(default=None, max_length=50)
    photo_path: Optional[str] = Field(default=None, max_length=500)

    status: int = Field(default=1, schema_extra={"comment": "1:在職(依你們約定), 其他:非在職"})
    sort_order: int = Field(default=0)

    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = Field(default=None)

    __table_args__ = (
        Index("idx_dept_status", "department_id", "status"),
    )

    # Relationship
    department: Optional[Department] = Relationship(back_populates="members")