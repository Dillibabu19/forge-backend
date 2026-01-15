from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.refresh_tokens import RefreshTokens
from app.models.user import User

from app.core.refresh_tokens import generate_refresh_token,hash_token

from datetime import datetime,timedelta,timezone

from app.core.exceptions import InvalidToken,TokenAlreadyRevoked,TokenExpired,UserNotFoundError

class TokenService:

    @staticmethod
    def get_active_token(db: Session,*,user_id:int) -> str:
        return db.query(RefreshTokens).filter(RefreshTokens.user_id==user_id,RefreshTokens.is_revoked==False,RefreshTokens.expires_at<datetime.now(timezone.utc))
    
    @staticmethod
    def login_or_rotate_token(db: Session,*,user_id: int) -> str:
        existing_tokens = TokenService.get_active_token(db,user_id=user_id)
        for existing_token in existing_tokens:
            existing_token.is_revoked = True
            db.add(existing_token)
        return TokenService.generate_user_refresh_token(db,user_id=user_id)

    @staticmethod
    def generate_user_refresh_token(db:Session,*,user_id:int) -> str:
        token = generate_refresh_token(64)
        hashed_token = hash_token(token)
        refresh_token = RefreshTokens(
            user_id=user_id,
            token_hash=hashed_token,
            expires_at=datetime.now(timezone.utc) + timedelta(days=30)
        )
        db.add(refresh_token)

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise ValueError

        db.refresh(refresh_token)
        return token
    

    @staticmethod
    def rotate_refresh_token(db:Session,*,token:str) -> str:
        hashed_token = hash_token(token)
        print(f"token : {token}, Hashed Token: {hashed_token}")
        rec = db.query(RefreshTokens).filter(RefreshTokens.token_hash == hashed_token).first()
        print(rec)

        if not rec:
            raise InvalidToken()
        
        if rec.is_revoked:
            raise TokenAlreadyRevoked()
        
        if rec.expires_at < datetime.now(timezone.utc):
            raise TokenExpired()
        
        user = db.query(User).filter(User.id == rec.user_id).first()

        if not user:
            raise UserNotFoundError
        
        rec.is_revoked = True
        db.add(rec)
        new_refresh_token = TokenService.generate_user_refresh_token(db,user_id=user.id)

        return new_refresh_token,user.id
        
