from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database.database import get_db
from app.database import Usuario
from app.schemas import user as user_schema, token as token_schema
from app.crud import crud_user
from app.core import security
from app.core.config import settings

router = APIRouter()

@router.post("/register", response_model=user_schema.User)
def register_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint para registrar un nuevo usuario.
    """
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado."
        )
    return crud_user.create_user(db=db, user=user)

@router.post("/token", response_model=token_schema.Token)
def login_for_access_token(
    db: Session = Depends(get_db), 
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Endpoint de Login. Valida usuario y contraseña.
    """
    user = crud_user.get_user_by_email(db, email=form_data.username)
    
    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Creamos el token JWT
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=user_schema.User)
def get_current_user_info(current_user: Usuario = Depends(security.get_current_user)):
    """
    Endpoint para obtener la información del usuario autenticado.
    Requiere token JWT válido.
    """
    return current_user