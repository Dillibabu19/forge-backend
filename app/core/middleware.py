from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from app.core.redis import redis_user_client
import json
from jose import jwt
from app.core.config import settings


class AuthContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.user = None 
        request.state.user_id = None 

        auth_header = request.headers.get("Authorization")
        if auth_header:
            try:
                scheme, token = auth_header.split()
                if scheme.lower() == "bearer":
                    payload = jwt.decode(
                        token,
                        settings.JWT_SECRET_KEY,
                        algorithms=[settings.JWT_ALGORITHM],
                    )
                    user_id = payload.get("sub")
                    if user_id:
                        request.state.user_id = user_id 
                        redis = redis_user_client
                        cached = redis.get(f"user:{user_id}")
                        if cached:
                            request.state.user = json.loads(cached)
            except Exception:
                pass

        return await call_next(request)
