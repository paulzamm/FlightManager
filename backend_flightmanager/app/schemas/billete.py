from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal

# Esquemas para Billete
class BilleteBase(BaseModel):
    codigo_confirmacion: str

class BilleteCreate(BaseModel):
    id_reserva: int
    id_tarjeta: int  # Cambiado de id_tarjeta_credito a id_tarjeta

class BilleteResponse(BaseModel):
    id: int
    id_reserva: int
    id_tarjeta_credito: int
    codigo_confirmacion: str
    fecha_compra: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Schema con detalles completos
class BilleteDetail(BilleteResponse):
    reserva: Optional[dict] = None  # Incluye info de reserva
    pasajeros: Optional[list] = None
    
    model_config = ConfigDict(from_attributes=True)

# Schema para confirmación de compra
class BilleteConfirmacion(BaseModel):
    id: int
    codigo_confirmacion: str
    fecha_compra: datetime
    monto_total: Decimal
    mensaje: str = "Compra realizada exitosamente"
    
    model_config = ConfigDict(from_attributes=True)
