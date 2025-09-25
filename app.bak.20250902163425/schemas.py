from datetime import date
from typing import Optional
from sqlmodel import SQLModel

class TripRead(SQLModel):
    model_config = {"title": "旅行"}
    id: int
    title: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None

class ItineraryItemRead(SQLModel):
    model_config = {"title": "旅程項目"}
    id: int
    trip_id: int
    date: Optional[date] = None
    time: Optional[str] = None
    title: str
    note: Optional[str] = None
