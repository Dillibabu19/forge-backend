from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session


from app.core.config import settings
from app.db.deps import get_db

from app.services.user_services import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token,settings.JWT_SECRET_KEY,algorithms=[settings.JWT_ALGORITHM])
        user_id : str | None = payload.get("sub")
        if not user_id:
            raise ValueError
    
    except (JWTError,ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid authentication credentials")
    
    user = UserService.get_user_by_id(db,user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    return user
