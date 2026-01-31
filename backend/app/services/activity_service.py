# app/services/activity_service.py
from typing import List
from app.repositories.activity_repository import ActivityRepository
from app.schemas.activity_schema import ActivityListView

# 設定一個預設圖片常數 (可依實際專案路徑修改)
DEFAULT_ACTIVITY_IMAGE = "assets/images/default_activity.jpg"

class ActivityService:
    def __init__(self, repository: ActivityRepository):
        self.repository = repository

    def get_activities(self) -> List[ActivityListView]:
        """
        取得前端所需的活動列表資料
        邏輯：
        1. 撈取全量資料
        2. 轉換圖片路徑 (無本地圖則使用預設圖)
        3. 轉換為 DTO
        """
        # 1. 從 Repo 拿資料
        raw_activities = self.repository.get_all()

        # 2. 轉換與組裝
        return [
            self._transform_to_list_view(activity)
            for activity in raw_activities
        ]

    def _transform_to_list_view(self, activity) -> ActivityListView:
        """
        單筆轉換邏輯
        """
        # 處理圖片路徑優先權：
        # 有 local_img_path 就用，沒有就用預設圖
        # 完全忽略 img_url (因為學校伺服器慢)
        final_img_path = activity.local_img_path if activity.local_img_path else DEFAULT_ACTIVITY_IMAGE

        return ActivityListView(
            id=activity.id,
            title=activity.title,
            link=activity.link,
            status=activity.status,
            local_img_path=final_img_path,
            views=activity.views,
            joined=activity.joined,
            target_audience=activity.target_audience or [], # 防呆：如果是 None 轉為空 list
            hour_labels=activity.hour_labels or [],
            sdg_labels=activity.sdg_labels or []
        )