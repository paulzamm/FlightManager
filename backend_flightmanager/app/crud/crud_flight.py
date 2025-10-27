from sqlalchemy.orm import Session, joinedload, aliased
from sqlalchemy.sql.expression import func
from app.database import Vuelo, Aeropuerto, Aerolinea, Asiento, EstadoVueloEnum, EstadoAsientoEnum
from datetime import date, datetime
from typing import List, Optional

# --- BÚSQUEDA Y CONSULTAS ---

def search_flights(db: Session, origen_iata: str, destino_iata: str, fecha: date) -> List[Vuelo]:
    """
    Busca vuelos basados en código IATA de origen, destino y fecha.
    Carga las relaciones de aerolínea, aeropuertos origen y destino.
    """
    # Crear alias para distinguir entre aeropuerto origen y destino
    AeropuertoOrigen = aliased(Aeropuerto)
    AeropuertoDestino = aliased(Aeropuerto)
    
    return db.query(Vuelo)\
        .join(AeropuertoOrigen, Vuelo.id_aeropuerto_origen == AeropuertoOrigen.id)\
        .join(AeropuertoDestino, Vuelo.id_aeropuerto_destino == AeropuertoDestino.id)\
        .join(Aerolinea, Vuelo.id_aerolinea == Aerolinea.id)\
        .options(
            joinedload(Vuelo.origen),
            joinedload(Vuelo.destino),
            joinedload(Vuelo.aerolinea)
        )\
        .filter(AeropuertoOrigen.codigo_iata == origen_iata)\
        .filter(AeropuertoDestino.codigo_iata == destino_iata)\
        .filter(func.date(Vuelo.hora_salida) == fecha)\
        .filter(Vuelo.estado != EstadoVueloEnum.Cancelado)\
        .order_by(Vuelo.hora_salida)\
        .all()

def get_flight_by_id(db: Session, flight_id: int) -> Optional[Vuelo]:
    """Obtiene un vuelo por su ID con todas las relaciones cargadas."""
    return db.query(Vuelo)\
        .options(
            joinedload(Vuelo.origen),
            joinedload(Vuelo.destino),
            joinedload(Vuelo.aerolinea),
            joinedload(Vuelo.asientos)
        )\
        .filter(Vuelo.id == flight_id)\
        .first()

def get_flight_by_number(db: Session, numero_vuelo: str, fecha: date) -> Optional[Vuelo]:
    """Obtiene un vuelo por su número y fecha."""
    return db.query(Vuelo)\
        .options(
            joinedload(Vuelo.origen),
            joinedload(Vuelo.destino),
            joinedload(Vuelo.aerolinea)
        )\
        .filter(Vuelo.numero_vuelo == numero_vuelo)\
        .filter(func.date(Vuelo.hora_salida) == fecha)\
        .first()

def get_flights(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    estado: Optional[EstadoVueloEnum] = None
) -> List[Vuelo]:
    """Lista vuelos con paginación y filtro opcional por estado."""
    query = db.query(Vuelo)\
        .options(
            joinedload(Vuelo.origen),
            joinedload(Vuelo.destino),
            joinedload(Vuelo.aerolinea)
        )
    
    if estado:
        query = query.filter(Vuelo.estado == estado)
    
    return query.order_by(Vuelo.hora_salida.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()

def get_available_seats(db: Session, flight_id: int) -> List[Asiento]:
    """Obtiene todos los asientos disponibles de un vuelo."""
    return db.query(Asiento)\
        .filter(Asiento.id_vuelo == flight_id)\
        .filter(Asiento.estado == EstadoAsientoEnum.Disponible)\
        .order_by(Asiento.numero_asiento)\
        .all()

def get_seats_by_category(db: Session, flight_id: int, categoria: str) -> List[Asiento]:
    """Obtiene asientos disponibles de un vuelo por categoría."""
    from app.database import CategoriaAsientosEnum
    
    return db.query(Asiento)\
        .filter(Asiento.id_vuelo == flight_id)\
        .filter(Asiento.categoria == categoria)\
        .filter(Asiento.estado == EstadoAsientoEnum.Disponible)\
        .order_by(Asiento.numero_asiento)\
        .all()

def count_available_seats(db: Session, flight_id: int) -> int:
    """Cuenta los asientos disponibles de un vuelo."""
    return db.query(Asiento)\
        .filter(Asiento.id_vuelo == flight_id)\
        .filter(Asiento.estado == EstadoAsientoEnum.Disponible)\
        .count()

# --- CREAR ---

def create_flight(db: Session, flight_data: dict) -> Vuelo:
    """
    Crea un nuevo vuelo.
    flight_data debe contener: numero_vuelo, hora_salida, hora_llegada,
    tarifa_base, id_aerolinea, id_aeropuerto_origen, id_aeropuerto_destino
    """
    db_flight = Vuelo(**flight_data)
    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)
    return db_flight

# --- ACTUALIZAR ---

def update_flight_status(db: Session, flight_id: int, nuevo_estado: EstadoVueloEnum) -> Optional[Vuelo]:
    """Actualiza el estado de un vuelo (Programado, EnHora, Retrasado, Cancelado)."""
    db_flight = get_flight_by_id(db, flight_id)
    if not db_flight:
        return None
    
    db_flight.estado = nuevo_estado
    db.commit()
    db.refresh(db_flight)
    return db_flight

def update_flight_times(db: Session, flight_id: int, hora_salida: Optional[datetime] = None, hora_llegada: Optional[datetime] = None) -> Optional[Vuelo]:
    """Actualiza las horas de salida y/o llegada de un vuelo."""
    db_flight = get_flight_by_id(db, flight_id)
    if not db_flight:
        return None
    
    if hora_salida:
        db_flight.hora_salida = hora_salida
    if hora_llegada:
        db_flight.hora_llegada = hora_llegada
    
    db.commit()
    db.refresh(db_flight)
    return db_flight

def update_flight(db: Session, flight_id: int, flight_data: dict) -> Optional[Vuelo]:
    """Actualiza un vuelo con datos parciales."""
    db_flight = get_flight_by_id(db, flight_id)
    if not db_flight:
        return None
    
    for key, value in flight_data.items():
        if hasattr(db_flight, key) and value is not None:
            setattr(db_flight, key, value)
    
    db.commit()
    db.refresh(db_flight)
    return db_flight

# --- ELIMINAR ---

def delete_flight(db: Session, flight_id: int) -> bool:
    """Elimina un vuelo de la BD."""
    db_flight = get_flight_by_id(db, flight_id)
    if not db_flight:
        return False
    
    db.delete(db_flight)
    db.commit()
    return True

# --- VALIDACIONES Y UTILIDADES ---

def flight_exists(db: Session, numero_vuelo: str, fecha: date) -> bool:
    """Verifica si un vuelo existe por número y fecha."""
    return db.query(Vuelo)\
        .filter(Vuelo.numero_vuelo == numero_vuelo)\
        .filter(func.date(Vuelo.hora_salida) == fecha)\
        .first() is not None

def is_flight_bookable(db: Session, flight_id: int) -> bool:
    """
    Verifica si un vuelo se puede reservar.
    Criterios: No cancelado y tiene asientos disponibles.
    """
    flight = get_flight_by_id(db, flight_id)
    if not flight:
        return False
    
    if flight.estado == EstadoVueloEnum.Cancelado:
        return False
    
    available_seats = count_available_seats(db, flight_id)
    return available_seats > 0