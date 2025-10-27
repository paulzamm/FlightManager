from pydantic import BaseModel, ConfigDict
from typing import Optional
from decimal import Decimal

# Esquemas para Asiento
class AsientoBase(BaseModel):
    numero_asiento: str
    categoria: str  # Economica, Business, PrimeraClase
    precio_adicional: Decimal = Decimal('0.00')

class AsientoCreate(AsientoBase):
    id_vuelo: int

class AsientoUpdate(BaseModel):
    estado: str  # Disponible, Reservado, Ocupado
    
class Asiento(AsientoBase):
    id: int
    id_vuelo: int
    estado: str
    
    model_config = ConfigDict(from_attributes=True)

# Schema simplificado para mostrar disponibilidad
class AsientoDisponible(BaseModel):
    id: int
    numero_asiento: str
    categoria: str
    precio_adicional: Decimal
    estado: str
    
    model_config = ConfigDict(from_attributes=True)

# Alias para compatibilidad con endpoints
AsientoResponse = AsientoDisponible
