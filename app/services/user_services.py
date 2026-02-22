from sqlalchemy.orm import Session
from app.models.user import User
from app.core.exceptions import UserNotFoundError

class UserService:
    @staticmethod
    def get_user_by_id(db:Session, id: int) -> User:
        user =  db.query(User).filter(User.id == id).first()
        if not user:
            raise UserNotFoundError
        return user
    
    @staticmethod
    def get_user_by_email(db:Session,email:str) -> User:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise UserNotFoundError
        return user