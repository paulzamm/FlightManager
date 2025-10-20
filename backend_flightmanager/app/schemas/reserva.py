from pydantic import BaseModel, ConfigDict
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from decimal import Decimal

if TYPE_CHECKING:
    from .pasajero import Pasajero

# Esquemas para Reserva
class ReservaBase(BaseModel):
    monto_total: Decimal

class ReservaCreate(BaseModel):
    id_usuario: int
    pasajeros: List[dict]  # Lista de pasajeros con sus asientos
    monto_total: Decimal

class ReservaUpdate(BaseModel):
    estado: str  # Pendiente, Confirmada, Cancelada
    
class Reserva(ReservaBase):
    id: int
    id_usuario: int
    fecha_reserva: datetime
    estado: str
    
    model_config = ConfigDict(from_attributes=True)

# Schema completo con pasajeros
class ReservaCompleta(Reserva):
    pasajeros: List['Pasajero'] = []
    
    model_config = ConfigDict(from_attributes=True)

# Schema para listar reservas del usuario
class ReservaListado(BaseModel):
    id: int
    fecha_reserva: datetime
    estado: str
    monto_total: Decimal
    cantidad_pasajeros: int
    
    model_config = ConfigDict(from_attributes=True)
