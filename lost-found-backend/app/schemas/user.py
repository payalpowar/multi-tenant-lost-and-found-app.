from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    tenant_id: int
    username: str
    email: EmailStr
    password: str
    role: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None


class UserResponse(BaseModel):
    user_id: int
    tenant_id: int
    username: str
    email: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True
