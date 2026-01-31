from typing import List, Optional, Any, Dict
from app.repositories.member_repository import MemberRepository
from app.schemas.member_schema import DepartmentMemberView, MemberPublic


def pick_i18n(
    d: Optional[Dict[str, Any]],
    locale: str,
    default: str = "zh-TW"
) -> Optional[Any]:
    """
    從 i18n dict 中取出指定語言的值（多語系工具函式）

    支援常見 locale key 變形：
    - zh-TW / zh_TW / zh-tw / zh_tw
    - 大小寫差異
    - en-US / en_US / en-us

    取值優先順序：
    1. 使用者傳入的 locale（及其變形）
    2. default 語言（預設 zh-TW）
    3. dict 中的第一個值（最後保底）

    若 dict 為 None 或空 dict，直接回傳 None
    """
    if not d:
        return None

    # 所有可能嘗試的 key 候選清單
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

        # 常見硬編碼保底
        "zh-TW", "zh_TW", "zh-tw",
        "en-US", "en_US", "en-us",
    ]

    # 依序嘗試每個 key
    for k in candidates:
        if k in d and d.get(k) not in (None, ""):
            return d.get(k)

    # 最後保底：直接取 dict 的第一個值
    try:
        return next(iter(d.values()))
    except StopIteration:
        return None


def normalize_job_description(raw: Any, locale: str) -> List[str]:
    """
    將 job_description 正規化成 List[str]

    DB 中 job_description 可能有多種型態：
      1. {"zh-TW": ["a","b"], "en-US": ["..."]}  -> dict
      2. ["a","b"]                              -> list
      3. "a"                                    -> str
      4. None

    不論原始格式為何，最終都回傳：
      - List[str]
    方便前端直接條列顯示
    """

    # 無資料直接回傳空陣列
    if raw is None:
        return []

    # 多語系 dict
    if isinstance(raw, dict):
        v = pick_i18n(raw, locale)
        if v is None:
            return []

        if isinstance(v, list):
            return [str(x) for x in v]

        if isinstance(v, str):
            return [v]

        return [str(v)]

    # 已經是 list
    if isinstance(raw, list):
        return [str(x) for x in raw]

    # 單一字串
    if isinstance(raw, str):
        return [raw]

    # 其他型別（保底）
    return [str(raw)]


class MemberService:
    """
    MemberService
    -------------
    Service 層負責：
    - 商業邏輯
    - 多語系轉換（i18n）
    - 資料整理與格式轉換
    - 對齊 API Schema

    不直接操作 DB（交由 Repository）
    """

    def __init__(self, repository: MemberRepository):
        """
        初始化 Service
        repository 由 dependency injection 傳入
        """
        self.repository = repository

    def get_organized_members(self, locale: str) -> List[DepartmentMemberView]:
        """
        取得「部門 + 成員」的整理後資料（給 API 用）

        流程說明：
        1. 從 Repository 撈出完整資料（不過濾 member status）
        2. 依部門排序
        3. 成員依 sort_order / id 排序
        4. 轉換多語系欄位為單一語言字串
        5. 組成對外 API Schema
        """

        # 從 repository 取得資料（List[Department]）
        raw_data = self.repository.get_all_active_members_by_dept()

        result: List[DepartmentMemberView] = []

        # 逐一處理每個部門
        for dept in raw_data:

            # 對部門底下成員排序
            # sort_order 優先，其次用 id 確保穩定排序
            members_sorted = sorted(
                dept.members or [],
                key=lambda m: (m.sort_order or 0, m.id or 0)
            )

            member_list: List[MemberPublic] = []

            # 將每位成員轉成對外顯示格式
            for m in members_sorted:
                member_list.append(
                    MemberPublic(
                        id=m.id,
                        name=(pick_i18n(m.name, locale) or ""),
                        job_title=(
                            pick_i18n(m.job_title, locale)
                            if m.job_title else None
                        ),
                        job_description=normalize_job_description(
                            m.job_description,
                            locale
                        ),
                        email=m.email,
                        tel=m.tel,
                        photo_path=m.photo_path,
                        status=m.status,
                        sort_order=m.sort_order or 0,
                    )
                )

            # ⚠️ 重點設計：
            # 不論該部門是否有成員，都回傳部門本身
            # members 可能是空陣列 []
            result.append(
                DepartmentMemberView(
                    id=dept.id,
                    name=(pick_i18n(dept.name, locale) or ""),
                    members=member_list,
                )
            )

        return result