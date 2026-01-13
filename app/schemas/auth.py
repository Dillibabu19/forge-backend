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