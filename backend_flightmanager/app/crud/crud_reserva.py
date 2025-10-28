from sqlalchemy.orm import Session, joinedload
from app.database import Reserva, Pasajero, Asiento, EstadoReservaEnum
from typing import List, Optional
from decimal import Decimal
from datetime import datetime

# --- READ ---

def get_reserva_by_id(db: Session, reserva_id: int) -> Optional[Reserva]:
    """Obtiene una reserva por su ID con todas las relaciones."""
    return db.query(Reserva)\
        .options(
            joinedload(Reserva.usuario),
            joinedload(Reserva.pasajeros).joinedload(Pasajero.asiento),
            joinedload(Reserva.billete)
        )\
        .filter(Reserva.id == reserva_id)\
        .first()

def get_reservas_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Reserva]:
    """Obtiene todas las reservas de un usuario."""
    return db.query(Reserva)\
        .options(
            joinedload(Reserva.pasajeros).joinedload(Pasajero.asiento)
        )\
        .filter(Reserva.id_usuario == user_id)\
        .order_by(Reserva.fecha_reserva.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()

def get_reservas_by_estado(db: Session, user_id: int, estado: EstadoReservaEnum, skip: int = 0, limit: int = 100) -> List[Reserva]:
    """Obtiene reservas filtradas por estado para un usuario específico."""
    return db.query(Reserva)\
        .options(joinedload(Reserva.pasajeros).joinedload(Pasajero.asiento))\
        .filter(Reserva.id_usuario == user_id)\
        .filter(Reserva.estado == estado)\
        .order_by(Reserva.fecha_reserva.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()

def get_pending_reservas(db: Session, user_id: int) -> List[Reserva]:
    """Obtiene reservas pendientes de pago de un usuario."""
    return db.query(Reserva)\
        .filter(Reserva.id_usuario == user_id)\
        .filter(Reserva.estado == EstadoReservaEnum.Pendiente)\
        .order_by(Reserva.fecha_reserva.desc())\
        .all()

# --- CREATE ---

def create_reserva(db: Session, user_id: int, monto_total: Decimal, pasajeros_data: Optional[List[dict]] = None) -> Reserva:
    """
    Crea una nueva reserva.
    pasajeros_data (opcional): lista de dicts con {nombre_completo, documento_identidad, id_asiento}
    """
    db_reserva = Reserva(
        id_usuario=user_id,
        monto_total=monto_total,
        estado=EstadoReservaEnum.Pendiente
    )
    db.add(db_reserva)
    db.commit()
    db.refresh(db_reserva)
    
    # Si se proporcionan pasajeros, agregarlos
    if pasajeros_data:
        from app.crud.crud_pasajero import create_pasajero
        for pasajero_data in pasajeros_data:
            pasajero_data['id_reserva'] = db_reserva.id
            create_pasajero(db, pasajero_data)
        
        # Recargar la reserva con los pasajeros
        db.refresh(db_reserva)
    
    return db_reserva

# --- UPDATE ---

def update_reserva_estado(db: Session, reserva_id: int, nuevo_estado: EstadoReservaEnum) -> Optional[Reserva]:
    """Actualiza el estado de una reserva."""
    reserva = get_reserva_by_id(db, reserva_id)
    if not reserva:
        return None
    
    reserva.estado = nuevo_estado
    db.commit()
    db.refresh(reserva)
    return reserva

def confirm_reserva(db: Session, reserva_id: int) -> Optional[Reserva]:
    """
    Confirma una reserva (tras pago exitoso).
    Cambia el estado a Confirmada y marca los asientos como Ocupados.
    """
    from app.crud.crud_asiento import occupy_seat
    
    reserva = get_reserva_by_id(db, reserva_id)
    if not reserva:
        return None
    
    # Cambiar estado de la reserva
    reserva.estado = EstadoReservaEnum.Confirmada
    
    # Marcar todos los asientos como ocupados
    for pasajero in reserva.pasajeros:
        occupy_seat(db, pasajero.id_asiento)
    
    db.commit()
    db.refresh(reserva)
    return reserva

def cancel_reserva(db: Session, reserva_id: int) -> Optional[Reserva]:
    """
    Cancela una reserva.
    Libera los asientos asociados.
    """
    from app.crud.crud_asiento import release_seat
    
    reserva = get_reserva_by_id(db, reserva_id)
    if not reserva:
        return None
    
    # Cambiar estado de la reserva
    reserva.estado = EstadoReservaEnum.Cancelada
    
    # Liberar todos los asientos
    for pasajero in reserva.pasajeros:
        release_seat(db, pasajero.id_asiento)
    
    db.commit()
    db.refresh(reserva)
    return reserva

def update_reserva_monto(db: Session, reserva_id: int, nuevo_monto: Decimal) -> Optional[Reserva]:
    """Actualiza el monto total de una reserva."""
    reserva = get_reserva_by_id(db, reserva_id)
    if not reserva:
        return None
    
    reserva.monto_total = nuevo_monto
    db.commit()
    db.refresh(reserva)
    return reserva

# --- DELETE ---

def delete_reserva(db: Session, reserva_id: int) -> bool:
    """
    Elimina una reserva.
    Libera los asientos antes de eliminar.
    """
    reserva = get_reserva_by_id(db, reserva_id)
    if not reserva:
        return False
    
    # Liberar asientos primero
    cancel_reserva(db, reserva_id)
    
    # Eliminar reserva
    db.delete(reserva)
    db.commit()
    return True

# --- VALIDACIONES Y UTILIDADES ---

def calculate_total(db: Session, asientos_ids: List[int], tarifa_base: Decimal) -> Decimal:
    """
    Calcula el monto total de una reserva.
    tarifa_base: precio base del vuelo
    asientos_ids: lista de IDs de asientos seleccionados
    """
    from app.crud.crud_asiento import get_asiento_by_id
    
    total = Decimal('0')
    for asiento_id in asientos_ids:
        asiento = get_asiento_by_id(db, asiento_id)
        if asiento:
            total += tarifa_base + asiento.precio_adicional
    
    return total

def reserva_exists(db: Session, reserva_id: int) -> bool:
    """Verifica si una reserva existe."""
    return db.query(Reserva).filter(Reserva.id == reserva_id).first() is not None

def is_reserva_cancelable(db: Session, reserva_id: int) -> bool:
    """
    Verifica si una reserva puede ser cancelada.
    Solo se pueden cancelar reservas Pendientes o Confirmadas.
    """
    reserva = get_reserva_by_id(db, reserva_id)
    if not reserva:
        return False
    
    return reserva.estado in [EstadoReservaEnum.Pendiente, EstadoReservaEnum.Confirmada]

def count_reservas_by_user(db: Session, user_id: int) -> int:
    """Cuenta el total de reservas de un usuario."""
    return db.query(Reserva)\
        .filter(Reserva.id_usuario == user_id)\
        .count()

def get_reserva_summary(db: Session, reserva_id: int) -> Optional[dict]:
    """
    Obtiene un resumen de la reserva con información útil.
    """
    reserva = get_reserva_by_id(db, reserva_id)
    if not reserva:
        return None
    
    return {
        "id": reserva.id,
        "fecha_reserva": reserva.fecha_reserva,
        "estado": reserva.estado.value,
        "monto_total": float(reserva.monto_total),
        "cantidad_pasajeros": len(reserva.pasajeros),
        "usuario": {
            "id": reserva.usuario.id,
            "nombre": reserva.usuario.nombre_completo,
            "email": reserva.usuario.email
        },
        "pasajeros": [
            {
                "nombre": p.nombre_completo,
                "asiento": p.asiento.numero_asiento if p.asiento else None
            }
            for p in reserva.pasajeros
        ]
    }
