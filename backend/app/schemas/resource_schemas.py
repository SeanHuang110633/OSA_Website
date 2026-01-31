from pydantic import BaseModel
from typing import Optional, Literal

ResourceType = Literal["link", "article"]

class ResourceListItem(BaseModel):
    id: int
    category_id: int
    type: ResourceType
    title: str
    description: Optional[str] = None
    url: Optional[str] = None
    sort_order: int = 0
    is_active: bool = True

class ResourceListResponse(BaseModel):
    items: list[ResourceListItem]
    page: int
    size: int
    total: int

class ResourceDetailResponse(ResourceListItem):
    content: Optional[str] = None
