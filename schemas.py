from pydantic import BaseModel, EmailStr
from typing import Optional
from models import RoleEnum

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: RoleEnum = RoleEnum.JUGADOR

class UserResponse(UserBase):
    id: int
    role: RoleEnum
    is_active: bool
    is_pending_validation: bool
    
    class Config:
        from_attributes = True

class RoleAssignmentRequest(BaseModel):
    target_user_id: int
    new_role: RoleEnum

class FamilyLinkRequest(BaseModel):
    family_user_id: int
    player_user_id: int
