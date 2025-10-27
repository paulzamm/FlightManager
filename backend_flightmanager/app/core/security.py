from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings

# Configuración OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Configuración de PassLib para hasheo
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

# --- Funciones de Contraseña ---
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña plana coincide con el hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Genera un hash de la contraseña."""
    return pwd_context.hash(password)

# --- Funciones de JWT ---
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Crea un nuevo token de acceso JWT."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception) -> str:
    """Valida el token JWT y devuelve el email (subject)."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return email

# --- Dependencia de Usuario Actual ---
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(lambda: None)  # Placeholder, se obtiene manualmente
):
    """
    Dependencia para obtener el usuario actual desde el token JWT.
    Úsala en endpoints protegidos: current_user: Usuario = Depends(get_current_user)
    """
    from app.database.database import get_db
    from app.crud import crud_user
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    email = verify_token(token, credentials_exception)
    
    # Obtener la sesión de base de datos manualmente
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        user = crud_user.get_user_by_email(db, email=email)
        if user is None:
            raise credentials_exception
        return user
    finally:
        try:
            db_gen.close()
        except:
            pass
