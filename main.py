from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
import routers_auto
from database import engine, get_db
from dependencies import verify_role_assignment, verify_family_link_permission

# Create all database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="S16 Rugby App Backup Migration API")
app.include_router(routers_auto.router, prefix="/api/v1")

# Configure CORS for Vercel Frontend
origins = [
    "http://localhost:3000",
    "http://localhost:5173", # Vite default
    "https://s16-nine.vercel.app", # Vercel Frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Mock Dependency for Current User ---
# In a real app, this would extract the JWT token, query the DB and return the current user.
# For this example, we'll simulate the current user role to test the RBAC rules.
def get_current_user_role(simulated_role: models.RoleEnum = models.RoleEnum.STAFF):
    """
    MOCK function: Returns the role of the user making the request.
    In real life this depends on the JWT Token in the Authorization header.
    """
    return simulated_role


@app.get("/")
def read_root():
    return {"message": "S16 Backend API running"}

@app.post("/users/assign-role", response_model=schemas.UserResponse)
def assign_role(
    request: schemas.RoleAssignmentRequest,
    db: Session = Depends(get_db),
    # TODO: Replace with actual auth dependency
    # current_user = Depends(get_current_active_user)
):
    """
    Assigns a role to a user. Validates the permissions of the requester.
    """
    # MOCK: Assuming the current user making the request is STAFF for demonstration.
    # In reality, extract this from the route's current_user.
    current_user_role = get_current_user_role(models.RoleEnum.STAFF)
    
    # 1. Validate if current user can assign the target role
    verify_role_assignment(current_user_role, request.new_role)
    
    # 2. Find target user
    target_user = db.query(models.User).filter(models.User.id == request.target_user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="Target user not found")
    
    # 3. Update role
    target_user.role = request.new_role
    db.commit()
    db.refresh(target_user)
    
    return target_user

@app.get("/users/pending", response_model=List[schemas.UserResponse])
def get_pending_users(
    db: Session = Depends(get_db)
):
    """
    Lista de nuevos registros (familias/jugadores) que el Staff debe validar.
    """
    # Verify if the current user is STAFF or ADMIN to view this list (optional but good practice)
    current_user_role = get_current_user_role(models.RoleEnum.STAFF)
    if current_user_role not in [models.RoleEnum.ADMIN, models.RoleEnum.STAFF]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
        
    pending_users = db.query(models.User).filter(models.User.is_pending_validation == True).all()
    return pending_users

@app.post("/users/link-family")
def link_family_player(
    request: schemas.FamilyLinkRequest,
    db: Session = Depends(get_db)
):
    """
    El rol 'STAFF' puede vincular usuarios JUGADOR y FAMILIA entre sí.
    """
    current_user_role = get_current_user_role(models.RoleEnum.STAFF)
    verify_family_link_permission(current_user_role)
    
    family = db.query(models.User).filter(models.User.id == request.family_user_id).first()
    player = db.query(models.User).filter(models.User.id == request.player_user_id).first()
    
    if not family or not player:
        raise HTTPException(status_code=404, detail="Family member or Player not found")
        
    if family.role != models.RoleEnum.FAMILIA:
        raise HTTPException(status_code=400, detail="User 1 must have FAMILIA role")
        
    if player.role != models.RoleEnum.JUGADOR:
        raise HTTPException(status_code=400, detail="User 2 must have JUGADOR role")
        
    # Check if link exists
    existing_link = db.query(models.FamilyPlayers).filter(
        models.FamilyPlayers.family_id == family.id,
        models.FamilyPlayers.player_id == player.id
    ).first()
    
    if existing_link:
        raise HTTPException(status_code=400, detail="Link already exists")
        
    new_link = models.FamilyPlayers(family_id=family.id, player_id=player.id)
    db.add(new_link)
    db.commit()
    
    return {"message": "Family member successfully linked to player."}
