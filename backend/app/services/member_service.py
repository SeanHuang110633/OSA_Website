from typing import List, Optional, Any, Dict
from app.repositories.member_repository import MemberRepository
from app.schemas.member_schema import DepartmentMemberView, MemberPublic


def pick_i18n(d: Optional[Dict[str, Any]], locale: str, default: str = "zh-TW") -> Optional[Any]:
    """
    從 i18n dict 中取值，支援常見 locale key 變形：
    zh-TW / zh_TW / zh-tw / zh_tw / 以及大小寫差異。
    取不到時：回 default → 再不行就回 dict 第一個值。
    """
    if not d:
        return None

    candidates = [
        locale,
        locale.replace("_", "-"),
        locale.replace("-", "_"),
        locale.lower(),
        locale.lower().replace("_", "-"),
        locale.lower().replace("-", "_"),
        default,
        default.replace("_", "-"),
        default.replace("-", "_"),
        default.lower(),
        default.lower().replace("_", "-"),
        default.lower().replace("-", "_"),
        "zh-TW",
        "zh_TW",
        "zh-tw",
        "en-US",
        "en_US",
        "en-us",
    ]

    for k in candidates:
        if k in d and d.get(k) not in (None, ""):
            return d.get(k)

    # 最後保底：拿 dict 第一個值
    try:
        return next(iter(d.values()))
    except StopIteration:
        return None


def normalize_job_description(raw: Any, locale: str) -> List[str]:
    """
    DB 可能長這樣：
      - {"zh-TW": ["a","b"], "en-US": ["..."]}  (dict -> list)
      - ["a","b"]                              (list)
      - "a"                                    (str)
      - None
    最終都轉成 List[str]
    """
    if raw is None:
        return []

    if isinstance(raw, dict):
        v = pick_i18n(raw, locale)
        if v is None:
            return []
        if isinstance(v, list):
            return [str(x) for x in v]
        if isinstance(v, str):
            return [v]
        return [str(v)]

    if isinstance(raw, list):
        return [str(x) for x in raw]

    if isinstance(raw, str):
        return [raw]

    return [str(raw)]


class MemberService:
    def __init__(self, repository: MemberRepository):
        self.repository = repository

    def get_organized_members(self, locale: str) -> List[DepartmentMemberView]:
        raw_data = self.repository.get_all_active_members_by_dept()
        result: List[DepartmentMemberView] = []

        for dept in raw_data:
            members_sorted = sorted(dept.members or [], key=lambda m: (m.sort_order or 0, m.id or 0))

            member_list = []
            for m in members_sorted:
                member_list.append(
                    MemberPublic(
                        id=m.id,
                        name=(pick_i18n(m.name, locale) or ""),
                        job_title=(pick_i18n(m.job_title, locale) if m.job_title else None),
                        job_description=normalize_job_description(m.job_description, locale),
                        email=m.email,
                        tel=m.tel,
                        photo_path=m.photo_path,
                        status=m.status,
                        sort_order=m.sort_order or 0,
                    )
                )

            # ✅ 不管部門有沒有成員，都回傳（members 可能是 []）
            result.append(
                DepartmentMemberView(
                    id=dept.id,
                    name=(pick_i18n(dept.name, locale) or ""),
                    members=member_list,
                )
            )

        return result