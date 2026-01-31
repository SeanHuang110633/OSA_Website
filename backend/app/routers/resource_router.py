from fastapi import APIRouter, Depends, HTTPException, Path, Query
from typing import Optional, Literal

from app.dependencies import get_resource_service
from app.services.resource_service import ResourceService
from app.schemas.resource_schemas import ResourceListResponse, ResourceDetailResponse

router = APIRouter(prefix="/resources", tags=["resources"])
ResourceType = Literal["link", "article"]

@router.get("/", response_model=ResourceListResponse)
def read_resources(
    locale: str = Query("zh-TW"),
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=200),
    type: Optional[ResourceType] = Query(None),
    category_id: Optional[int] = Query(None, ge=1),
    query: Optional[str] = Query(None),
    service: ResourceService = Depends(get_resource_service),
):
    return service.get_resources(
        locale=locale, page=page, size=size, type=type, category_id=category_id, query=query
    )

@router.get("/{resource_id}", response_model=ResourceDetailResponse)
def read_resource_detail(
    resource_id: int = Path(..., ge=1),
    locale: str = Query("zh-TW"),
    service: ResourceService = Depends(get_resource_service),
):
    try:
        return service.get_resource_detail(resource_id=resource_id, locale=locale)
    except ValueError:
        raise HTTPException(status_code=404, detail="Resource not found")
