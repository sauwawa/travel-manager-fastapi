# app/utils/otp.py
import secrets, hashlib

def gen_6digit() -> str:
    # 000000～999999，左側補零
    return f"{secrets.randbelow(1_000_000):06d}"

def hash_code(code: str) -> str:
    return hashlib.sha256(code.encode("utf-8")).hexdigest()

def normalize_email(email: str) -> str:
    return (email or "").strip().lower()