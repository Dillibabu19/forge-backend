from app.core.secure_tokens import generate_secure_token,hash_token
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


from app.models.email_verification import EmailVerification

from app.models.user import User
from datetime import datetime,timedelta,timezone
from app.core.exceptions import InvalidToken,TokenAlreadyRevoked,TokenExpired,UserNotFoundError,TokenAlreadyUsed,UserAlreadyActive

from app.services.user_services import UserService


class EmailValidationService:
    
    @staticmethod
    def get_active_tokens(db: Session,*,hashed_token:str) -> str:
        return db.query(EmailVerification).filter(EmailVerification.token_hash==hashed_token,EmailVerification.is_used==False,EmailVerification.expires_at>datetime.now(timezone.utc)).first()
    
    
    @staticmethod
    def generate_email_validation_token(db:Session,*,user_id:int):
        raw_token = generate_secure_token()
        hashed_token = hash_token(raw_token)
        email_validation_token = EmailVerification(
            token_hash = hashed_token,
            user_id = user_id,
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=10)
        )
        db.add(email_validation_token)

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise ValueError
        
        db.refresh(email_validation_token)
        return raw_token
    
    @staticmethod
    def validate_email_token(db:Session,*,token:str):
        hashed_token = hash_token(token)
        email_token = EmailValidationService.get_active_tokens(db,hashed_token=hashed_token)
        if not email_token:
            raise InvalidToken
        
        if email_token.is_used:
            raise TokenAlreadyUsed()

        if email_token.expires_at < datetime.now(timezone.utc):
            raise TokenExpired()
        
        user = UserService.get_user_by_id(db,id=email_token.user_id)

        if user.is_active:
            raise UserAlreadyActive
        
        user.is_active = True
        email_token.is_used = True
        db.commit()
        return user

        
