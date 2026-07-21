from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: str = Field("officer", pattern="^(admin|officer|analyst)$")
    district: Optional[str] = None
    station: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenRefreshRequest(BaseModel):
    refresh_token: str

class UserResponse(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    email: EmailStr
    role: str
    district: Optional[str] = None
    station: Optional[str] = None
    createdAt: datetime

    model_config = {
        "populate_by_name": True,
        "from_attributes": True
    }
