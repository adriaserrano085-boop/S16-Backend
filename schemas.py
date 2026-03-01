from pydantic import BaseModel, EmailStr
from typing import Optional, Union
from uuid import UUID
from models import RoleEnum

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: RoleEnum = RoleEnum.JUGADOR

class UserResponse(UserBase):
    id: Union[str, UUID]
    role: RoleEnum
    is_active: bool
    is_pending_validation: bool
    
    class Config:
        from_attributes = True

class RoleAssignmentRequest(BaseModel):
    target_user_id: Union[str, UUID]
    new_role: RoleEnum

class FamilyLinkRequest(BaseModel):
    family_user_id: Union[str, UUID]
    player_user_id: Union[str, UUID]

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

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    token: str
    new_password: str
