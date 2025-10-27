from sqlalchemy.orm import Session, joinedload
from app.database import Pasajero, Asiento
from typing import List, Optional

# --- READ ---

def get_pasajero_by_id(db: Session, pasajero_id: int) -> Optional[Pasajero]:
    """Obtiene un pasajero por su ID."""
    return db.query(Pasajero)\
        .options(
            joinedload(Pasajero.asiento),
            joinedload(Pasajero.reserva)
        )\
        .filter(Pasajero.id == pasajero_id)\
        .first()

def get_pasajeros_by_reserva(db: Session, reserva_id: int) -> List[Pasajero]:
    """Obtiene todos los pasajeros de una reserva."""
    return db.query(Pasajero)\
        .options(joinedload(Pasajero.asiento))\
        .filter(Pasajero.id_reserva == reserva_id)\
        .all()

def get_pasajero_by_asiento(db: Session, asiento_id: int) -> Optional[Pasajero]:
    """Obtiene el pasajero asignado a un asiento."""
    return db.query(Pasajero)\
        .filter(Pasajero.id_asiento == asiento_id)\
        .first()

# --- CREATE ---

def create_pasajero(db: Session, pasajero_data: dict) -> Pasajero:
    """
    Crea un nuevo pasajero.
    pasajero_data debe contener: id_reserva, id_asiento, nombre_completo, documento_identidad (opcional)
    """
    # Reservar el asiento automáticamente
    from app.crud.crud_asiento import reserve_seat
    reserve_seat(db, pasajero_data['id_asiento'])
    
    db_pasajero = Pasajero(**pasajero_data)
    db.add(db_pasajero)
    db.commit()
    db.refresh(db_pasajero)
    return db_pasajero

def create_pasajeros_bulk(db: Session, pasajeros_data: List[dict]) -> List[Pasajero]:
    """Crea múltiples pasajeros a la vez."""
    pasajeros = []
    for data in pasajeros_data:
        pasajero = create_pasajero(db, data)
        pasajeros.append(pasajero)
    return pasajeros

# --- UPDATE ---

def update_pasajero(db: Session, pasajero_id: int, pasajero_data: dict) -> Optional[Pasajero]:
    """Actualiza los datos de un pasajero."""
    pasajero = get_pasajero_by_id(db, pasajero_id)
    if not pasajero:
        return None
    
    # Si se cambia el asiento, liberar el anterior y reservar el nuevo
    if 'id_asiento' in pasajero_data and pasajero_data['id_asiento'] != pasajero.id_asiento:
        from app.crud.crud_asiento import release_seat, reserve_seat
        
        # Liberar asiento anterior
        release_seat(db, pasajero.id_asiento)
        
        # Reservar nuevo asiento
        reserve_seat(db, pasajero_data['id_asiento'])
    
    # Actualizar datos
    for key, value in pasajero_data.items():
        if hasattr(pasajero, key) and value is not None:
            setattr(pasajero, key, value)
    
    db.commit()
    db.refresh(pasajero)
    return pasajero

def change_pasajero_asiento(db: Session, pasajero_id: int, nuevo_asiento_id: int) -> Optional[Pasajero]:
    """Cambia el asiento de un pasajero."""
    from app.crud.crud_asiento import release_seat, reserve_seat, is_seat_available
    
    pasajero = get_pasajero_by_id(db, pasajero_id)
    if not pasajero:
        return None
    
    # Verificar que el nuevo asiento esté disponible
    if not is_seat_available(db, nuevo_asiento_id):
        return None
    
    # Liberar asiento anterior
    release_seat(db, pasajero.id_asiento)
    
    # Reservar nuevo asiento
    reserve_seat(db, nuevo_asiento_id)
    
    # Actualizar pasajero
    pasajero.id_asiento = nuevo_asiento_id
    db.commit()
    db.refresh(pasajero)
    return pasajero

# --- DELETE ---

def delete_pasajero(db: Session, pasajero_id: int) -> bool:
    """Elimina un pasajero y libera su asiento."""
    from app.crud.crud_asiento import release_seat
    
    pasajero = get_pasajero_by_id(db, pasajero_id)
    if not pasajero:
        return False
    
    # Liberar el asiento
    release_seat(db, pasajero.id_asiento)
    
    # Eliminar pasajero
    db.delete(pasajero)
    db.commit()
    return True

# --- VALIDACIONES Y UTILIDADES ---

def pasajero_exists(db: Session, pasajero_id: int) -> bool:
    """Verifica si un pasajero existe."""
    return db.query(Pasajero).filter(Pasajero.id == pasajero_id).first() is not None

def count_pasajeros_by_reserva(db: Session, reserva_id: int) -> int:
    """Cuenta los pasajeros de una reserva."""
    return db.query(Pasajero)\
        .filter(Pasajero.id_reserva == reserva_id)\
        .count()

def validate_pasajero_data(pasajero_data: dict) -> bool:
    """Valida que los datos del pasajero sean correctos."""
    required_fields = ['id_reserva', 'id_asiento', 'nombre_completo']
    return all(field in pasajero_data for field in required_fields)
