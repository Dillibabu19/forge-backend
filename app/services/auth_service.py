from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.refresh_tokens import RefreshTokens
from app.services.token_service import TokenService
from app.models.user import User
from app.core.security import hash_password,verify_password
from app.core.refresh_tokens import hash_token

from app.core.exceptions import UserNotFoundError,InvalidCredentialsError,UserInactiveError,UserAlreadyExistsError,InvalidToken,TokenAlreadyRevoked

class AuthService:
    @staticmethod
    def create_user(db:Session,*,email:str,password:str) -> User:
        user=User(
            email=email,
            password_hash=hash_password(password),
            is_active=True
        )
        db.add(user)

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise UserAlreadyExistsError()
        
        db.refresh(user)
        return user
    
    @staticmethod
    def authenticate_user(db:Session,*,email:str,password:str) -> User:
        user = db.query(User).filter(User.email == email).first()

        if not user:
            raise UserNotFoundError()
        
        if not user.is_active:
           raise UserInactiveError()
        
        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()
        
        return user
    
    @staticmethod
    def logout_user_all(db:Session,*,user_id:int) -> None:
        tokens = TokenService.get_active_token(db,user_id=user_id)
        for token in tokens:
            token.is_revoked=True
        db.commit()


    @staticmethod
    def logout_user_one(db:Session,*,refresh_token:str) -> None:
        hashed_token = hash_token(refresh_token)
        token = db.query(RefreshTokens).filter(RefreshTokens.token_hash == hashed_token).first()
        if not token:
            raise InvalidToken
        if token.is_revoked:
            return
        try:
            token.is_revoked=True
            db.commit()
        except Exception:
            db.rollback()
            raise