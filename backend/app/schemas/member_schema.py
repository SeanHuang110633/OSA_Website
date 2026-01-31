# app/schemas/member_schema.py
from typing import List, Optional, Dict # 確保引入 Dict
from pydantic import BaseModel

class MemberPublic(BaseModel):
    """個別成員顯示格式"""
    id: int
    name: str  # 修改：這裡應該是 str，因為 Service 已經 pick_i18n 過了
    job_title: Optional[str] = None # 修改：這裡也應該是 str
    job_description: List[str] = [] # 修改：與 Service 轉換後的 List[str] 保持一致
    email: Optional[str] = None
    tel: Optional[str] = None
    photo_path: Optional[str] = None

    status: int
    sort_order: int = 0

class DepartmentMemberView(BaseModel):
    """部門 + 成員清單"""
    id: int
    name: str
    members: List[MemberPublic] = []