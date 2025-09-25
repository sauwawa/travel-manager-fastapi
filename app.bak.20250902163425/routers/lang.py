from fastapi import APIRouter, Request, Response
from fastapi.responses import RedirectResponse
from app.i18n import LANGS

router = APIRouter()

@router.get("/lang")
def set_lang(code: str, request: Request, response: Response, next: str | None = None):
    if code not in LANGS:
        code = "ja"
    back = request.headers.get("referer") or next or "/"
    resp = RedirectResponse(url=back, status_code=303)
    resp.set_cookie("lang", code, max_age=60*60*24*365, httponly=False, samesite="lax", path="/")
    return resp
