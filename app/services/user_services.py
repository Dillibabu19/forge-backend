from sqlalchemy.orm import Session
from app.models.user import User
from app.models.roles import Roles
from app.core.exceptions import UserNotFoundError

from app.schemas.user import UserUpdate
import uuid

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
    
    @staticmethod 
    def get_all_users(db:Session) -> list:
        user = db.query(User.id,User.email,User.created_at,User.updated_at,User.is_active,Roles.name.label("role_name")).outerjoin(Roles).all()
        users = []
        for x in user:
            users.append({
                "id":x.id,
                "email":x.email,
                "is_active":x.is_active,
                "created_at":x.created_at,
                "updated_at":x.updated_at,
                "role":x.role_name if x.role_name else "No Role"
            })

        return users
    
    @staticmethod
    def update_user(db: Session,user_id: uuid.UUID, user_data: UserUpdate):
        user = UserService.get_user_by_id(db,id=user_id)
        if not user:
            return UserNotFoundError
        
        for field, value in user_data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)

        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def delete_user(db: Session,user_id: uuid.UUID):
        user = UserService.get_user_by_id(db,id=user_id)
        if not user:
            return UserNotFoundError
        db.delete(user)
        db.commit()
        return user