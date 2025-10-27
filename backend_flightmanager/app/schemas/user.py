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
