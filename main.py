from fastapi import FastAPI, Depends, HTTPException, status
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

app = FastAPI(title="S16 Rugby App Backup Migration API")

print("Main.py: Starting imports...")
try:
    import models
    import schemas
    import routers_auto
    import auth_utils
    from database import engine, get_db
    from dependencies import verify_role_assignment, verify_family_link_permission, get_current_user
    print("Main.py: Imports successful.")
    
    # Include legitimate routes
    app.include_router(routers_auto.router, prefix="/api/v1")
except Exception as e:
    print(f"CRITICAL ERROR DURING IMPORTS in main.py: {e}")
    import traceback
    traceback.print_exc()
    
    # Override root to show error
    @app.get("/")
    def import_error(): return {"error": "Import failure", "details": str(e)}

print("Main.py: Defining basic routes...")

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Backend process is running"}

@app.get("/ping")
def ping():
    return "pong"

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

@app.on_event("startup")
def startup_db_check():
    print("FastAPI starting up...")
    try:
        print("Synchronizing database tables...")
        models.Base.metadata.create_all(bind=engine)
        print("Database synchronization successful.")
    except Exception as e:
        print(f"CRITICAL: Database synchronization failed: {e}")
        # We don't raise here to allow the app to serve diagnostic endpoints

@app.get("/")
def read_root():
    return {"message": "S16 Backend API running"}

@app.post("/token")
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth_utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth_utils.create_access_token(data={"sub": user.email, "role": user.role})
    
    # Base response
    response_data = {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email,
        "role": user.role
    }

    # Cross-reference with domain tables to find the specific profile ID (as suggested by user)
    if user.role == models.RoleEnum.JUGADOR:
        p = db.query(routers_auto.models.JugadoresPropios).filter(routers_auto.models.JugadoresPropios.email == user.email).first()
        if p: response_data["playerId"] = p.id
    elif user.role == models.RoleEnum.STAFF:
        # Try finding by auth_id (common for Staff) or email
        s = db.query(routers_auto.models.Staff).filter(
            (routers_auto.models.Staff.auth_id == str(user.id)) | 
            (routers_auto.models.Staff.nombre == user.email) # In some schemas email is stored in name fields temporarily
        ).first()
        if s: response_data["staffId"] = s.id
    elif user.role == models.RoleEnum.FAMILIA:
        f = db.query(routers_auto.models.Familias).filter(routers_auto.models.Familias.id_usuario == str(user.id)).first()
        if f: response_data["familyId"] = f.id_usuario

    return response_data

@app.post("/users/assign-role", response_model=schemas.UserResponse)
def assign_role(
    request: schemas.RoleAssignmentRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Assigns a role to a user. Validates the permissions of the requester.
    """
    # 1. Validate if current user can assign the target role
    verify_role_assignment(current_user.role, request.new_role)
    
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
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Lista de nuevos registros (familias/jugadores) que el Staff debe validar.
    """
    if current_user.role not in [models.RoleEnum.ADMIN, models.RoleEnum.STAFF]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
        
    pending_users = db.query(models.User).filter(models.User.is_pending_validation == True).all()
    return pending_users

@app.post("/users/link-family")
def link_family_player(
    request: schemas.FamilyLinkRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    El rol 'STAFF' puede vincular usuarios JUGADOR y FAMILIA entre sí.
    """
    verify_family_link_permission(current_user.role)
    
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

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
