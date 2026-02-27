from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
import os
import logging
import traceback
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="S16 Rugby App Backup Migration API")

# Global Exception Handler for 500s
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global Error: {exc}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": str(exc),
            "traceback": traceback.format_exc() if os.getenv("DEBUG") else "Secret"
        }
    )

# Response logging middleware to catch what is being sent
@app.middleware("http")
async def log_responses(request: Request, call_next):
    from fastapi.responses import Response
    response = await call_next(request)
    
    # If it's a 200 OK but not JSON, let's log what it is
    content_type = response.headers.get("content-type", "")
    if response.status_code == 200 and "application/json" not in content_type:
        logger.warning(f"Non-JSON 200 Response for {request.url}: {content_type}")
        
    return response

# Storage for diagnostic info

# Storage for diagnostic info
startup_error = None

import models
import schemas
import auth_utils
from database import engine, get_db
from dependencies import verify_role_assignment, verify_family_link_permission, get_current_user

print("Main.py: Loading components...")
import routers_auto
app.include_router(routers_auto.router, prefix="/api/v1")
print("Main.py: All routers included successfully.")

@app.get("/ping")
@app.get("/api/v1/ping")
def ping():
    return JSONResponse(content={"message": "pong"})

@app.get("/health")
@app.get("/api/v1/health")
def health_check(db: Session = Depends(get_db)):
    db_status = "ok"
    try:
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"error: {str(e)}"
    return {
        "status": "ok", 
        "database": db_status,
        "startup_error": startup_error,
        "env_port": os.getenv("PORT"),
        "db_resolved": db_status == "ok"
    }

@app.get("/debug/error")
@app.get("/api/v1/debug/error")
def get_startup_error():
    return {
        "startup_error": startup_error, 
        "traceback": startup_stack if "startup_stack" in globals() else None
    }

@app.exception_handler(404)
async def custom_404_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Path not found", 
            "path": str(request.url), 
            "startup_error": startup_error,
            "message": "Verify if you are using the correct prefix (/api/v1/)."
        },
    )

# Configure CORS for Vercel Frontend
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://s16-nine.vercel.app",
    "*", # Temporary wide open for debugging
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Temporary wide open for debugging
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
@app.post("/api/v1/token")
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
@app.post("/api/v1/users/assign-role", response_model=schemas.UserResponse)
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
@app.get("/api/v1/users/pending", response_model=List[schemas.UserResponse])
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
@app.post("/api/v1/users/link-family")
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
