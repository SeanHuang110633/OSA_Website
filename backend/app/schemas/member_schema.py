# app/schemas/member_schema.py
from typing import Optional, List
from pydantic import BaseModel


class DepartmentPublic(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    website_url: Optional[str] = None
    image_path: Optional[str] = None


class MemberPublic(BaseModel):
    id: int
    department_id: int
    name: str

    job_title: Optional[str] = None
    job_description: List[str] = []

    email: Optional[str] = None
    tel: Optional[str] = None
    photo_path: Optional[str] = None

    status: int
    sort_order: int


class DepartmentWithMembers(BaseModel):
    department: DepartmentPublic
    members: List[MemberPublic]