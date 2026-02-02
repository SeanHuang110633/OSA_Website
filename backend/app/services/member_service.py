from typing import List, Optional, Any, Dict
from app.repositories.member_repository import MemberRepository
from app.schemas.member_schema import DepartmentMemberView, MemberPublic

# ==========================================
# Helper Functions (多語系處理工具)
# ==========================================

def pick_i18n(
    d: Optional[Dict[str, Any]],
    locale: str,
    default: str = "zh-TW"
) -> Optional[Any]:
    """
    從 i18n dict 中取出指定語言的值
    """
    if not d:
        return None

    # 候選 key 清單
    candidates = [
        locale,
        locale.replace("_", "-"),
        locale.lower(),
        default,
        "zh-TW", "en-US"
    ]

    for k in candidates:
        if k in d and d.get(k) not in (None, ""):
            return d.get(k)

    # 保底：取第一個值
    try:
        return next(iter(d.values()))
    except StopIteration:
        return None

def normalize_job_description(raw: Any, locale: str) -> List[str]:
    """
    處理 job_description，確保回傳 List[str]
    Model 結構: {"zh-TW": ["事項A", "事項B"], "en-US": ["Item A"]}
    """
    if raw is None:
        return []

    # 1. 如果是 Dict (多語系)，先取出對應語言的內容
    target = raw
    if isinstance(raw, dict):
        target = pick_i18n(raw, locale)
        
    if target is None:
        return []

    # 2. 如果取出的是 List，直接轉字串回傳 (符合預期)
    if isinstance(target, list):
        return [str(x) for x in target]

    # 3. 如果取出的是字串 (髒資料或單一字串)，包成 List
    if isinstance(target, str):
        return [target]

    return [str(target)]

# ==========================================
# Service Class
# ==========================================

class MemberService:
    def __init__(self, repository: MemberRepository):
        self.repository = repository

    def get_organized_members(self, locale: str) -> List[DepartmentMemberView]:
        """
        取得「部門 + 成員」的完整視圖
        """
        # 1. 從 Repository 撈取資料 (Repository 層已處理 deleted_at 與 is_active 過濾)
        raw_depts = self.repository.get_departments_with_members()

        result: List[DepartmentMemberView] = []

        for dept in raw_depts:
            # 2. 處理部門下的成員列表
            # Repository 撈出來的 members 已經過濾掉 status!=3 (離職) 的人
            # 這裡只需要負責「排序」與「格式轉換」
            
            sorted_members = sorted(
                dept.members,
                key=lambda m: (m.sort_order, m.id) # 排序：先看 sort_order，再看 id
            )

            member_list: List[MemberPublic] = []
            for m in sorted_members:
                member_list.append(
                    MemberPublic(
                        id=m.id,
                        # 多語系欄位轉換
                        name=str(pick_i18n(m.name, locale) or ""),
                        job_title=pick_i18n(m.job_title, locale), # Optional
                        
                        # 職務說明處理
                        job_description=normalize_job_description(m.job_description, locale),
                        
                        # 一般欄位
                        email=m.email,
                        tel=m.tel,
                        photo_path=m.photo_path,
                        status=m.status,
                        sort_order=m.sort_order
                    )
                )

            # 3. 組裝部門資料 (DepartmentMemberView)
            result.append(
                DepartmentMemberView(
                    id=dept.id,
                    
                    # 多語系欄位轉換
                    name=str(pick_i18n(dept.name, locale) or ""),
                    description=pick_i18n(dept.description, locale),
                    website_url=pick_i18n(dept.website_url, locale),
                    
                    # 一般欄位
                    email=dept.email,
                    image_path=dept.image_path,
                    
                    # 排序
                    sort_order=dept.sort_order,  
                    
                    # 成員列表
                    members=member_list
                )
            )

        return result