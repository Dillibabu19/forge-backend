from datetime import datetime, timedelta, timezone
from jose import jwt

from app.core.config import settings

def create_access_token(*,subject:str) -> str:
    now = datetime.now(tz=timezone.utc)

    payload = {
        "sub": subject,
        "iat": now,
        "exp": now+timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    }

    return jwt.encode(payload,settings.JWT_SECRET_KEY,algorithm=settings.JWT_ALGORITHM)