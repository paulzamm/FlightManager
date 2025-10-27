from sqlalchemy.orm import Session
from typing import Optional, List
from app.database import Usuario
from app.schemas import UserCreate, UserUpdate
from app.core.security import get_password_hash

# --- CREATE ---
def create_user(db: Session, user: UserCreate) -> Usuario:
    """Crea un nuevo usuario en la BD."""
    # Hasheamos la contraseña antes de guardarla
    hashed_password = get_password_hash(user.password)
    
    db_user = Usuario(
        email=user.email,
        nombre_completo=user.nombre_completo,
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- READ ---
def get_user_by_id(db: Session, user_id: int) -> Optional[Usuario]:
    """Busca un usuario por su ID."""
    return db.query(Usuario).filter(Usuario.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[Usuario]:
    """Busca un usuario por su email."""
    return db.query(Usuario).filter(Usuario.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[Usuario]:
    """Obtiene una lista de usuarios con paginación."""
    return db.query(Usuario).offset(skip).limit(limit).all()

# --- UPDATE ---
def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[Usuario]:
    """Actualiza los datos de un usuario."""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    # Actualizar solo los campos que no son None
    update_data = user_update.model_dump(exclude_unset=True)
    
    # Si se actualiza la contraseña, hashearla
    if "password" in update_data:
        update_data["password_hash"] = get_password_hash(update_data.pop("password"))
    
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

# --- DELETE ---
def delete_user(db: Session, user_id: int) -> bool:
    """Elimina un usuario de la BD."""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True

# --- VALIDACIONES ---
def user_exists(db: Session, email: str) -> bool:
    """Verifica si un usuario existe por email."""
    return db.query(Usuario).filter(Usuario.email == email).first() is not None