# app/schemas/activity_schema.py
from typing import List, Optional
from pydantic import BaseModel

class ActivityListView(BaseModel):
    """
    活動列表顯示用 DTO
    完全對應前端需求：title, link, status, local_img_path, views, joined, tags...
    """
    id: int
    title: str
    link: Optional[str] = None
    status: Optional[str] = None
    
    # 這是經過 Service 邏輯處理後的圖片路徑 (可能是本地圖或預設圖)
    local_img_path: str 
    
    views: int
    joined: int
    
    # JSON 欄位在 Pydantic 會自動轉為 Array
    target_audience: List[str] = []
    hour_labels: List[str] = []
    sdg_labels: List[str] = []

    class Config:
        # 讓 Pydantic 可以讀取 ORM model 的資料
        from_attributes = True