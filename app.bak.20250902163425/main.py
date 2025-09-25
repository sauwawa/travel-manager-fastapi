import warnings
warnings.filterwarnings("ignore", message=r"FieldInfo\(annotation=NoneType", category=UserWarning)

from fastapi import FastAPI
from app.db import create_db_and_tables
from app.routers import trips, auth, lang

app = FastAPI(
    title="旅行管理 API",
    description="旅行の作成・編集・一覧・項目管理・並び替え・CSV 出力・ユーザー認証を提供します。",
    version="1.1.0",
    docs_url="/docs",
    redoc_url=None,
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(auth.router)
app.include_router(trips.router)
app.include_router(lang.router)


