from pydantic import BaseModel, EmailStr
from typing import Optional
from models import RoleEnum

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: RoleEnum = RoleEnum.JUGADOR

class UserResponse(UserBase):
    id: str
    role: RoleEnum
    is_active: bool
    is_pending_validation: bool
    
    class Config:
        from_attributes = True

class RoleAssignmentRequest(BaseModel):
    target_user_id: str
    new_role: RoleEnum

class FamilyLinkRequest(BaseModel):
    family_user_id: str
    player_user_id: str

# --- Auth Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
