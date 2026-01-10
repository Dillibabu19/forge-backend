from fastapi import APIRouter,HTTPException,Depends,status

from app.services.auth_service import AuthService

from sqlalchemy.orm import Session

from app.db.deps import get_db

from app.core.exceptions import UserAlreadyExistsError,UserInactiveError,UserNotFoundError,InvalidCredentialsError
from app.schemas.auth import AuthResponse,SignInRequest,SignUpRequest

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup",response_model=AuthResponse)
async def sign_up_user(payload: SignUpRequest,db: Session = Depends(get_db)):
    try:
        AuthService.create_user(db,email=payload.email,password=payload.password)
        return {"success": True}
    except UserAlreadyExistsError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User already exists")
    
@router.post("/login",response_model=AuthResponse)
async def sign_in_user(payload: SignInRequest,db: Session = Depends(get_db)):
    try:
        AuthService.authenticate_user(db,email=payload.email,password=payload.password)
        return {"success": True}
    except InvalidCredentialsError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials")
    except UserNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    except UserInactiveError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="User inactive")