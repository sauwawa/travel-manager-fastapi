from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from sqlmodel import select
from app.db import get_session
from app.models import ItineraryItem
from app.schemas import ItineraryItemRead
from sqlmodel import Session
from pydantic import BaseModel

router = APIRouter(prefix="/api/items", tags=["項目"])

class ItemUpdate(BaseModel):
    title: Optional[str] = None
    date: Optional[str] = None   # YYYY-MM-DD
    time: Optional[str] = None
    note: Optional[str] = None

@router.get("/", response_model=List[ItineraryItemRead],
            summary="項目の一覧を取得",
            description="登録されているすべての旅程項目を取得します。")
def list_items(session: Session = Depends(get_session)):
    return session.exec(select(ItineraryItem)).all()

@router.get("/{item_id}", response_model=ItineraryItemRead,
            summary="項目の詳細を取得",
            description="指定したIDの旅程項目を取得します。")
def get_item(item_id: int, session: Session = Depends(get_session)):
    item = session.get(ItineraryItem, item_id)
    if not item:
        raise HTTPException(404, "Item not found")
    return item

@router.put("/{item_id}", response_model=ItineraryItemRead,
            summary="項目を編集",
            description="指定したIDの旅程項目を更新します。")
def update_item(item_id: int, body: ItemUpdate, session: Session = Depends(get_session)):
    item = session.get(ItineraryItem, item_id)
    if not item:
        raise HTTPException(404, "Item not found")

    if body.title is not None:
        item.title = body.title
    if body.date is not None:
        item.date = body.date or None
    if body.time is not None:
        item.time = body.time or None
    if body.note is not None:
        item.note = body.note or None

    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@router.delete("/{item_id}",
               summary="項目を削除",
               description="指定したIDの旅程項目を削除します。")
def delete_item(item_id: int, session: Session = Depends(get_session)):
    item = session.get(ItineraryItem, item_id)
    if not item:
        raise HTTPException(404, "Item not found")
    session.delete(item)
    session.commit()
    return {"ok": True}
