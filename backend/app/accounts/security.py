"""Пароли и сессии: только стандартная библиотека.

Пароль хранится как scrypt-хеш с солью: `scrypt$n$r$p$соль$хеш` (base64). Токен сессии —
случайная строка в HttpOnly-cookie; в базе лежит только её SHA-256, поэтому утечка базы не
даёт войти по чужой сессии.
"""

import base64
import hashlib
import hmac
import secrets

N, R, P = 2**14, 8, 1
SALT_BYTES = 16
KEY_BYTES = 32


def _b64(raw: bytes) -> str:
    return base64.b64encode(raw).decode("ascii")


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(SALT_BYTES)
    key = hashlib.scrypt(
        password.encode("utf-8"), salt=salt, n=N, r=R, p=P, dklen=KEY_BYTES
    )
    return f"scrypt${N}${R}${P}${_b64(salt)}${_b64(key)}"


def verify_password(password: str, stored: str) -> bool:
    try:
        scheme, n, r, p, salt, key = stored.split("$")
        if scheme != "scrypt":
            return False
        expected = base64.b64decode(key)
        actual = hashlib.scrypt(
            password.encode("utf-8"),
            salt=base64.b64decode(salt),
            n=int(n),
            r=int(r),
            p=int(p),
            dklen=len(expected),
        )
    except (ValueError, TypeError):
        return False
    return hmac.compare_digest(actual, expected)


def new_session_token() -> str:
    return secrets.token_urlsafe(32)


def token_hash(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
