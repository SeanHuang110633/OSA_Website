# app/dependencies.py
# 統一處理依賴注入的工廠函式

from fastapi import Depends
from app.repositories.download_repository import DownloadRepository
from sqlmodel import Session
from app.core.database import get_session
from app.repositories.event_repository import EventRepository
from app.services.event_service import EventService
from app.services.download_service import DownloadService
from app.services.activity_service import ActivityService
from app.repositories.activity_repository import ActivityRepository
from app.repositories.member_repository import MemberRepository
from app.services.member_service import MemberService

from app.services.activity_service import ActivityService
from app.repositories.activity_repository import ActivityRepository

# event_service 依賴注入工廠 (Dependency Injection Factory)
def get_event_service(session: Session = Depends(get_session)) -> EventService:
    # 建立順序：Session -> Repository -> Service
    return EventService(EventRepository(session))

# download_service 依賴注入工廠
def get_download_service(session: Session = Depends(get_session)) -> DownloadService:
    # 建立順序：Session -> Repository -> Service
    return DownloadService(DownloadRepository(session))


# activity_service 依賴注入工廠
def get_activity_service(session: Session = Depends(get_session)) -> ActivityService:
    return ActivityService(ActivityRepository(session))

def get_member_service(session: Session = Depends(get_session)) -> MemberService:
    return MemberService(MemberRepository(session))


# activity_service 依賴注入工廠
def get_activity_service(session: Session = Depends(get_session)) -> ActivityService:
    return ActivityService(ActivityRepository(session))
