# Schemas para facilitar las importaciones
from .user import User, UserBase, UserCreate, UserUpdate, UserProfile, PasswordChange, AccountDeletion
from .token import Token, TokenData
from .flight import (
    Aeropuerto, AeropuertoBase,
    Aerolinea, AerolineaBase,
    FlightResult
)
from .asiento import (
    AsientoBase, AsientoCreate, 
    AsientoUpdate, AsientoDisponible, AsientoResponse
)
from .pasajero import (
    PasajeroBase, PasajeroCreate,
    PasajeroResponse, PasajeroDetail
)
from .reserva import (
    ReservaBase, ReservaCreate,
    ReservaUpdate, ReservaResponse, ReservaDetail, ReservaSummary
)
from .tarjeta import (
    TarjetaBase, TarjetaCreate,
    TarjetaUpdate, TarjetaResponse, TarjetaSegura
)
from .billete import (
    BilleteBase, BilleteCreate,
    BilleteResponse, BilleteDetail, BilleteConfirmacion
)

__all__ = [
    # User
    "User", "UserBase", "UserCreate", "UserUpdate", "UserProfile", "PasswordChange", "AccountDeletion",
    # Token
    "Token", "TokenData",
    # Flight
    "Aeropuerto", "AeropuertoBase",
    "Aerolinea", "AerolineaBase",
    "FlightResult",
    # Asiento
    "AsientoBase", "AsientoCreate",
    "AsientoUpdate", "AsientoDisponible", "AsientoResponse",
    # Pasajero
    "PasajeroBase", "PasajeroCreate",
    "PasajeroResponse", "PasajeroDetail",
    # Reserva
    "ReservaBase", "ReservaCreate",
    "ReservaUpdate", "ReservaResponse", "ReservaDetail", "ReservaSummary",
    # Tarjeta
    "TarjetaBase", "TarjetaCreate",
    "TarjetaUpdate", "TarjetaResponse", "TarjetaSegura",
    # Billete
    "BilleteBase", "BilleteCreate",
    "BilleteResponse", "BilleteDetail", "BilleteConfirmacion",
]
