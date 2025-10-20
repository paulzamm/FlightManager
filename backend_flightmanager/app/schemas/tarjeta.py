from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
import re

# Esquemas para TarjetaCredito
class TarjetaCreditoBase(BaseModel):
    numero_tarjeta: str  # En producción debe ser tokenizado
    fecha_expiracion: str  # Formato: MM/YY
    nombre_titular: str
    es_predeterminada: bool = False
    
    @field_validator('fecha_expiracion')
    @classmethod
    def validar_fecha_expiracion(cls, v: str) -> str:
        # Validar formato MM/YY
        if not re.match(r'^\d{2}/\d{2}$', v):
            raise ValueError('Formato debe ser MM/YY')
        return v
    
    @field_validator('numero_tarjeta')
    @classmethod
    def validar_numero_tarjeta(cls, v: str) -> str:
        # Eliminar espacios y validar solo números
        numero = v.replace(' ', '').replace('-', '')
        if not numero.isdigit() or len(numero) < 13 or len(numero) > 19:
            raise ValueError('Número de tarjeta inválido')
        return numero

class TarjetaCreditoCreate(TarjetaCreditoBase):
    id_usuario: int

class TarjetaCreditoUpdate(BaseModel):
    es_predeterminada: Optional[bool] = None
    
class TarjetaCredito(BaseModel):
    id: int
    id_usuario: int
    numero_tarjeta: str
    fecha_expiracion: str
    nombre_titular: str
    es_predeterminada: bool
    
    model_config = ConfigDict(from_attributes=True)

# Schema seguro que oculta el número completo
class TarjetaCreditoSegura(BaseModel):
    id: int
    ultimos_4_digitos: str
    fecha_expiracion: str
    nombre_titular: str
    es_predeterminada: bool
    
    @classmethod
    def from_tarjeta(cls, tarjeta: TarjetaCredito):
        return cls(
            id=tarjeta.id,
            ultimos_4_digitos=tarjeta.numero_tarjeta[-4:],
            fecha_expiracion=tarjeta.fecha_expiracion,
            nombre_titular=tarjeta.nombre_titular,
            es_predeterminada=tarjeta.es_predeterminada
        )
