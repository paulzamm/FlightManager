from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

# Esquema base
class UserBase(BaseModel):
    email: EmailStr
    nombre_completo: str

# Esquema para crear un usuario
class UserCreate(UserBase):
    password: str

# Esquema para leer un usuario
class User(UserBase):
    id: int
    
    # Configuración del modelo para permitir la conversión desde objetos ORM
    model_config = ConfigDict(from_attributes=True)
