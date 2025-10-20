from sqlalchemy.orm import Session
from app.database import Usuario
from app.schemas import UserCreate
from app.core import get_password_hash

def get_user_by_email(db: Session, email: str) -> Usuario:
    """Busca un usuario por su email."""
    return db.query(Usuario).filter(Usuario.email == email).first()

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