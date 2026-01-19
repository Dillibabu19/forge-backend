from pydantic import BaseModel, EmailStr

class SignUpRequest(BaseModel):
    email: EmailStr
    password: str

class SignInRequest(BaseModel):
    email: EmailStr
    password: str

class SignUpResponse(BaseModel):
    success: bool

class SignInResponse(BaseModel):
    success: bool
    access_token: str
    refresh_token: str
    
class RefreshResponse(BaseModel):
    success: bool
    refresh_token: str
    access_token: str

class RefreshRequest(BaseModel):
    refresh_token: str

class LogoutResponse(BaseModel):
    success: bool

class LogoutRequest(BaseModel):
    refresh_token: str