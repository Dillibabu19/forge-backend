from fastapi import APIRouter,HTTPException,Depends,status,Request,Response
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.services.user_services import UserService
from app.core.exceptions import UserNotFoundError
from app.schemas.user import UserUpdate
import logging

logger=logging.getLogger(__name__)
router = APIRouter(prefix="/user", tags=["user"])

@router.get('/')
async def get_users(db:Session = Depends(get_db)):
    users = UserService.get_all_users(db)
    return users

@router.get("/{user_id}")
async def get_user(user_id: str, db: Session = Depends(get_db)):
    try:
        user = UserService.get_user_by_id(db,id=user_id)
        return user
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")

@router.put("/{user_id}")
async def update_user(user_id: str, user_data: UserUpdate, db: Session = Depends(get_db)):
    try:
        user = UserService.update_user(user_id, user_data, db)
        return user
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")

@router.delete("/{user_id}")
async def delete_user(user_id: str, db: Session = Depends(get_db)):
    try:
        UserService.delete_user(db,user_id=user_id)
        return {'sucess':True}
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")

