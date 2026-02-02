from __future__ import annotations

from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import JSON as MySQLJSON
from typing import Optional, Dict, Any
from datetime import datetime


class Resource(SQLModel, table=True):
    __tablename__ = "resources"

    id: Optional[int] = Field(default=None, primary_key=True)
    category_id: int = Field(index=True)

    type: str = Field(default="link", max_length=20)

    # MySQL JSON 欄位
    title: Dict[str, Any] = Field(sa_column=Column(MySQLJSON), default={})
    description: Optional[Dict[str, Any]] = Field(sa_column=Column(MySQLJSON), default=None)
    url: Optional[Dict[str, Any]] = Field(sa_column=Column(MySQLJSON), default=None)
    content: Optional[Dict[str, Any]] = Field(sa_column=Column(MySQLJSON), default=None)

    sort_order: int = Field(default=0)
    is_active: bool = Field(default=True)

    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)
    deleted_at: Optional[datetime] = Field(default=None)
