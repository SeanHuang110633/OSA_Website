from typing import List, Optional
from pydantic import BaseModel

# ==========================================
# 顯示用元件
# ==========================================

class MemberPublic(BaseModel):
    id: int
    name: str
    job_title: Optional[str] = None
    
    # [修正] 對應 Model 的 List[str]
    job_description: List[str] = []
    
    email: Optional[str] = None
    tel: Optional[str] = None
    photo_path: Optional[str] = None
    status: int
    sort_order: int

class DepartmentBase(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    website_url: Optional[str] = None
    email: Optional[str] = None
    image_path: Optional[str] = None
    sort_order: int

# ==========================================
# API 回傳結構
# ==========================================

class DepartmentMemberView(DepartmentBase):
    """
    包含成員列表的部門視圖
    """
    members: List[MemberPublic] = []