from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    role_id: Optional[uuid.UUID] = None
    is_active: Optional[bool] = None