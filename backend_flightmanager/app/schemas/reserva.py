from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# Importar schemas de pasajero para type hints
from .pasajero import PasajeroCreate, PasajeroResponse

# Esquemas para Reserva
class ReservaBase(BaseModel):
    monto_total: Decimal

class ReservaCreate(BaseModel):
    pasajeros: List[PasajeroCreate]  # Lista de pasajeros con sus asientos

class ReservaUpdate(BaseModel):
    estado: str  # Pendiente, Confirmada, Cancelada
    
class ReservaResponse(BaseModel):
    id: int
    id_usuario: int
    fecha_reserva: datetime
    estado: str
    monto_total: Decimal
    
    model_config = ConfigDict(from_attributes=True)

# Schema completo con pasajeros
class ReservaDetail(ReservaResponse):
    pasajeros: List[PasajeroResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

# Schema para resumen de reserva
class ReservaSummary(BaseModel):
    id: int
    fecha_reserva: datetime
    estado: str
    monto_total: Decimal
    cantidad_pasajeros: int
    vuelos: List[dict] = []
    
    model_config = ConfigDict(from_attributes=True)
