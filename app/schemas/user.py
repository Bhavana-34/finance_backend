from pydantic import BaseModel, EmailStr, Field
from app.enums import RoleEnum, UserStatusEnum
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    """Schema for creating a new user"""
    username: str = Field(..., min_length=3, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: RoleEnum = RoleEnum.VIEWER


class UserUpdate(BaseModel):
    """Schema for updating user information"""
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)
    role: Optional[RoleEnum] = None
    status: Optional[UserStatusEnum] = None


class UserResponse(BaseModel):
    """Schema for user response"""
    id: int
    username: str
    email: str
    role: RoleEnum
    status: UserStatusEnum
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    """Schema for listing users (limited info)"""
    id: int
    username: str
    email: str
    role: RoleEnum
    status: UserStatusEnum

    class Config:
        from_attributes = True
