"""
Member Schema
"""

from pydantic import BaseModel
from typing import List, Optional


class MemberListItem(BaseModel):
    """AboutUs/成員列表用的最小欄位集合（後續可再擴充）"""
    id: int
    name: str
    title: Optional[str] = None
    email: Optional[str] = None
    ext: Optional[str] = None
    duty: Optional[str] = None
    extra: Optional[str] = None
    avatar_url: Optional[str] = None


class MemberPaginationResponse(BaseModel):
    """成員列表回傳：items + total（先做成跟 download 類似的分頁回傳）"""
    items: List[MemberListItem]
    total: int