from fastapi import APIRouter, Depends, HTTPException, status, Path, Body
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.database import Usuario, EstadoReservaEnum
from app.schemas import billete as billete_schema
from app.crud import crud_billete, crud_reserva, crud_tarjeta
from app.core.security import get_current_user

router = APIRouter()

# --- COMPRAR BILLETE ---

@router.post("/purchase", response_model=billete_schema.BilleteResponse, status_code=status.HTTP_201_CREATED)
def purchase_ticket(
    compra_data: billete_schema.BilleteCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Compra un billete para una reserva existente usando una tarjeta de crédito.
    
    **Proceso:**
    1. Valida que la reserva existe y pertenece al usuario
    2. Valida que la reserva está en estado Pendiente
    3. Valida que la tarjeta pertenece al usuario
    4. "Procesa" el pago (simulado)
    5. Genera billete con código de confirmación único
    6. Cambia reserva a estado 'Confirmada'
    7. Marca asientos como 'Ocupado'
    
    **Requiere autenticación JWT.**
    """
    # Validar reserva
    reserva = crud_reserva.get_reserva_by_id(db, compra_data.id_reserva)
    
    if not reserva:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reserva con ID {compra_data.id_reserva} no encontrada"
        )
    
    # Verificar que la reserva pertenece al usuario
    if reserva.id_usuario != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para comprar esta reserva"
        )
    
    # Verificar estado de la reserva
    if reserva.estado != EstadoReservaEnum.Pendiente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La reserva debe estar en estado Pendiente. Estado actual: {reserva.estado.value}"
        )
    
    # Validar que no tenga ya un billete
    billete_existente = crud_billete.get_billete_by_reserva(db, compra_data.id_reserva)
    if billete_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Esta reserva ya tiene un billete asociado"
        )
    
    # Validar tarjeta
    tarjeta = crud_tarjeta.get_tarjeta_by_id(db, compra_data.id_tarjeta)
    
    if not tarjeta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarjeta con ID {compra_data.id_tarjeta} no encontrada"
        )
    
    # Verificar que la tarjeta pertenece al usuario
    if not crud_tarjeta.user_has_tarjeta(db, current_user.id, compra_data.id_tarjeta):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Esta tarjeta no te pertenece"
        )
    
    # Crear billete (esto automáticamente confirma la reserva y ocupa los asientos)
    try:
        billete = crud_billete.create_billete(db, compra_data.id_reserva, compra_data.id_tarjeta)
        
        return billete
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar la compra: {str(e)}"
        )

# --- CONSULTAR BILLETES ---

@router.get("/me", response_model=List[billete_schema.BilleteResponse])
def get_my_tickets(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene el historial de billetes comprados por el usuario autenticado.
    
    Devuelve todos los billetes ordenados por fecha de compra (más reciente primero).
    
    **Requiere autenticación JWT.**
    """
    billetes = crud_billete.get_billetes_by_user(db, current_user.id)
    
    return billetes

@router.get("/confirmation/{codigo}", response_model=billete_schema.BilleteConfirmacion)
def get_ticket_by_confirmation_code(
    codigo: str = Path(..., description="Código de confirmación del billete (ej. ABCD1234)"),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene un billete usando el código de confirmación.
    
    Útil para consultar detalles del billete con el código único generado.
    
    **Requiere autenticación JWT.**
    """
    billete = crud_billete.get_billete_by_codigo(db, codigo)
    
    if not billete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Billete con código {codigo} no encontrado"
        )
    
    # Verificar que el billete pertenece al usuario
    if billete.reserva.id_usuario != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Este billete no te pertenece"
        )
    
    # Obtener resumen de confirmación
    confirmacion = crud_billete.get_billete_confirmacion(db, codigo)
    
    return confirmacion

@router.get("/{billete_id}", response_model=billete_schema.BilleteDetail)
def get_ticket_details(
    billete_id: int = Path(..., description="ID del billete"),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene los detalles completos de un billete específico.
    
    Incluye:
    - Información del billete
    - Detalles de la reserva
    - Lista de pasajeros
    - Información de vuelos
    - Asientos asignados
    
    **Requiere autenticación JWT.**
    """
    billete = crud_billete.get_billete_by_id(db, billete_id)
    
    if not billete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Billete con ID {billete_id} no encontrado"
        )
    
    # Verificar que el billete pertenece al usuario
    if billete.reserva.id_usuario != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Este billete no te pertenece"
        )
    
    # Obtener detalles completos
    detalles = crud_billete.get_billete_details(db, billete_id)
    
    return detalles

# --- SIMULACIÓN DE ENVÍO POR EMAIL ---

@router.post("/{billete_id}/send-email", response_model=dict)
def send_ticket_by_email(
    billete_id: int = Path(..., description="ID del billete"),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Simula el envío del billete por correo electrónico.
    
    En producción, esto integraría con un servicio de email como SendGrid o AWS SES.
    
    **Requiere autenticación JWT.**
    """
    billete = crud_billete.get_billete_by_id(db, billete_id)
    
    if not billete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Billete con ID {billete_id} no encontrado"
        )
    
    # Verificar que el billete pertenece al usuario
    if billete.reserva.id_usuario != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Este billete no te pertenece"
        )
    
    # Simulación de envío de email
    # En producción: integrar con SendGrid, AWS SES, Mailgun, etc.
    
    return {
        "success": True,
        "message": f"Billete enviado exitosamente a {current_user.email}",
        "codigo_confirmacion": billete.codigo_confirmacion,
        "email_destino": current_user.email,
        "nota": "Este es un envío simulado. En producción se integraría con un servicio de email real."
    }

# --- DISPONIBILIDAD EN MOSTRADOR ---

@router.get("/{billete_id}/pickup-info", response_model=dict)
def get_pickup_information(
    billete_id: int = Path(..., description="ID del billete"),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene información para recoger el billete en el mostrador del aeropuerto.
    
    Según los requisitos: "Los billetes estarán listos para ser recogidos 
    en el mostrador del aeropuerto antes de la salida del primer vuelo."
    
    **Requiere autenticación JWT.**
    """
    billete = crud_billete.get_billete_by_id(db, billete_id)
    
    if not billete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Billete con ID {billete_id} no encontrado"
        )
    
    # Verificar que el billete pertenece al usuario
    if billete.reserva.id_usuario != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Este billete no te pertenece"
        )
    
    # Obtener información del primer vuelo
    detalles = crud_billete.get_billete_details(db, billete_id)
    
    return {
        "codigo_confirmacion": billete.codigo_confirmacion,
        "instrucciones": "Presente este código de confirmación en el mostrador del aeropuerto",
        "documentos_requeridos": [
            "Documento de identidad válido",
            "Código de confirmación",
            "Tarjeta de crédito usada para la compra (opcional)"
        ],
        "recomendacion": "Llegue al aeropuerto al menos 2 horas antes de la salida del vuelo",
        "mostrador_disponible": True,
        "nota": "Su billete estará disponible para recogida en el mostrador de la aerolínea"
    }

# --- ESTADÍSTICAS ---

@router.get("/me/count", response_model=dict)
def count_my_tickets(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cuenta los billetes del usuario.
    
    **Requiere autenticación JWT.**
    """
    total = crud_billete.count_billetes_by_user(db, current_user.id)
    billetes = crud_billete.get_billetes_by_user(db, current_user.id)
    
    # Calcular monto total gastado
    monto_total = sum([b.reserva.monto_total for b in billetes])
    
    return {
        "user_id": current_user.id,
        "total_billetes": total,
        "monto_total_gastado": float(monto_total)
    }
