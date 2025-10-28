from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

# Esquemas para Aeropuertos
class AeropuertoBase(BaseModel):
    codigo_iata: str
    nombre: str
    ciudad: str
    pais: str

class Aeropuerto(AeropuertoBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

# Esquemas para Aerolíneas
class AerolineaBase(BaseModel):
    nombre: str
    codigo_iata: str

class Aerolinea(AerolineaBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

# Esquema para el resultado de una búsqueda de vuelo
class FlightResult(BaseModel):
    id: int
    numero_vuelo: str
    hora_salida: datetime
    hora_llegada: datetime
    tarifa_base: float
    estado: str  # Estado del vuelo: Programado, EnHora, Retrasado, Cancelado
    aerolinea: Aerolinea
    origen: Aeropuerto
    destino: Aeropuerto

    model_config = ConfigDict(from_attributes=True)
