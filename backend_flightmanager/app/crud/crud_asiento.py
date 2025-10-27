from sqlalchemy.orm import Session, joinedload
from app.database import Asiento, Vuelo, EstadoAsientoEnum, CategoriaAsientosEnum
from typing import List, Optional
from decimal import Decimal

# --- READ ---

def get_asiento_by_id(db: Session, asiento_id: int) -> Optional[Asiento]:
    """Obtiene un asiento por su ID."""
    return db.query(Asiento)\
        .options(joinedload(Asiento.vuelo))\
        .filter(Asiento.id == asiento_id)\
        .first()

def get_asientos_by_vuelo(db: Session, vuelo_id: int) -> List[Asiento]:
    """Obtiene todos los asientos de un vuelo."""
    return db.query(Asiento)\
        .filter(Asiento.id_vuelo == vuelo_id)\
        .order_by(Asiento.numero_asiento)\
        .all()

def get_available_seats(db: Session, vuelo_id: int) -> List[Asiento]:
    """Obtiene solo los asientos disponibles de un vuelo."""
    return db.query(Asiento)\
        .filter(Asiento.id_vuelo == vuelo_id)\
        .filter(Asiento.estado == EstadoAsientoEnum.Disponible)\
        .order_by(Asiento.numero_asiento)\
        .all()

def get_seats_by_category(db: Session, vuelo_id: int, categoria: CategoriaAsientosEnum) -> List[Asiento]:
    """Obtiene asientos disponibles por categoría."""
    return db.query(Asiento)\
        .filter(Asiento.id_vuelo == vuelo_id)\
        .filter(Asiento.categoria == categoria)\
        .filter(Asiento.estado == EstadoAsientoEnum.Disponible)\
        .order_by(Asiento.numero_asiento)\
        .all()

def get_seat_by_number(db: Session, vuelo_id: int, numero_asiento: str) -> Optional[Asiento]:
    """Obtiene un asiento específico por número."""
    return db.query(Asiento)\
        .filter(Asiento.id_vuelo == vuelo_id)\
        .filter(Asiento.numero_asiento == numero_asiento)\
        .first()

# --- CREAR ---

def create_asiento(db: Session, asiento_data: dict) -> Asiento:
    """
    Crea un nuevo asiento.
    asiento_data debe contener: id_vuelo, numero_asiento, categoria, precio_adicional
    """
    db_asiento = Asiento(**asiento_data)
    db.add(db_asiento)
    db.commit()
    db.refresh(db_asiento)
    return db_asiento

def create_asientos_bulk(db: Session, asientos_data: List[dict]) -> List[Asiento]:
    """Crea múltiples asientos a la vez (útil al crear un vuelo)."""
    asientos = [Asiento(**data) for data in asientos_data]
    db.add_all(asientos)
    db.commit()
    for asiento in asientos:
        db.refresh(asiento)
    return asientos

# --- ACTUALIZAR ---

def reserve_seat(db: Session, asiento_id: int) -> Optional[Asiento]:
    """
    Marca un asiento como Reservado.
    Retorna None si el asiento no existe o no está disponible.
    """
    asiento = get_asiento_by_id(db, asiento_id)
    if not asiento:
        return None
    
    if asiento.estado != EstadoAsientoEnum.Disponible:
        return None  # No se puede reservar si no está disponible
    
    asiento.estado = EstadoAsientoEnum.Reservado
    db.commit()
    db.refresh(asiento)
    return asiento

def occupy_seat(db: Session, asiento_id: int) -> Optional[Asiento]:
    """
    Marca un asiento como Ocupado (tras confirmación de pago).
    """
    asiento = get_asiento_by_id(db, asiento_id)
    if not asiento:
        return None
    
    asiento.estado = EstadoAsientoEnum.Ocupado
    db.commit()
    db.refresh(asiento)
    return asiento

def release_seat(db: Session, asiento_id: int) -> Optional[Asiento]:
    """
    Libera un asiento (lo marca como Disponible).
    Útil cuando se cancela una reserva.
    """
    asiento = get_asiento_by_id(db, asiento_id)
    if not asiento:
        return None
    
    asiento.estado = EstadoAsientoEnum.Disponible
    db.commit()
    db.refresh(asiento)
    return asiento

def update_asiento_estado(db: Session, asiento_id: int, nuevo_estado: EstadoAsientoEnum) -> Optional[Asiento]:
    """Actualiza el estado de un asiento."""
    asiento = get_asiento_by_id(db, asiento_id)
    if not asiento:
        return None
    
    asiento.estado = nuevo_estado
    db.commit()
    db.refresh(asiento)
    return asiento

# --- DELETE ---

def delete_asiento(db: Session, asiento_id: int) -> bool:
    """Elimina un asiento."""
    asiento = get_asiento_by_id(db, asiento_id)
    if not asiento:
        return False
    
    db.delete(asiento)
    db.commit()
    return True

# --- VALIDACIONES Y UTILIDADES ---

def is_seat_available(db: Session, asiento_id: int) -> bool:
    """Verifica si un asiento está disponible."""
    asiento = get_asiento_by_id(db, asiento_id)
    return asiento is not None and asiento.estado == EstadoAsientoEnum.Disponible

def count_available_seats(db: Session, vuelo_id: int) -> int:
    """Cuenta los asientos disponibles de un vuelo."""
    return db.query(Asiento)\
        .filter(Asiento.id_vuelo == vuelo_id)\
        .filter(Asiento.estado == EstadoAsientoEnum.Disponible)\
        .count()

def count_seats_by_category(db: Session, vuelo_id: int, categoria: CategoriaAsientosEnum) -> int:
    """Cuenta asientos disponibles por categoría."""
    return db.query(Asiento)\
        .filter(Asiento.id_vuelo == vuelo_id)\
        .filter(Asiento.categoria == categoria)\
        .filter(Asiento.estado == EstadoAsientoEnum.Disponible)\
        .count()

def get_seat_price(db: Session, asiento_id: int, tarifa_base: Decimal) -> Decimal:
    """
    Calcula el precio total de un asiento (tarifa base + precio adicional).
    """
    asiento = get_asiento_by_id(db, asiento_id)
    if not asiento:
        return Decimal('0')
    
    return tarifa_base + asiento.precio_adicional

def seat_exists(db: Session, vuelo_id: int, numero_asiento: str) -> bool:
    """Verifica si un asiento existe en un vuelo."""
    return db.query(Asiento)\
        .filter(Asiento.id_vuelo == vuelo_id)\
        .filter(Asiento.numero_asiento == numero_asiento)\
        .first() is not None
