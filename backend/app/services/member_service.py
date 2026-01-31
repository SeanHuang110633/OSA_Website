# app/services/member_service.py
from typing import List, Optional, Any
from fastapi import HTTPException

from app.schemas.member_schema import (
    DepartmentPublic,
    MemberPublic,
    DepartmentWithMembers,
)
from app.repositories.member_repository import MemberRepository


class MemberService:
    def __init__(self, repository: MemberRepository):
        self.repository = repository

    # ========== Public APIs ==========

    def get_departments(self, locale: str) -> List[DepartmentPublic]:
        raw = self.repository.get_departments()
        return [
            DepartmentPublic(
                id=d.id,
                name=self._get_json_text(d.name, locale, default="Unknown Department"),
                email=d.email,
                website_url=self._get_json_text(d.website_url, locale, default=None) if d.website_url else None,
                image_path=d.image_path,
            )
            for d in raw
        ]

    def get_members_by_department(self, department_id: int, locale: str) -> DepartmentWithMembers:
        dept = self.repository.get_department_by_id(department_id)
        if not dept:
            raise HTTPException(status_code=404, detail="Department not found")

        members = self.repository.get_members_by_department(department_id=department_id, status=1)

        dept_dto = DepartmentPublic(
            id=dept.id,
            name=self._get_json_text(dept.name, locale, default="Unknown Department"),
            email=dept.email,
            website_url=self._get_json_text(dept.website_url, locale, default=None) if dept.website_url else None,
            image_path=dept.image_path,
        )

        member_dtos = [self._transform_member(m, locale) for m in members]

        return DepartmentWithMembers(department=dept_dto, members=member_dtos)

    # ========== Helpers ==========

    def _get_json_text(self, data_dict: dict, locale: str, default: Optional[str] = "Unknown") -> Optional[str]:
        if not data_dict:
            return default
        return data_dict.get(locale) or data_dict.get("zh-TW") or default

    def _get_json_list(self, data_dict: Any, locale: str) -> List[str]:
        """
        job_description 在 seed 看起來可能是：
        - {"zh-TW": ["...", "..."], "en-US": []}
        - 或者 {"zh-TW": "..."}（如果之後有人改成字串）
        - 或者 None
        這裡統一整理成 list[str] 給前端好渲染（UI/UX 乾淨）
        """
        if not data_dict:
            return []

        value = None
        if isinstance(data_dict, dict):
            value = data_dict.get(locale)
            if value is None:
                value = data_dict.get("zh-TW")

        if value is None:
            return []

        if isinstance(value, list):
            return [str(x) for x in value if x is not None]
        if isinstance(value, str):
            return [value] if value.strip() else []

        return []

    def _transform_member(self, m, locale: str) -> MemberPublic:
        return MemberPublic(
            id=m.id,
            department_id=m.department_id,
            name=self._get_json_text(m.name, locale, default="Unknown"),
            job_title=self._get_json_text(m.job_title, locale, default=None) if m.job_title else None,
            job_description=self._get_json_list(m.job_description, locale),
            email=m.email,
            tel=m.tel,
            photo_path=m.photo_path,
            status=m.status,
            sort_order=m.sort_order,
        )