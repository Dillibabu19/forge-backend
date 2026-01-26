from fastapi import Request
import time

def is_allow_request(key:str,limit:int, window_sec:int,redis):
    now = int(time.time())
    window_start = now - window_sec

    redis.zremrangebyscore(key,0,window_start)

    count = redis.zcard(key)

    if count>=limit:
        return False
    
    redis.zadd(key,{now:now})
    redis.expire(key,window_sec)

    return True

def build_rate_limit_key(
    *,
    request: Request,
    user_id: int | None = None,
) -> str:
    
    path = request.url.path
    method = request.method

    if user_id:
        return f"rl:user:{user_id}:{method}:{path}"

    ip = request.client.host
    return f"rl:ip:{ip}:{method}:{path}"