from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

# Esquema base
class UserBase(BaseModel):
    email: EmailStr
    nombre_completo: str

# Esquema para crear un usuario
class UserCreate(UserBase):
    password: str

# Esquema para actualizar un usuario (todos los campos opcionales)
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    nombre_completo: Optional[str] = None
    password: Optional[str] = None

# Esquema para leer un usuario
class User(UserBase):
    id: int
    fecha_creacion: datetime
    
    # Configuración del modelo para permitir la conversión desde objetos ORM
    model_config = ConfigDict(from_attributes=True)

# Esquema para perfil completo con estadísticas
class UserProfile(BaseModel):
    id: int
    nombre_completo: str
    email: EmailStr
    fecha_creacion: datetime
    estadisticas: dict
    
    model_config = ConfigDict(from_attributes=True)

# Esquema para cambiar contraseña
class PasswordChange(BaseModel):
    current_password: str
    new_password: str

# Esquema para eliminar cuenta
class AccountDeletion(BaseModel):
    password: str
    confirmar_eliminacion: bool = False
