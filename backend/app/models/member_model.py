from typing import Optional, Dict, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import JSON

class Department(SQLModel, table=True):
    __tablename__ = "departments"
    id: Optional[int] = Field(default=None, primary_key=True)
    # 儲存 {"zh-TW": "學務處", "en-US": "Office of Student Affairs"}
    name: Dict[str, str] = Field(sa_type=JSON) 
    sort_order: int = Field(default=0)
    is_active: bool = Field(default=True)
    
    # 一對多關聯：一個部門有多名成員
    members: List["Member"] = Relationship(back_populates="department")

class Member(SQLModel, table=True):
    __tablename__ = "department_members"
    id: Optional[int] = Field(default=None, primary_key=True)
    department_id: int = Field(foreign_key="departments.id")
    name: Dict[str, str] = Field(sa_type=JSON)
    job_title: Optional[Dict[str, str]] = Field(default=None, sa_type=JSON)
    # 注意：SQL 中這是一個字串陣列的 JSON
    job_description: Optional[Dict[str, List[str]]] = Field(default=None, sa_type=JSON)
    email: Optional[str] = Field(default=None)
    tel: Optional[str] = Field(default=None)
    photo_path: Optional[str] = Field(default=None)
    status: int = Field(default=1) # 1: 在職
    sort_order: int = Field(default=0)

    department: Optional[Department] = Relationship(back_populates="members")