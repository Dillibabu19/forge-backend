import redis
from app.core.config import settings

redis_user_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_USER_DB,
    decode_responses=True,
)

redis_rl_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_RL_DB,
    decode_responses=True,
)
