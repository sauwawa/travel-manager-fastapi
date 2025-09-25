# -*- coding: utf-8 -*-
# app/models.py
# 純 SQLAlchemy 模型。行程/項目有 sort_order 供拖曳排序用。

from datetime import datetime, date
from typing import Optional, List

from sqlalchemy import (
    String, Integer, Date, DateTime, Boolean, ForeignKey, Text, func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class User(Base):
    __tablename__ = "users"

    # 主鍵（Primary Key：唯一識別一筆資料）
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Login ID（顯示用，保留大小寫）
    login_id: Mapped[str] = mapped_column(String(50), nullable=False)

    # 正規化 Login ID（小寫、一意約束）：用於登入比對、避免大小寫差異
    login_id_norm: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)

    # 密碼雜湊（不要存明碼）
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    # Email 與驗證
    email: Mapped[Optional[str]] = mapped_column(String(255), unique=True, nullable=True)  # 允許空白（未綁定）
    email_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # 驗證碼（僅存哈希）、有效期限
    email_code_hash: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    email_code_expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # 建立時間
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    # 關聯：一個使用者有多個 Trip
    trips: Mapped[List["Trip"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )


class Trip(Base):
    __tablename__ = "trips"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # 用 Date（日期）欄位；Python 型別對應 date
    start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    # 拖曳排序用
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    user: Mapped["User"] = relationship(back_populates="trips")
    items: Mapped[List["Item"]] = relationship(
        back_populates="trip",
        cascade="all, delete-orphan",
        order_by="Item.sort_order"
    )


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    trip_id: Mapped[int] = mapped_column(ForeignKey("trips.id", ondelete="CASCADE"), nullable=False, index=True)

    title: Mapped[str] = mapped_column(String(200), nullable=False)

    # 同樣用 Date（日期）欄位
    date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    # ‘HH:MM’ 等字串時間
    time: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # 拖曳排序用
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    trip: Mapped["Trip"] = relationship(back_populates="items")