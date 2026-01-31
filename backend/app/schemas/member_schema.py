# app/schemas/member_schema.py

from typing import List, Optional
from pydantic import BaseModel


class MemberPublic(BaseModel):
    """
    MemberPublic
    ------------
    對外（API Response）用的「成員顯示格式」

    注意：
    這個 schema 是「已經過 Service 層處理後」的結果
    - 多語系已經在 Service 層被轉成單一語言字串
    - API / Frontend 不需要再處理 i18n 結構
    """

    # 成員唯一識別 ID
    id: int

    # 成員姓名（單一語言字串）
    # 原始資料為 Dict[str, str]（多語系）
    # 但 Service 層已依 locale 選好語言並轉成 str
    name: str

    # 職稱（單一語言字串，可為空）
    # 原始資料也是 Dict[str, str]
    job_title: Optional[str] = None

    # 職務說明（條列）
    # 原始資料為 Dict[str, List[str]]
    # Service 層會依 locale 取出 List[str]
    # 前端可直接用 v-for / map 顯示
    job_description: List[str] = []

    # 電子郵件（可選）
    email: Optional[str] = None

    # 聯絡電話（可選）
    tel: Optional[str] = None

    # 成員照片路徑
    # 通常為相對路徑，例如：/uploads/members/xxx.jpg
    photo_path: Optional[str] = None

    # 成員狀態
    # 1 = 在職
    # 0 = 非在職（是否顯示由 Service 決定）
    status: int

    # 成員排序欄位
    # 用於同一部門內的顯示順序
    sort_order: int = 0


class DepartmentMemberView(BaseModel):
    """
    DepartmentMemberView
    --------------------
    API 回傳用的「部門 + 成員清單」格式

    一個 DepartmentMemberView 代表：
    - 一個部門
    - 底下所有可顯示的成員（已由 Service 整理）
    """

    # 部門 ID
    id: int

    # 部門名稱（單一語言字串）
    # 原始資料為 Dict[str, str]
    # 已由 Service 層依 locale 轉換完成
    name: str

    # 該部門底下的成員清單
    # MemberPublic 為對外顯示用 schema
    members: List[MemberPublic] = []