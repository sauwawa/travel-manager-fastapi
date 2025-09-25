# -*- coding: utf-8 -*-
# routers/auth.py
# セッション Cookie に user_id / login_id を格納して認証を行う。

import re, os, hashlib, hmac, secrets, logging
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from passlib.hash import bcrypt
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_session
from ..models import User, Trip, Item
from ..i18n import get_L, get_lang
# ▼ 起動時 500 を避けるため、mail モジュールはここでは import しない
# from ..mail import send_verification_email

router = APIRouter()

# ====== 開発モード用フラグ／ユーティリティ ======
log = logging.getLogger("uvicorn.error")

def _dev_mode() -> bool:
    # 毎回 .env を読み直す（起動時固定を避ける）
    return os.getenv("DEV_PRINT_EMAIL", "1") == "1"

async def _send_code(email: str, code: str):
    if _dev_mode():
        msg = f"[DEV EMAIL] To: {email}  認証コード: {code}（15分有効）"
        print(msg)
        log.info(msg)
        return
    try:
        # 運用時のみ、必要なときに遅延 import
        from ..mail import send_verification_email
        await send_verification_email(email, code)
    except Exception as e:
        log.error(f"[MAIL ERROR] {e}")

# ====== 入力検証／共通関数 ======
# 入力検証用の正規表現（Login ID は英数字 5～20）
LOGIN_ID_RE = re.compile(r"^[A-Za-z0-9]{5,20}$")

def _now() -> datetime:
    # タイムゾーン（UTC）現在時刻
    return datetime.now(timezone.utc)

def _gen_code() -> str:
    # DEV は固定 123456（画面でも確認できる）
    return "123456" if _dev_mode() else f"{secrets.randbelow(1_000_000):06d}"

def _hash_code(code: str) -> str:
    # コードはDB/セッションに平文で置かず、SHA256 のハッシュで保存（セキュリティ向上）
    return hashlib.sha256(code.encode("utf-8")).hexdigest()

def current_user(request: Request, session: Session) -> Optional[User]:
    uid = request.session.get("user_id")
    if not uid:
        return None
    return session.get(User, uid)

def require_user(request: Request, session: Session = Depends(get_session)) -> User:
    u = current_user(request, session)
    if not u:
        # 303 で /login に飛ばす合図（フロント側で拾ってリダイレクトしてもOK）
        raise HTTPException(status_code=303, detail="redirect:/login")
    return u

def seed_template_for_user(session: Session, user: User):
    # 登録直後に「道後温泉小旅行」を自分のデータとして複製
    t = Trip(user_id=user.id, title="道後温泉小旅行（サンプル）", description="松山・道後温泉の1泊2日プラン", sort_order=0)
    session.add(t)
    session.flush()  # t.id を得る
    items = [
        Item(trip_id=t.id, title="松山城", time=" 10:00", note="ロープウェイ＋松山城観光", sort_order=0),
        Item(trip_id=t.id, title="ロープウェイ街", time=" 12:00", note="ランチ（昼食）", sort_order=1),
        Item(trip_id=t.id, title="道後温泉 本館", time=" 14:00", note="日本最古といわれる共同浴場で、 歴史情緒あふれる温泉を楽しめます", sort_order=2),
        Item(trip_id=t.id, title="道後商店街（道後ハイカラ通り）", time=" 16:00", note="温泉街を散策し、お土産やご当地グルメを楽しめます", sort_order=3),
        Item(trip_id=t.id, title="宿泊先の旅館でチェックイン", time=" 17:00", note="旅館で晩ご飯", sort_order=4),
        Item(trip_id=t.id, title="夜散歩", time="19:00", note="ライトアップされた道後温泉本館を眺めながら街歩き", sort_order=5),
        
    ]
    session.add_all(items)

# ---------- 画面：ログイン ----------
@router.get("/login")
def login_page(request: Request):
    L = get_L(get_lang(request))
    msg = request.query_params.get("msg")
    return request.app.state.templates.TemplateResponse(
        "login.html", {"request": request, "L": L, "msg": msg}
    )

