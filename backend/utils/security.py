from typing import Optional
from datetime import datetime, timedelta, timezone
from fastapi import Response, HTTPException, Cookie
import jwt
from .constants import SECRET_KEY


def genToken(user_id: int, response: Response):
    token = jwt.encode(
        {"id": user_id, "exp": datetime.now(timezone.utc) + timedelta(minutes=64)},
        SECRET_KEY,
    )
    response.set_cookie(
        key="authorisation", value=f"Bearer {token}", max_age=86400
    )  # 24h


def checkToken(authorisation: Optional[str] = Cookie(None)):
    try:
        token = authorisation.split(" ")[1]
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except Exception:
        raise HTTPException(status_code=401, detail="Not authorised")
    return True
