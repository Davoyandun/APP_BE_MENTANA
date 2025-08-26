from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID


class CreateUserRequest(BaseModel):
    """DTO for creating a user"""
    email: EmailStr
    name: str


class UpdateUserRequest(BaseModel):
    """DTO for updating a user"""
    name: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    """DTO for user response"""
    id: UUID
    email: str
    name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    """DTO for user list response"""
    users: list[UserResponse]
    total: int
    page: int
    size: int 