# ---------- アクション：ログイン ----------
@router.post("/login")
def login_action(
    request: Request,
    login_id: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session),
):
    L = get_L(get_lang(request))
    norm = (login_id or "").lower().strip()
    user = session.execute(select(User).where(User.login_id_norm == norm)).scalar_one_or_none()
    if not user or not bcrypt.verify(password, user.password_hash):
        err = L.get("err_login_bad", "ID またはパスワードが正しくありません")
        return RedirectResponse(url=f"/login?msg={err}", status_code=303)

    request.session["user_id"] = user.id
    request.session["login_id"] = user.login_id
    return RedirectResponse(url="/", status_code=303)

# ---------- 画面：新規登録（テンプレ依存） ----------
@router.get("/register")
def register_page(request: Request):
    L = get_L(get_lang(request))
    msg = request.query_params.get("msg")
    return request.app.state.templates.TemplateResponse(
        "register.html", {"request": request, "L": L, "msg": msg}
    )

# ---------- 画面：新規登録（最小ページ／テンプレなし・デバッグ用） ----------
@router.get("/register/min", response_class=HTMLResponse)
def register_page_min():
    return HTMLResponse(
        """
        <h1>新規登録（簡易）</h1>
        <form method="post" action="/register/send-code">
            <input name="email" placeholder="Email" required />
            <input name="email_confirm" placeholder="Email(確認)" required />
            <button type="submit">コード送信</button>
        </form>
        """
    )

# ---------- アクション：認証コード送信（メール確認用 / デバッグ版） ----------
@router.post("/register/send-code")
async def register_send_code(
    request: Request,
    email: str = Form(None),
    email_confirm: str = Form(None),
):
    import traceback
    try:
        # 1) テンプレ/i18n 非依存でまず成功させる
        email = (email or "").strip().lower()
        email_confirm = (email_confirm or "").strip().lower()

        # 2) 基本チェック
        if email != email_confirm or not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
            return HTMLResponse(
                "<h3>メールアドレスが一致しないか形式が不正です。</h3>"
                "<p><a href='/register/min'>戻る</a></p>",
                status_code=400,
            )

        # 3) 生成＆セッション保存
        code = _gen_code()
        expires_at = _now() + timedelta(minutes=15)
        request.session["email_for_verif"] = email
        request.session["email_code_hash"] = _hash_code(code)
        request.session["email_code_expires_at"] = expires_at.isoformat()

        # 4) 送信（DEV は画面にも表示）
        await _send_code(email, code)
        dev_note = f"<p><b>DEV</b> 認証コード: <code>{code}</code></p>" if _dev_mode() else ""
        return HTMLResponse(
            "<h3>認証コードを送信しました。</h3>" + dev_note +
            "<p>開発モード（DEV_PRINT_EMAIL=1）では、サーバーのコンソールにもコードが表示されます。</p>"
            "<p><a href='/register/min'>戻る</a></p>"
        )
    except Exception:
        import traceback
        tb = traceback.format_exc()
        log.error(tb)
        return HTMLResponse(f"<pre style='white-space:pre-wrap'>{tb}</pre>", status_code=500)

