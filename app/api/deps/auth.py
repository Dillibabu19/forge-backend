from fastapi import Depends,HTTPException,status,Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session


from app.core.config import settings
from app.db.deps import get_db

from app.services.user_services import UserService

from app.db.redis import get_user_redis
import json

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db), redis = Depends(get_user_redis)):
    # try:
    #     payload = jwt.decode(token,settings.JWT_SECRET_KEY,algorithms=[settings.JWT_ALGORITHM])
    #     user_id : str | None = payload.get("sub")
    #     if not user_id:
    #         raise ValueError
    
    # except (JWTError,ValueError):
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid authentication credentials")
    
    # cache_key = f"user:{user_id}"
    # cached_user = redis.get(cache_key)
    # if cached_user:
    #     return json.loads(cached_user)
    
    # user = UserService.get_user_by_id(db,user_id)
    user = resolve_user_from_token(
        token=token,
        db=db,
        redis=redis,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    
    # data = {
    #     "id": user.id,
    #     "email": user.email,
    #     "is_active": user.is_active,
    # }
    
    # redis.setex(cache_key,600,json.dumps(data))
    
    return user

def resolve_user_from_token(*,token:str,db:Session,redis):
    try:
        payload = jwt.decode(
            token,settings.JWT_SECRET_KEY,algorithms=[settings.JWT_ALGORITHM]
        )
        user_id = payload.get("sub")
        if not user_id:
            return None
    except JWTError:
        return None
    
    cache_key = f"user:{user_id}"
    cached_user = redis.get(cache_key)
    if cached_user:
        return json.loads(cached_user)
    
    user = UserService.get_user_by_id(db,user_id)
    if not user:
        return None
    
    data = {
        "id": user.id,
        "email": user.email,
        "is_active": user.is_active,
    }
    redis.setex(cache_key, 600, json.dumps(data))

    return data