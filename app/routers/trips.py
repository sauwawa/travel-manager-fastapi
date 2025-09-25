# -*- coding: utf-8 -*-
# routers/trips.py
# 旅行一覧・詳細・項目操作・並べ替え API（ログイン必須）

from datetime import date
from typing import List
from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..db import get_session
from ..models import Trip, Item, User
from ..i18n import get_L, get_lang
from .auth import require_user

router = APIRouter()

@router.get("/")
def root_redirect(request: Request, session: Session = Depends(get_session)):
    # 未ログインなら /login へ、ログイン済なら /trips へ
    if not request.session.get("user_id"):
        return RedirectResponse(url="/login", status_code=303)
    return RedirectResponse(url="/trips", status_code=303)

@router.get("/trips")
def trips_list(request: Request, session: Session = Depends(get_session), user: User = Depends(require_user)):
    L = get_L(get_lang(request))
    trips = session.execute(select(Trip).where(Trip.user_id == user.id).order_by(Trip.sort_order, Trip.id)).scalars().all()
    return request.app.state.templates.TemplateResponse("trips_list.html", {"request": request, "L": L, "trips": trips})

@router.get("/trips/new")
def new_trip_page(request: Request, user: User = Depends(require_user)):
    L = get_L(get_lang(request))
    return request.app.state.templates.TemplateResponse("trip_new.html", {"request": request, "L": L})

@router.post("/trips")
def create_trip(
    request: Request,
    title: str = Form(...),
    start_date: str | None = Form(None),
    end_date: str | None = Form(None),
    description: str | None = Form(None),
    session: Session = Depends(get_session),
    user: User = Depends(require_user),
):
    # 並び順は末尾へ
    max_order = session.execute(select(Trip.sort_order).where(Trip.user_id == user.id).order_by(Trip.sort_order.desc())).scalars().first()
    order = (max_order or 0) + 1
    trip = Trip(
        user_id=user.id,
        title=title.strip(),
        start_date=(date.fromisoformat(start_date) if start_date else None),
        end_date=(date.fromisoformat(end_date) if end_date else None),
        description=(description or None),
        sort_order=order,
    )
    session.add(trip)
    session.commit()
    return RedirectResponse(url=f"/trips/{trip.id}", status_code=303)

@router.get("/trips/{trip_id}")
def trip_detail(request: Request, trip_id: int, session: Session = Depends(get_session), user: User = Depends(require_user)):
    L = get_L(get_lang(request))
    trip = session.get(Trip, trip_id)
    if not trip or trip.user_id != user.id:
        raise HTTPException(404)
    items = trip.items  # order_by を model で指定済
    return request.app.state.templates.TemplateResponse("trip_detail.html", {"request": request, "L": L, "trip": trip, "items": items})

@router.post("/trips/{trip_id}/delete")
def delete_trip(request: Request, trip_id: int, session: Session = Depends(get_session), user: User = Depends(require_user)):
    trip = session.get(Trip, trip_id)
    if not trip or trip.user_id != user.id:
        raise HTTPException(404)
    session.delete(trip)
    session.commit()
    return RedirectResponse(url="/trips", status_code=303)

@router.post("/trips/reorder")
async def reorder_trips(request: Request, session: Session = Depends(get_session), user: User = Depends(require_user)):
    data = await request.json()
    ids: list[int] = data.get("ids") or []
    # 自分の trip のみ対象
    my_ids = set([t.id for t in session.execute(select(Trip.id).where(Trip.user_id == user.id)).scalars().all()])
    order = 0
    for tid in ids:
        if tid in my_ids:
            t = session.get(Trip, tid)
            t.sort_order = order
            order += 1
    session.commit()
    return JSONResponse({"ok": True})

