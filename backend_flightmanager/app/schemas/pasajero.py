from pydantic import BaseModel, ConfigDict
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .asiento import AsientoDisponible

# Esquemas para Pasajero
class PasajeroBase(BaseModel):
    nombre_completo: str
    documento_identidad: Optional[str] = None

class PasajeroCreate(PasajeroBase):
    id_asiento: int

class PasajeroResponse(BaseModel):
    id: int
    id_reserva: int
    id_asiento: int
    nombre_completo: str
    documento_identidad: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

# Schema con información del asiento
class PasajeroDetail(PasajeroResponse):
    asiento: Optional[dict] = None
    
    model_config = ConfigDict(from_attributes=True)
