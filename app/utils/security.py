# セキュリティ共通関数（パスワードハッシュ、検証コード生成/検証）

import hashlib, hmac, secrets, string
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(raw: str) -> str:
    # パスワードをbcryptでハッシュ化
    return pwd_ctx.hash(raw)

def verify_password(raw: str, hashed: str) -> bool:
    # パスワード照合
    return pwd_ctx.verify(raw, hashed)

def now_utc():
    # UTC現在時刻
    return datetime.now(timezone.utc)

def in_15min():
    # 15分後（検証コードの有効期限）
    return now_utc() + timedelta(minutes=15)

def gen_6digit_code() -> str:
    # 6桁の数字コードを生成（先頭0可）
    return ''.join(secrets.choice(string.digits) for _ in range(6))

def sha256_hex(text: str) -> str:
    # SHA256（16進）ハッシュ
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def consteq(a: str, b: str) -> bool:
    # タイミング攻撃対策の比較
    return hmac.compare_digest(a, b)