@router.post("/trips/{trip_id}/items")
def create_item(
    request: Request,
    trip_id: int,
    title: str = Form(...),
    date_str: str | None = Form(None),
    time: str | None = Form(None),
    note: str | None = Form(None),
    session: Session = Depends(get_session),
    user: User = Depends(require_user),
):
    trip = session.get(Trip, trip_id)
    if not trip or trip.user_id != user.id:
        raise HTTPException(404)
    max_order = session.execute(select(Item.sort_order).where(Item.trip_id == trip_id).order_by(Item.sort_order.desc())).scalars().first()
    order = (max_order or 0) + 1
    it = Item(
        trip_id=trip_id,
        title=title.strip(),
        date=(date.fromisoformat(date_str) if date_str else None),
        time=(time or None),
        note=(note or None),
        sort_order=order,
    )
    session.add(it)
    session.commit()
    return RedirectResponse(url=f"/trips/{trip_id}", status_code=303)

@router.post("/trips/{trip_id}/items/{item_id}/edit")
def edit_item(
    request: Request,
    trip_id: int,
    item_id: int,
    title: str = Form(...),
    date_str: str | None = Form(None),
    time: str | None = Form(None),
    note: str | None = Form(None),
    session: Session = Depends(get_session),
    user: User = Depends(require_user),
):
    trip = session.get(Trip, trip_id)
    if not trip or trip.user_id != user.id:
        raise HTTPException(404)
    it = session.get(Item, item_id)
    if not it or it.trip_id != trip_id:
        raise HTTPException(404)
    it.title = title.strip()
    it.date = (date.fromisoformat(date_str) if date_str else None)
    it.time = (time or None)
    it.note = (note or None)
    session.add(it)
    session.commit()
    return RedirectResponse(url=f"/trips/{trip_id}", status_code=303)

@router.post("/trips/{trip_id}/items/{item_id}/delete")
def delete_item(request: Request, trip_id: int, item_id: int, session: Session = Depends(get_session), user: User = Depends(require_user)):
    trip = session.get(Trip, trip_id)
    if not trip or trip.user_id != user.id:
        raise HTTPException(404)
    it = session.get(Item, item_id)
    if it and it.trip_id == trip_id:
        session.delete(it)
        session.commit()
    return RedirectResponse(url=f"/trips/{trip_id}", status_code=303)

@router.post("/trips/{trip_id}/items/reorder")
async def reorder_items(request: Request, trip_id: int, session: Session = Depends(get_session), user: User = Depends(require_user)):
    data = await request.json()
    ids: list[int] = data.get("ids") or []
    # 自分の trip に属する item のみ対象
    my_ids = set([i.id for i in session.execute(
        select(Item.id).join(Trip, Item.trip_id == Trip.id).where(Trip.user_id == user.id, Item.trip_id == trip_id)
    ).scalars().all()])
    order = 0
    for iid in ids:
        if iid in my_ids:
            it = session.get(Item, iid)
            it.sort_order = order
            order += 1
    session.commit()
    return JSONResponse({"ok": True})

# -*- coding: utf-8 -*-
# 日本語コメント: 旅行ヘッダ（タイトル／開始日／終了日／説明）を更新するエンドポイント
from fastapi.responses import RedirectResponse
from sqlmodel import Session

@router.post("/trips/{trip_id}/edit")
def edit_trip_action(
    trip_id: int,
    title: str = Form(...),
    start_date: str | None = Form(None),
    end_date: str | None = Form(None),
    description: str | None = Form(None),
    session: Session = Depends(get_session),
):
    # 日本語コメント: 対象の旅行を取得
    from app.models import Trip  # ループインポート回避のため関数内で import
    trip = session.get(Trip, trip_id)
    if not trip:
        raise HTTPException(404, "Trip not found")

    # 日本語コメント: 値を反映（空文字は None に正規化）
    trip.title = title
    trip.start_date = (start_date or None)
    trip.end_date = (end_date or None)
    trip.description = (description or None)

    session.add(trip)
    session.commit()

    # 日本語コメント: 編集後は元の詳細に戻る
    return RedirectResponse(url=f"/trips/{trip_id}", status_code=303)
