from sqlalchemy import Column, Integer, String, VARCHAR, TIMESTAMP, ForeignKey, DECIMAL, Boolean, Enum, text
from sqlalchemy.orm import relationship
from .database import Base
import enum

# Enum para tipos de estados y categorias
class CategoriaAsientosEnum(str, enum.Enum):
    Economica = 'Economica'
    Business = 'Business'
    PrimeraClase = 'PrimeraClase'

class EstadoVueloEnum(str, enum.Enum):
    Programado = 'Programado'
    EnHora = 'EnHora'
    Retrasado = 'Retrasado'
    Cancelado = 'Cancelado'

class EstadoReservaEnum(str, enum.Enum):
    Pendiente = 'Pendiente'
    Confirmada = 'Confirmada'
    Cancelada = 'Cancelada'

class EstadoAsientoEnum(str, enum.Enum):
    Disponible = 'Disponible'
    Reservado = 'Reservado'
    Ocupado = 'Ocupado'

# 1. Modelo de Usuario
class Usuario(Base):
    __tablename__ = "Usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(VARCHAR(100), nullable=False)
    email = Column(VARCHAR(100), unique=True, index=True, nullable=False)
    password_hash = Column(VARCHAR(255), nullable=False)
    fecha_creacion = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    
    # Relaciones
    reservas = relationship("Reserva", back_populates="usuario")
    tarjetas = relationship("TarjetaCredito", back_populates="usuario")

# 2. Modelo de Vuelo
class Vuelo(Base):
    __tablename__ = "Vuelos"
    
    id = Column(Integer, primary_key=True, index=True)
    numero_vuelo = Column(VARCHAR(10), nullable=False)
    hora_salida = Column(TIMESTAMP, nullable=False)
    hora_llegada = Column(TIMESTAMP, nullable=False)
    tarifa_base = Column(DECIMAL(10, 2), nullable=False)
    estado = Column(Enum(EstadoVueloEnum), default=EstadoVueloEnum.Programado)
    
    id_aerolinea = Column(Integer, ForeignKey("Aerolineas.id"))
    id_aeropuerto_origen = Column(Integer, ForeignKey("Aeropuertos.id"))
    id_aeropuerto_destino = Column(Integer, ForeignKey("Aeropuertos.id"))

    # Relaciones
    aerolinea = relationship("Aerolinea")
    origen = relationship("Aeropuerto", foreign_keys=[id_aeropuerto_origen])
    destino = relationship("Aeropuerto", foreign_keys=[id_aeropuerto_destino])
    asientos = relationship("Asiento", back_populates="vuelo")

# 3. Modelo de Aeropuerto
class Aeropuerto(Base):
    __tablename__ = "Aeropuertos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(VARCHAR(100), nullable=False)
    codigo_iata = Column(VARCHAR(3), unique=True, index=True)
    ciudad = Column(VARCHAR(100), nullable=False)
    pais = Column(VARCHAR(100), nullable=False)

# 4. Modelo de Aerolinea
class Aerolinea(Base):
    __tablename__ = "Aerolineas"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(VARCHAR(100), unique=True, nullable=False)
    codigo_iata = Column(VARCHAR(3), unique=True, index=True)

# 5. Modelo de TarjetaCredito
class TarjetaCredito(Base):
    __tablename__ = "TarjetasCredito"
    
    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("Usuarios.id", ondelete="CASCADE"), nullable=False)
    numero_tarjeta = Column(VARCHAR(50), nullable=False)  # En producción debe ser tokenizado
    fecha_expiracion = Column(VARCHAR(10), nullable=False)
    nombre_titular = Column(VARCHAR(100), nullable=False)
    es_predeterminada = Column(Boolean, default=False)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="tarjetas")
    billetes = relationship("Billete", back_populates="tarjeta_credito")

# 6. Modelo de Asiento
class Asiento(Base):
    __tablename__ = "Asientos"
    
    id = Column(Integer, primary_key=True, index=True)
    id_vuelo = Column(Integer, ForeignKey("Vuelos.id", ondelete="CASCADE"), nullable=False)
    numero_asiento = Column(VARCHAR(5), nullable=False)  # Ej. "A1", "22F"
    categoria = Column(Enum(CategoriaAsientosEnum), nullable=False)
    estado = Column(Enum(EstadoAsientoEnum), default=EstadoAsientoEnum.Disponible)
    precio_adicional = Column(DECIMAL(10, 2), default=0)
    
    # Relaciones
    vuelo = relationship("Vuelo", back_populates="asientos")
    pasajeros = relationship("Pasajero", back_populates="asiento")

# 7. Modelo de Reserva
class Reserva(Base):
    __tablename__ = "Reservas"
    
    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("Usuarios.id"), nullable=False)
    fecha_reserva = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    estado = Column(Enum(EstadoReservaEnum), default=EstadoReservaEnum.Pendiente)
    monto_total = Column(DECIMAL(10, 2), nullable=False)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="reservas")
    pasajeros = relationship("Pasajero", back_populates="reserva", cascade="all, delete-orphan")
    billete = relationship("Billete", back_populates="reserva", uselist=False)

# 8. Modelo de Pasajero
class Pasajero(Base):
    __tablename__ = "Pasajeros"
    
    id = Column(Integer, primary_key=True, index=True)
    id_reserva = Column(Integer, ForeignKey("Reservas.id", ondelete="CASCADE"), nullable=False)
    id_asiento = Column(Integer, ForeignKey("Asientos.id"), nullable=False)
    nombre_completo = Column(VARCHAR(100), nullable=False)
    documento_identidad = Column(VARCHAR(50))  # Ej. Pasaporte
    
    # Relaciones
    reserva = relationship("Reserva", back_populates="pasajeros")
    asiento = relationship("Asiento", back_populates="pasajeros")

# 9. Modelo de Billete
class Billete(Base):
    __tablename__ = "Billetes"
    
    id = Column(Integer, primary_key=True, index=True)
    id_reserva = Column(Integer, ForeignKey("Reservas.id"), unique=True, nullable=False)
    id_tarjeta_credito = Column(Integer, ForeignKey("TarjetasCredito.id"), nullable=False)
    fecha_compra = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    codigo_confirmacion = Column(VARCHAR(20), unique=True, nullable=False)
    
    # Relaciones
    reserva = relationship("Reserva", back_populates="billete")
    tarjeta_credito = relationship("TarjetaCredito", back_populates="billetes")