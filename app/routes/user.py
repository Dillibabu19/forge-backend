from fastapi import APIRouter,HTTPException,Depends,status,Request,Response

from sqlalchemy.orm import Session
from app.db.deps import get_db

from app.services.user_services import UserService

import logging

logger=logging.getLogger(__name__)

router = APIRouter(prefix="/user", tags=["user"])

@router.get('/')
async def get_users(db:Session = Depends(get_db)):
    users = UserService.get_all_users(db)
    return users
