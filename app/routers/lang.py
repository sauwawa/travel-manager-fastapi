# -*- coding: utf-8 -*-
# routers/lang.py
# /lang?code=xx or /lang?set=xx を受け取り Cookie "lang" をセットして前ページへ戻る。

from fastapi import APIRouter, Request, Response, Query
from fastapi.responses import RedirectResponse

router = APIRouter()

ALLOWED = {"ja", "en", "zh-Hant", "zh-Hans"}
NORMALIZE = {
    "zh": "zh-Hant", "zh_TW": "zh-Hant", "zh-TW": "zh-Hant", "tw": "zh-Hant",
    "zh_CN": "zh-Hans", "zh-CN": "zh-Hans", "cn": "zh-Hans",
    "zh-Hant": "zh-Hant", "zh-Hans": "zh-Hans",
}

def _normalize(code: str | None) -> str:
    c = (code or "").strip()
    c = NORMALIZE.get(c, c)
    return c if c in ALLOWED else "ja"

@router.get("/lang")
def set_lang(
    request: Request,
    response: Response,
    code: str | None = Query(None),   # 舊參數名
    set:  str | None = Query(None),   # 新參數名（前端用這個也OK）
    next: str | None = Query(None),   # 返回頁
):
    lang = _normalize(code or set)
    # 只允許站內路徑，避免 open redirect
    back = next if (next and next.startswith("/")) else (request.headers.get("referer") or "/")
    resp = RedirectResponse(url=back, status_code=303)
    resp.set_cookie("lang", lang, max_age=60*60*24*365, httponly=False, samesite="lax", path="/")
    return resp