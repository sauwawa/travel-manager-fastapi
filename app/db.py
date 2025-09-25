# -*- coding: utf-8 -*-
# db.py
# SQLAlchemy 2.0 の初期化。SQLite を既定。MySQL へ切替は DATABASE_URL を差し替え。

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# 簡易：環境変数 DATABASE_URL があれば優先（例: mysql+pymysql://user:pass@localhost/dbname）
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///travel.db")

# SQLite の場合だけ接続引数を追加（スレッドセーフ）
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, echo=False, future=True, connect_args=connect_args)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

class Base(DeclarativeBase):
    pass

# セッション依存関数（FastAPI の Depends 用）
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
