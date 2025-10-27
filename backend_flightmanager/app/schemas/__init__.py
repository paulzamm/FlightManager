# Schemas para facilitar las importaciones
from .user import User, UserBase, UserCreate, UserUpdate
from .token import Token, TokenData
from .flight import (
    Aeropuerto, AeropuertoBase,
    Aerolinea, AerolineaBase,
    FlightResult
)
from .asiento import (
    Asiento, AsientoBase, AsientoCreate, 
    AsientoUpdate, AsientoDisponible
)
from .pasajero import (
    Pasajero, PasajeroBase, PasajeroCreate,
    PasajeroConAsiento
)
from .reserva import (
    Reserva, ReservaBase, ReservaCreate,
    ReservaUpdate, ReservaCompleta, ReservaListado
)
from .tarjeta import (
    TarjetaCredito, TarjetaCreditoBase, TarjetaCreditoCreate,
    TarjetaCreditoUpdate, TarjetaCreditoSegura
)
from .billete import (
    Billete, BilleteBase, BilleteCreate,
    BilleteCompleto, BilleteConfirmacion
)

__all__ = [
    # User
    "User", "UserBase", "UserCreate", "UserUpdate",
    # Token
    "Token", "TokenData",
    # Flight
    "Aeropuerto", "AeropuertoBase",
    "Aerolinea", "AerolineaBase",
    "FlightResult",
    # Asiento
    "Asiento", "AsientoBase", "AsientoCreate",
    "AsientoUpdate", "AsientoDisponible",
    # Pasajero
    "Pasajero", "PasajeroBase", "PasajeroCreate",
    "PasajeroConAsiento",
    # Reserva
    "Reserva", "ReservaBase", "ReservaCreate",
    "ReservaUpdate", "ReservaCompleta", "ReservaListado",
    # Tarjeta
    "TarjetaCredito", "TarjetaCreditoBase", "TarjetaCreditoCreate",
    "TarjetaCreditoUpdate", "TarjetaCreditoSegura",
    # Billete
    "Billete", "BilleteBase", "BilleteCreate",
    "BilleteCompleto", "BilleteConfirmacion",
]
