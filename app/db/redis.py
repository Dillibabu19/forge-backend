from app.core.redis import redis_user_client,redis_rl_client

def get_user_redis():
    return redis_user_client

def get_rl_redis():
    return redis_rl_client