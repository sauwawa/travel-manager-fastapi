# -*- coding: utf-8 -*-
# app/main.py

from dotenv import load_dotenv
load_dotenv()  # 讓 .env 生效（一定放最前面）

import os, secrets
from fastapi import FastAPI, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from .db import engine, Base
from .routers import auth, trips, lang
# 🚫 注意：不要在這裡 import .mail（避免啟動時就初始化郵件）

app = FastAPI(
    title="旅行管理",
    description="多言語対応のシンプルな旅行管理アプリ",
)

# Jinja2 模板
templates = Jinja2Templates(directory="app/templates")
app.state.templates = templates

# 靜態檔案（目錄存在才掛載，避免啟動時崩）
if os.path.isdir("app/static"):
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Session 中介層
SESSION_SECRET = os.getenv("SESSION_SECRET", "dev-please-change-me-32chars")
app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET,
    same_site="lax",
    session_cookie="session",
)

# 路由
app.include_router(auth.router)
app.include_router(trips.router)
app.include_router(lang.router)

# 啟動時建立資料表（開發用；正式請用 migration）
@app.on_event("startup")
def on_start():
    Base.metadata.create_all(bind=engine)

# 測試寄信端點（把 import 放函式內，避免啟動即爆）
@app.get("/__mailtest")
async def mailtest(background_tasks: BackgroundTasks, to: str = "test@example.com"):
    from .mail import send_verification_email  # ← 延後匯入
    background_tasks.add_task(send_verification_email, to, "123456")
    return {"ok": True}
