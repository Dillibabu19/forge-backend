from fastapi import APIRouter,HTTPException,Depends,status

from app.services.auth_service import AuthService

from sqlalchemy.orm import Session

from app.db.deps import get_db

from app.core.exceptions import UserAlreadyExistsError,UserInactiveError,UserNotFoundError,InvalidCredentialsError,TokenAlreadyRevoked,TokenExpired,InvalidToken
from app.schemas.auth import SignInRequest,SignUpRequest,SignInResponse,SignUpResponse,RefreshRequest,RefreshResponse,LogoutRequest,LogoutResponse

from app.core.jwt import create_access_token

from app.services.token_service import TokenService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup",response_model=SignUpResponse)
async def sign_up_user(payload: SignUpRequest,db: Session = Depends(get_db)):
    try:
        AuthService.create_user(db,email=payload.email,password=payload.password)
        return {"success": True}
    except UserAlreadyExistsError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User already exists")
    
@router.post("/login",response_model=SignInResponse)
async def sign_in_user(payload: SignInRequest,db: Session = Depends(get_db)):
    try:
        user = AuthService.authenticate_user(db,email=payload.email,password=payload.password)
        refresh_token = TokenService.login_or_rotate_token(db,user_id=user.id)
        access_token = create_access_token(subject=str(user.id))
        return {"success": True , "access_token":access_token, "refresh_token":refresh_token}
    except InvalidCredentialsError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials")
    except UserNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    except UserInactiveError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="User inactive")
    
@router.post("/refresh",response_model=RefreshResponse)
async def rotate_token(payload: RefreshRequest,db: Session= Depends(get_db)):
    try:
        new_refresh_token,user_id = TokenService.rotate_refresh_token(db, token=payload.refresh_token)
        new_access_token = create_access_token(subject=str(user_id))
        return {"success": True,"refresh_token": new_refresh_token,"access_token": new_access_token}
    except TokenAlreadyRevoked:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token Already Revoked")
    except TokenExpired:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token Expired")
    except InvalidToken:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Token")
    
@router.post("/logout",response_model=LogoutResponse)
async def logout_user(payload:LogoutRequest,db:Session=Depends(get_db)):
    try:
        AuthService.logout_user_one(db,refresh_token=payload.refresh_token)
        return {"success": True}
    except TokenAlreadyRevoked:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Session Already Logged Out")
    except InvalidToken:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Token")