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

class Pasajero(PasajeroBase):
    id: int
    id_reserva: int
    id_asiento: int
    
    model_config = ConfigDict(from_attributes=True)

# Schema con información del asiento
class PasajeroConAsiento(Pasajero):
    asiento: Optional['AsientoDisponible'] = None
    
    model_config = ConfigDict(from_attributes=True)
