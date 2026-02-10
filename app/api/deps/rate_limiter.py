from app.db.redis import get_rl_redis
from fastapi import Depends,HTTPException,status,Request
from app.core.rl import is_allow_request,build_rate_limit_key

from app.core.config import settings

def rate_limit_dep(request:Request,redis = Depends(get_rl_redis),limit:int = settings.RL_LIMIT, window_sec:int = settings.RL_WINDOW):

    user = getattr(request.state, "user", None)
    user_id = user.id if user else None

    key = build_rate_limit_key(request=request,user_id=user_id)

    if not is_allow_request(key=key,limit=limit,window_sec=window_sec,redis=redis):
        raise HTTPException(
            status_code=429,
            detail="Too many requests",
        )

def refresh_token_rate_limit(request: Request, redis = Depends(get_rl_redis)):
    return rate_limit_dep(request=request,redis=redis,limit=1,window_sec=10)