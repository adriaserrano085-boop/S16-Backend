from fastapi import HTTPException, status
from models import RoleEnum

def verify_role_assignment(current_user_role: RoleEnum, target_role: RoleEnum):
    """
    Validates if the current user has the correct role hierarchy to assign the target_role.
    
    1. Solo el rol 'ADMIN' puede crear o asignar los roles 'ADMIN' y 'STAFF'.
    2. El rol 'STAFF' puede crear usuarios y asignar los roles 'JUGADOR' y 'FAMILIA', además de vincularlos entre sí.
    3. Si un 'STAFF' intenta asignar un rol de nivel superior, el sistema debe devolver un error 403 Forbidden.
    """
    
    # Admins can do anything regarding roles
    if current_user_role == RoleEnum.ADMIN:
        return True
    
    # Staff restrictions
    if current_user_role == RoleEnum.STAFF:
        if target_role in [RoleEnum.ADMIN, RoleEnum.STAFF]:
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

def verify_family_link_permission(current_user_role: RoleEnum):
    """
    Validates if the current user can link a family member to a player.
    Only ADMIN and STAFF can do this.
    """
    if current_user_role not in [RoleEnum.ADMIN, RoleEnum.STAFF]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only ADMIN or STAFF can link family members to players."
        )
    return True
