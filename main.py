from fastapi import FastAPI, Depends, HTTPException, status, Request, File, UploadFile
from sqlalchemy import inspect
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import shutil
import uuid
import os
import logging
import traceback
from fastapi.middleware.cors import CORSMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
import uuid

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="S16 Rugby App Backup Migration API",
    redirect_slashes=False
)

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

@app.get("/reset-admin-pwd")
@app.get("/api/v1/reset-admin-pwd")
def reset_admin_password(db: Session = Depends(get_db)):
    logger.info("ADMIN_RESET: Endpoint called.")
    user = db.query(models.User).filter(models.User.email == "adriserrajime@gmail.com").first()
    if not user:
        logger.warning("ADMIN_RESET: User adriserrajime@gmail.com NOT found in database.")
        return {"error": "User not found"}
    user.hashed_password = auth_utils.get_password_hash("bakunin1990")
    db.commit()
    logger.info("ADMIN_RESET: Password updated successfully via endpoint.")
    return {"message": "Admin password updated to bakunin1990 successfully"}

@app.get("/debug/error")
@app.get("/api/v1/debug/error")
def get_startup_error():
    return {
        "startup_error": startup_error, 
        "traceback": startup_stack if "startup_stack" in globals() else None
    }

@app.get("/debug/tables")
@app.get("/api/v1/debug/tables")
def list_tables(db: Session = Depends(get_db)):
    """
    Diagnostic endpoint to list all tables in the database.
    """
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        return {"tables": tables}
    except Exception as e:
        logger.error(f"Error inspecting tables: {e}")
        return {"error": str(e)}

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

# Middleware for proxy headers (Railway/Vercel)
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")

# Static Files for Uploads
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

@app.post("/api/v1/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user)
):
    """
    Uploads a file to the local uploads directory and returns the public URL.
    """
    if current_user.role not in [models.RoleEnum.ADMIN, models.RoleEnum.STAFF]:
        raise HTTPException(status_code=403, detail="Only Staff/Admin can upload files")
        
    try:
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Determine base URL for returning the full path
        base_url = os.getenv("APP_URL", "") # Railway usually sets this or we can infer it
        
        return {
            "filename": file.filename,
            "url": f"/uploads/{unique_filename}",
            "full_url": f"{base_url}/uploads/{unique_filename}" if base_url else f"/uploads/{unique_filename}"
        }
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

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
    email_clean = form_data.username.strip().lower()
    logger.info(f"AUTH: Login attempt for user: {email_clean}")
    
    user = db.query(models.User).filter(models.User.email.ilike(email_clean)).first()
    
    if not user:
        logger.warning(f"AUTH: Login failed - User not found: {email_clean}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    if not auth_utils.verify_password(form_data.password, user.hashed_password):
        logger.warning(f"AUTH: Login failed - Password mismatch for: {email_clean}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    logger.info(f"AUTH: Login successful for: {email_clean}")
    # --- Dynamic Role Sync (Auto-RBAC) ---
    target_role = user.role
    
    # Rule 1: Master Admin
    if user.email.lower() == "adriserrajime@gmail.com":
        target_role = models.RoleEnum.ADMIN
    else:
        # Rule 2: Check presence in Staff table (models_auto)
        import models_auto
        is_staff = db.query(models_auto.Staff).filter(
            (models_auto.Staff.auth_id == str(user.id))
        ).first()
        
        if is_staff:
            target_role = models.RoleEnum.STAFF
    
    # Update user role if it has changed
    if user.role != target_role:
        logger.info(f"Syncing role for {user.email}: {user.role} -> {target_role}")
        user.role = target_role
        db.commit()
        db.refresh(user)

    access_token = auth_utils.create_access_token(data={"sub": user.email, "role": user.role})
    
    # Base response
    response_data = {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email,
        "role": user.role
    }

    # Cross-reference with domain tables to find the specific profile ID (robust version)
    try:
        import routers_auto
        
        # Helper to check if a string is a valid UUID
        def is_valid_uuid(val):
            try:
                if not val: return False
                uuid.UUID(str(val))
                return True
            except ValueError:
                return False

        if user.role == models.RoleEnum.JUGADOR:
            p = db.query(routers_auto.models.JugadoresPropios).filter(routers_auto.models.JugadoresPropios.email == user.email).first()
            if p: response_data["playerId"] = p.id
        elif user.role == models.RoleEnum.STAFF:
            # Only query by auth_id if it's a valid UUID to avoid Postgres errors
            auth_id_str = str(user.id)
            if is_valid_uuid(auth_id_str):
                s = db.query(routers_auto.models.Staff).filter(
                    (routers_auto.models.Staff.auth_id == auth_id_str) | 
                    (routers_auto.models.Staff.nombre == user.email)
                ).first()
            else:
                # Fallback to just email/name if ID isn't a UUID
                s = db.query(routers_auto.models.Staff).filter(
                    routers_auto.models.Staff.nombre == user.email
                ).first()
            if s: response_data["staffId"] = s.id
        elif user.role == models.RoleEnum.FAMILIA:
            auth_id_str = str(user.id)
            if is_valid_uuid(auth_id_str):
                f = db.query(routers_auto.models.Familias).filter(routers_auto.models.Familias.id_usuario == auth_id_str).first()
                if f: response_data["familyId"] = f.id_usuario
    except Exception as e:
        logger.error(f"Error during login profile lookup for {user.email}: {e}")
        # Not fatal, we still have the token
        response_data["profile_warning"] = "Could not fetch domain-specific ID"

    return response_data

@app.get("/users/me")
@app.get("/api/v1/users/me")
def get_current_user_profile(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Returns the full profile of the currently authenticated user.
    """
    response_data = {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role,
        "is_active": current_user.is_active,
        "is_pending_validation": current_user.is_pending_validation
    }
    
    # Add domain-specific IDs with robust error handling
    try:
        import routers_auto # Ensure access to domain models
        
        # Helper to check if a string is a valid UUID
        def is_valid_uuid(val):
            try:
                if not val: return False
                uuid.UUID(str(val))
                return True
            except ValueError:
                return False

        if current_user.role == models.RoleEnum.JUGADOR:
            p = db.query(routers_auto.models.JugadoresPropios).filter(
                routers_auto.models.JugadoresPropios.email.ilike(current_user.email)
            ).first()
            if p: response_data["playerId"] = p.id
            
        elif current_user.role in [models.RoleEnum.STAFF, models.RoleEnum.ADMIN]:
            auth_id_str = str(current_user.id)
            if is_valid_uuid(auth_id_str):
                s = db.query(routers_auto.models.Staff).filter(
                    (routers_auto.models.Staff.auth_id == auth_id_str) | 
                    (routers_auto.models.Staff.nombre.ilike(current_user.email))
                ).first()
            else:
                s = db.query(routers_auto.models.Staff).filter(
                    routers_auto.models.Staff.nombre.ilike(current_user.email)
                ).first()
                
            if s: 
                response_data["staffId"] = s.id
    except Exception as e:
        logger.error(f"Error fetching domain profile for {current_user.email}: {e}")
        # We don't raise here, we just return the base user info
        response_data["profile_error"] = str(e)
            
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
