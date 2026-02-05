from fastapi import APIRouter,HTTPException,Depends,status,Request,Response

from app.services.auth_service import AuthService

from sqlalchemy.orm import Session

from app.db.deps import get_db

from app.core.exceptions import UserAlreadyExistsError,UserInactiveError,UserNotFoundError,InvalidCredentialsError,TokenAlreadyRevoked,TokenExpired,InvalidToken
from app.schemas.auth import SignInRequest,SignUpRequest,SignInResponse,SignUpResponse,RefreshRequest,RefreshResponse,LogoutRequest,LogoutResponse

from app.core.jwt import create_access_token

from app.services.token_service import TokenService

from app.api.deps.rate_limiter import rate_limit_dep
from app.api.deps.ip_dep import get_client_ip


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup",response_model=SignUpResponse)
async def sign_up_user(payload: SignUpRequest,db: Session = Depends(get_db)):
    try:
        AuthService.create_user(db,email=payload.email,password=payload.password)
        return {"success": True}
    except UserAlreadyExistsError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User already exists")
    
@router.post("/login",response_model=SignInResponse,dependencies=[Depends(rate_limit_dep)])
async def sign_in_user(payload: SignInRequest,client_ip:str =Depends(get_client_ip) ,db: Session = Depends(get_db)):
    try:
        user = AuthService.authenticate_user(db,email=payload.email,password=payload.password)
        refresh_token = TokenService.login_or_rotate_token(db,client_ip=client_ip,user_id=user.id)
        access_token = create_access_token(subject=str(user.id))
        return {"success": True , "access_token":access_token, "refresh_token":refresh_token}
    except InvalidCredentialsError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials")
    except UserNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    except UserInactiveError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="User inactive")
    
@router.post("/refresh",response_model=RefreshResponse)
async def rotate_token(request: Request,response: Response,db: Session = Depends(get_db)):
    try:
        new_refresh_token,user_id = TokenService.rotate_refresh_token(db, token=request.cookies.get('refresh_token'))
        new_access_token = create_access_token(subject=str(user_id))

        response.set_cookie(
            key='refresh_token',
            value=new_refresh_token,
            httponly=True,
            secure=False, #for testing
            path='/auth/refresh'
        )

        return {"success": True,"access_token": new_access_token}
    except TokenAlreadyRevoked:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token Already Revoked")
    except TokenExpired:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token Expired")
    except InvalidToken:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Token")
    
@router.post("/logout",response_model=LogoutResponse)
async def logout_user(request: Request, response: Response, db:Session=Depends(get_db)):
    try:
        refresh_token=request.cookies.get('refresh_token')
        if not refresh_token:
            raise InvalidToken
        
        AuthService.logout_user_one(db,refresh_token=request.cookies.get('refresh_token'))

        response.delete_cookie(
            key='refresh_token',
            path='auth/refresh',
        )
        return {"success": True}
    except TokenAlreadyRevoked:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Session Already Logged Out")
    except InvalidToken:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Token")
    
@router.post("/logout/all",response_model=LogoutResponse)
async def logout_user_all(request: Request, response: Response, db:Session=Depends(get_db)):

    user = getattr(request.state,"user",None)
    if user:
        AuthService.logout_user_all(db,user_id=user.id)
        return
    
    refresh_token = request.cookies.get('refresh_token')
    if not refresh_token:
        return
    
    user_id = TokenService.get_user_id_from_refresh(db,token=refresh_token)
    AuthService.logout_user_all(db,user_id=user_id)

