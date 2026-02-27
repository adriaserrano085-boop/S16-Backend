from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
import models
import auth_utils

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = auth_utils.decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    email = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def verify_role_assignment(current_user_role: models.RoleEnum, target_role: models.RoleEnum):
    """
    Validates if the current user has the correct role hierarchy to assign the target_role.
    
    1. Solo el rol 'ADMIN' puede crear o asignar los roles 'ADMIN' y 'STAFF'.
    2. El rol 'STAFF' puede crear usuarios y asignar los roles 'JUGADOR' y 'FAMILIA', además de vincularlos entre sí.
    3. Si un 'STAFF' intenta asignar un rol de nivel superior, el sistema debe devolver un error 403 Forbidden.
    """
    
    # Admins can do anything regarding roles
    if current_user_role == models.RoleEnum.ADMIN:
        return True
    
    # Staff restrictions
    if current_user_role == models.RoleEnum.STAFF:
        if target_role in [models.RoleEnum.ADMIN, models.RoleEnum.STAFF]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Staff cannot assign ADMIN or STAFF roles."
            )
        # Staff can assign JUGADOR and FAMILIA
        return True
    
    # Other roles (JUGADOR, FAMILIA) cannot assign roles
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have permission to assign roles."
    )

def verify_family_link_permission(current_user_role: models.RoleEnum):
    """
    Validates if the current user can link a family member to a player.
    Only ADMIN and STAFF can do this.
    """
    if current_user_role not in [models.RoleEnum.ADMIN, models.RoleEnum.STAFF]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only ADMIN or STAFF can link family members to players."
        )
    return True