# ---------- アクション：本登録（コード検証込み） ----------
@router.post("/register")
def register_action(
    request: Request,
    login_id: str = Form(...),
    password: str = Form(...),
    password_confirm: str = Form(...),
    email: str = Form(...),
    email_confirm: str = Form(...),
    code: str = Form(...),
    session: Session = Depends(get_session),
):
    from sqlalchemy.exc import IntegrityError

    L = get_L(get_lang(request))

    # 入力チェック
    login_id = (login_id or "").strip()
    if not LOGIN_ID_RE.fullmatch(login_id):
        msg = L.get("err_id_format", "ログインIDは英数字5～20文字で入力してください")
        return request.app.state.templates.TemplateResponse(
            "register.html", {"request": request, "L": L, "msg": msg}
        )
    if password != password_confirm or not (8 <= len(password) <= 20):
        msg = L.get("error_password_mismatch", "パスワードが一致しないか、長さが不正です")
        return request.app.state.templates.TemplateResponse(
            "register.html", {"request": request, "L": L, "msg": msg}
        )
    email = (email or "").strip().lower()
    email_confirm = (email_confirm or "").strip().lower()

    if email != email_confirm:
        msg = L.get("error_email_mismatch", "メールアドレスが一致しません")
        return request.app.state.templates.TemplateResponse(
            "register.html", {"request": request, "L": L, "msg": msg}
        )

    # セッション側のコード情報を取得
    sess_email   = request.session.get("email_for_verif")
    sess_hash    = request.session.get("email_code_hash")
    sess_expires = request.session.get("email_code_expires_at")

    ok = False
    if sess_email and sess_hash and sess_expires and sess_email == email:
        try:
            expires_dt = datetime.fromisoformat(sess_expires)
        except Exception:
            expires_dt = None
        if expires_dt and _now() <= expires_dt:
            ok = hmac.compare_digest(sess_hash, _hash_code((code or "").strip()))

    if not ok:
        msg = L.get("error_code_invalid_or_expired", "認証コードが無効または期限切れです")
        return request.app.state.templates.TemplateResponse(
            "register.html", {"request": request, "L": L, "msg": msg}
        )

    # 既存の重複チェック
    norm = login_id.lower()
    exists = session.execute(select(User).where(User.login_id_norm == norm)).scalar_one_or_none()
    if exists:
        msg = L.get("err_id_used", "このログインIDは既に使用されています")
        return RedirectResponse(url=f"/register?msg={msg}", status_code=303)

    # Email 重複チェック（DB に UNIQUE がある場合の 500 を防ぐ）
    exists_email = session.execute(select(User).where(User.email == email)).scalar_one_or_none()
    if exists_email:
        msg = L.get("err_email_used", "このメールは既に使用されています")
        return request.app.state.templates.TemplateResponse(
           "register.html", {"request": request, "L": L, "msg": msg}
    )    

    # ユーザー作成（メールは検証済みとして保存）
    # ※ users テーブルに email_verified / email_code_hash / email_code_expires_at が無い場合は、以下3行を削除してください
    user = User(
        login_id=login_id,
        login_id_norm=norm,
        password_hash=bcrypt.hash(password),
        email=email,
        # email_verified=True,
        # email_code_hash=None,
        # email_code_expires_at=None,
    )
    session.add(user); session.flush()

    # 初期テンプレを複製
    seed_template_for_user(session, user)

    # commit で UNIQUE 衝突などが起きても 500 にしない
    try:
        session.commit()
    except IntegrityError:
            session.rollback()
            msg = L.get("err_email_used", "このメールは既に使用されています")
            return request.app.state.templates.TemplateResponse(
                "register.html", {"request": request, "L": L, "msg": msg}
        )

    # セッションのコード情報を掃除
    for k in ("email_for_verif", "email_code_hash", "email_code_expires_at"):
        request.session.pop(k, None)

    # そのままログイン状態にする
    request.session["user_id"] = user.id
    request.session["login_id"] = user.login_id
    return RedirectResponse(url="/", status_code=303)

# ---------- アクション：ログアウト ----------
@router.post("/logout")
def logout_action(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)

# ---------- 非同期：JSON版 認証コード送信 ----------
@router.post("/register/send-code.json")
async def register_send_code_json(request: Request):
    L = get_L(get_lang(request))
    data = await request.form()
    email  = (data.get("email") or "").strip().lower()
    email2 = (data.get("email_confirm") or "").strip().lower()

    # 基本検査
    if email != email2 or not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return {"ok": False, "message": L.get("error_email_mismatch", "メールアドレスが一致しません")}

    # （可選）防濫発：60 秒內不重寄
    now = _now()
    last = request.session.get("last_code_sent_at")
    if last:
        try:
            if (now - datetime.fromisoformat(last)).total_seconds() < 60:
                return {"ok": False, "message": "Please wait 60s before resending."}
        except Exception:
            pass

    code = _gen_code()
    request.session["email_for_verif"]        = email
    request.session["email_code_hash"]        = _hash_code(code)
    request.session["email_code_expires_at"]  = (now + timedelta(minutes=15)).isoformat()
    request.session["last_code_sent_at"]      = now.isoformat()

    await _send_code(email, code)
    return {"ok": True, "message": L.get("code_sent", "認証コードを送信しました")}
