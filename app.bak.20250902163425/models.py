from __future__ import annotations
from typing import Optional
from datetime import date, datetime
from sqlalchemy import Date
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    model_config = {"arbitrary_types_allowed": True}
    id: Optional[int] = Field(default=None, primary_key=True)
    # 使用者登入ID（你要輸入的「ID」）、必須唯一
    login_id: str = Field(index=True, unique=True)
    # 顯示名稱（User name）
    username: str
    # Email（唯一），會做「email 與 email確認一致」檢查
    email: str = Field(index=True, unique=True)
    # 密碼雜湊 & 鹽值（用 hashlib.pbkdf2_hmac）
    password_hash: str
    password_salt: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Trip(SQLModel, table=True):
    model_config = {"arbitrary_types_allowed": True}
    id: Optional[int] = Field(default=None, primary_key=True)
    # 所屬使用者
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", index=True)
    title: str
    start_date: Optional[date] = Field(default=None, sa_type=Date)
    end_date: Optional[date] = Field(default=None, sa_type=Date)
    description: Optional[str] = None
    order_index: Optional[int] = Field(default=None, index=True)  # 旅行列表排序

class ItineraryItem(SQLModel, table=True):
    model_config = {"arbitrary_types_allowed": True}
    id: Optional[int] = Field(default=None, primary_key=True)
    trip_id: int = Field(foreign_key="trip.id")
    date: Optional[date] = Field(default=None, sa_type=Date)
    time: Optional[str] = None
    title: str
    note: Optional[str] = None
    order_index: Optional[int] = Field(default=None, index=True)  # 行程項目排序
