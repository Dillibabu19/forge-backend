from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.core.security import hash_password,verify_password

from app.core.exceptions import UserNotFoundError,InvalidCredentialsError,UserInactiveError,UserAlreadyExistsError

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
