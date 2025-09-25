from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.i18n import get_lang, get_L

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/login")
def login_page(request: Request, next: str | None = None):
    L = get_L(get_lang(request))
    return templates.TemplateResponse("login.html", {"request": request, "L": L, "next": next or "/"})

@router.post("/login")
def login_action(
    request: Request,
    login_id: str = Form(...),
    password: str = Form(...),
    next: str | None = Form(None),
):
    # 這裡先不做真正驗證；成功就把 username 寫到 cookie
    dest = next or "/"
    resp = RedirectResponse(url=dest, status_code=303)
    resp.set_cookie("username", login_id, max_age=60*60*24*30, httponly=False, samesite="lax", path="/")
    return resp

@router.get("/logout")
def logout(request: Request):
    resp = RedirectResponse(url="/", status_code=303)
    resp.delete_cookie("username", path="/")
    return resp

@router.get("/register")
def register_page(request: Request):
    L = get_L(get_lang(request))
    return templates.TemplateResponse("register.html", {"request": request, "L": L, "error": None})

@router.post("/register")
def register_action(
    request: Request,
    login_id: str = Form(...),
    password: str = Form(...),
    username: str = Form(...),
    email: str = Form(...),
    email_confirm: str = Form(...),
):
    # 簡化處理：不做 DB 儲存；驗證 Email 一致後直接登入
    if email != email_confirm:
        L = get_L(get_lang(request))
        return templates.TemplateResponse("register.html", {"request": request, "L": L, "error": L["error_email_mismatch"]})
    resp = RedirectResponse(url="/", status_code=303)
    resp.set_cookie("username", username or login_id, max_age=60*60*24*30, httponly=False, samesite="lax", path="/")
    return resp
