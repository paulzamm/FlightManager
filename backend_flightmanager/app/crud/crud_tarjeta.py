from sqlalchemy.orm import Session
from app.database import TarjetaCredito
from typing import List, Optional

# --- READ ---

def get_tarjeta_by_id(db: Session, tarjeta_id: int) -> Optional[TarjetaCredito]:
    """Obtiene una tarjeta por su ID."""
    return db.query(TarjetaCredito)\
        .filter(TarjetaCredito.id == tarjeta_id)\
        .first()

def get_tarjetas_by_user(db: Session, user_id: int) -> List[TarjetaCredito]:
    """Obtiene todas las tarjetas de un usuario."""
    return db.query(TarjetaCredito)\
        .filter(TarjetaCredito.id_usuario == user_id)\
        .order_by(TarjetaCredito.es_predeterminada.desc())\
        .all()

def get_default_tarjeta(db: Session, user_id: int) -> Optional[TarjetaCredito]:
    """Obtiene la tarjeta predeterminada de un usuario."""
    return db.query(TarjetaCredito)\
        .filter(TarjetaCredito.id_usuario == user_id)\
        .filter(TarjetaCredito.es_predeterminada == True)\
        .first()

# --- CREATE ---

def create_tarjeta(db: Session, user_id: int, numero_tarjeta: str, fecha_expiracion: str, nombre_titular: str, es_predeterminada: bool = False) -> TarjetaCredito:
    """
    Crea una nueva tarjeta de crédito.
    
    IMPORTANTE: En producción, numero_tarjeta debe ser tokenizado
    antes de guardarse en la BD.
    """
    # Si es la primera tarjeta, hacerla predeterminada automáticamente
    tarjetas_existentes = get_tarjetas_by_user(db, user_id)
    if not tarjetas_existentes:
        es_predeterminada = True
    
    # Si se marca como predeterminada, desmarcar las demás
    if es_predeterminada:
        _unset_default_tarjetas(db, user_id)
    
    db_tarjeta = TarjetaCredito(
        id_usuario=user_id,
        numero_tarjeta=numero_tarjeta,
        fecha_expiracion=fecha_expiracion,
        nombre_titular=nombre_titular,
        es_predeterminada=es_predeterminada
    )
    db.add(db_tarjeta)
    db.commit()
    db.refresh(db_tarjeta)
    return db_tarjeta

# --- UPDATE ---

def set_default_tarjeta(db: Session, tarjeta_id: int, user_id: int) -> Optional[TarjetaCredito]:
    """Marca una tarjeta como predeterminada."""
    tarjeta = get_tarjeta_by_id(db, tarjeta_id)
    if not tarjeta or tarjeta.id_usuario != user_id:
        return None
    
    # Desmarcar otras tarjetas del usuario
    _unset_default_tarjetas(db, user_id)
    
    # Marcar esta como predeterminada
    tarjeta.es_predeterminada = True
    db.commit()
    db.refresh(tarjeta)
    return tarjeta

def update_tarjeta(db: Session, tarjeta_id: int, tarjeta_data: dict) -> Optional[TarjetaCredito]:
    """Actualiza los datos de una tarjeta."""
    tarjeta = get_tarjeta_by_id(db, tarjeta_id)
    if not tarjeta:
        return None
    
    # Convertir Pydantic model a dict si es necesario
    if not isinstance(tarjeta_data, dict):
        tarjeta_data = tarjeta_data.model_dump(exclude_unset=True)
    
    # Si se cambia a predeterminada, desmarcar las demás
    if tarjeta_data.get('es_predeterminada') == True:
        _unset_default_tarjetas(db, tarjeta.id_usuario)
    
    for key, value in tarjeta_data.items():
        if hasattr(tarjeta, key) and value is not None:
            setattr(tarjeta, key, value)
    
    db.commit()
    db.refresh(tarjeta)
    return tarjeta

# --- DELETE ---

def delete_tarjeta(db: Session, tarjeta_id: int, user_id: int) -> bool:
    """
    Elimina una tarjeta.
    Si era la predeterminada, marca otra como predeterminada.
    """
    tarjeta = get_tarjeta_by_id(db, tarjeta_id)
    if not tarjeta or tarjeta.id_usuario != user_id:
        return False
    
    era_predeterminada = tarjeta.es_predeterminada
    
    # Eliminar tarjeta
    db.delete(tarjeta)
    db.commit()
    
    # Si era predeterminada, marcar otra como predeterminada
    if era_predeterminada:
        tarjetas_restantes = get_tarjetas_by_user(db, user_id)
        if tarjetas_restantes:
            tarjetas_restantes[0].es_predeterminada = True
            db.commit()
    
    return True

# --- VALIDACIONES Y UTILIDADES ---

def tarjeta_exists(db: Session, tarjeta_id: int) -> bool:
    """Verifica si una tarjeta existe."""
    return db.query(TarjetaCredito)\
        .filter(TarjetaCredito.id == tarjeta_id)\
        .first() is not None

def user_has_tarjeta(db: Session, user_id: int, tarjeta_id: int) -> bool:
    """Verifica si una tarjeta pertenece a un usuario."""
    tarjeta = get_tarjeta_by_id(db, tarjeta_id)
    return tarjeta is not None and tarjeta.id_usuario == user_id

def count_tarjetas_by_user(db: Session, user_id: int) -> int:
    """Cuenta las tarjetas de un usuario."""
    return db.query(TarjetaCredito)\
        .filter(TarjetaCredito.id_usuario == user_id)\
        .count()

def get_tarjeta_segura(db: Session, tarjeta_id: int) -> Optional[dict]:
    """
    Retorna los datos de la tarjeta de forma segura (ocultando número completo).
    Solo muestra los últimos 4 dígitos.
    """
    tarjeta = get_tarjeta_by_id(db, tarjeta_id)
    if not tarjeta:
        return None
    
    return {
        "id": tarjeta.id,
        "ultimos_4_digitos": tarjeta.numero_tarjeta[-4:],
        "fecha_expiracion": tarjeta.fecha_expiracion,
        "nombre_titular": tarjeta.nombre_titular,
        "es_predeterminada": tarjeta.es_predeterminada
    }

# --- FUNCIONES PRIVADAS ---

def _unset_default_tarjetas(db: Session, user_id: int):
    """Desmarca todas las tarjetas predeterminadas de un usuario."""
    db.query(TarjetaCredito)\
        .filter(TarjetaCredito.id_usuario == user_id)\
        .filter(TarjetaCredito.es_predeterminada == True)\
        .update({"es_predeterminada": False})
    db.commit()
