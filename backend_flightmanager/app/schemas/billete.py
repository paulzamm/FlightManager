from pydantic import BaseModel, ConfigDict
from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .reserva import ReservaCompleta
    from .tarjeta import TarjetaCreditoSegura

# Esquemas para Billete
class BilleteBase(BaseModel):
    codigo_confirmacion: str

class BilleteCreate(BaseModel):
    id_reserva: int
    id_tarjeta_credito: int
    codigo_confirmacion: str

class Billete(BilleteBase):
    id: int
    id_reserva: int
    id_tarjeta_credito: int
    fecha_compra: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Schema completo con información de reserva y tarjeta
class BilleteCompleto(Billete):
    reserva: Optional['ReservaCompleta'] = None
    tarjeta_credito: Optional['TarjetaCreditoSegura'] = None
    
    model_config = ConfigDict(from_attributes=True)

# Schema para confirmación de compra
class BilleteConfirmacion(BaseModel):
    id: int
    codigo_confirmacion: str
    fecha_compra: datetime
    monto_total: float
    mensaje: str = "Compra realizada exitosamente"
    
    model_config = ConfigDict(from_attributes=True)
