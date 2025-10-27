from sqlalchemy.orm import Session, joinedload
from app.database import Billete, Reserva
from typing import List, Optional
import secrets
import string

# --- READ ---

def get_billete_by_id(db: Session, billete_id: int) -> Optional[Billete]:
    """Obtiene un billete por su ID con todas las relaciones."""
    return db.query(Billete)\
        .options(
            joinedload(Billete.reserva).joinedload(Reserva.pasajeros),
            joinedload(Billete.tarjeta_credito)
        )\
        .filter(Billete.id == billete_id)\
        .first()

def get_billete_by_codigo(db: Session, codigo_confirmacion: str) -> Optional[Billete]:
    """Obtiene un billete por su código de confirmación."""
    return db.query(Billete)\
        .options(
            joinedload(Billete.reserva).joinedload(Reserva.pasajeros),
            joinedload(Billete.tarjeta_credito)
        )\
        .filter(Billete.codigo_confirmacion == codigo_confirmacion)\
        .first()

def get_billete_by_reserva(db: Session, reserva_id: int) -> Optional[Billete]:
    """Obtiene el billete asociado a una reserva."""
    return db.query(Billete)\
        .filter(Billete.id_reserva == reserva_id)\
        .first()

def get_billetes_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Billete]:
    """Obtiene todos los billetes de un usuario."""
    return db.query(Billete)\
        .join(Reserva, Billete.id_reserva == Reserva.id)\
        .options(
            joinedload(Billete.reserva).joinedload(Reserva.pasajeros)
        )\
        .filter(Reserva.id_usuario == user_id)\
        .order_by(Billete.fecha_compra.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()

# --- CREATE ---

def create_billete(db: Session, reserva_id: int, tarjeta_credito_id: int) -> Billete:
    """
    Crea un billete tras una compra exitosa.
    Genera automáticamente el código de confirmación.
    """
    # Generar código de confirmación único
    codigo = generate_codigo_confirmacion(db)
    
    db_billete = Billete(
        id_reserva=reserva_id,
        id_tarjeta_credito=tarjeta_credito_id,
        codigo_confirmacion=codigo
    )
    db.add(db_billete)
    db.commit()
    db.refresh(db_billete)
    
    # Confirmar la reserva
    from app.crud.crud_reserva import confirm_reserva
    confirm_reserva(db, reserva_id)
    
    return db_billete

# --- UPDATE ---
# Los billetes generalmente no se actualizan, solo se crean

# --- DELETE ---
# Los billetes NO se deben eliminar por razones de auditoría
# Si se cancela un viaje, se cancela la reserva, no el billete

# --- VALIDACIONES Y UTILIDADES ---

def billete_exists(db: Session, billete_id: int) -> bool:
    """Verifica si un billete existe."""
    return db.query(Billete).filter(Billete.id == billete_id).first() is not None

def codigo_confirmacion_exists(db: Session, codigo: str) -> bool:
    """Verifica si un código de confirmación ya existe."""
    return db.query(Billete)\
        .filter(Billete.codigo_confirmacion == codigo)\
        .first() is not None

def generate_codigo_confirmacion(db: Session, length: int = 8) -> str:
    """
    Genera un código de confirmación único alfanumérico.
    Formato: ABCD1234 (8 caracteres por defecto)
    """
    characters = string.ascii_uppercase + string.digits
    
    while True:
        codigo = ''.join(secrets.choice(characters) for _ in range(length))
        if not codigo_confirmacion_exists(db, codigo):
            return codigo

def count_billetes_by_user(db: Session, user_id: int) -> int:
    """Cuenta los billetes de un usuario."""
    return db.query(Billete)\
        .join(Reserva, Billete.id_reserva == Reserva.id)\
        .filter(Reserva.id_usuario == user_id)\
        .count()

def get_billete_details(db: Session, billete_id: int) -> Optional[dict]:
    """
    Obtiene los detalles completos de un billete en formato dict.
    Útil para mostrar en confirmación de compra.
    """
    billete = get_billete_by_id(db, billete_id)
    if not billete:
        return None
    
    reserva = billete.reserva
    
    return {
        "codigo_confirmacion": billete.codigo_confirmacion,
        "fecha_compra": billete.fecha_compra,
        "monto_total": float(reserva.monto_total),
        "estado_reserva": reserva.estado.value,
        "pasajeros": [
            {
                "nombre": p.nombre_completo,
                "documento": p.documento_identidad,
                "asiento": p.asiento.numero_asiento if p.asiento else None,
                "categoria": p.asiento.categoria.value if p.asiento else None
            }
            for p in reserva.pasajeros
        ],
        "tarjeta": {
            "ultimos_4_digitos": billete.tarjeta_credito.numero_tarjeta[-4:] if billete.tarjeta_credito else None,
            "nombre_titular": billete.tarjeta_credito.nombre_titular if billete.tarjeta_credito else None
        }
    }

def get_billete_confirmacion(db: Session, codigo: str) -> Optional[dict]:
    """
    Obtiene la confirmación de compra por código.
    Retorna un resumen limpio para mostrar al usuario.
    """
    billete = get_billete_by_codigo(db, codigo)
    if not billete:
        return None
    
    return {
        "codigo": billete.codigo_confirmacion,
        "fecha": billete.fecha_compra,
        "monto": float(billete.reserva.monto_total),
        "mensaje": "Compra realizada exitosamente",
        "estado": "Confirmado"
    }
