from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.database import Usuario, EstadoReservaEnum
from app.schemas import reserva as reserva_schema
from app.crud import crud_reserva, crud_asiento, crud_pasajero
from app.core.security import get_current_user

router = APIRouter()

# --- CREAR RESERVA ---

@router.post("/", response_model=reserva_schema.ReservaResponse, status_code=status.HTTP_201_CREATED)
def create_reservation(
    reserva_data: reserva_schema.ReservaCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Crea una nueva reserva para el usuario autenticado.
    
    - Valida disponibilidad de asientos
    - Calcula el monto total automáticamente
    - Crea pasajeros asociados si se proporcionan
    - Marca asientos como 'Reservado'
    
    **Requiere autenticación JWT.**
    """
    # Validar que todos los asientos existan y estén disponibles
    asientos_ids = [p.id_asiento for p in reserva_data.pasajeros]
    
    for asiento_id in asientos_ids:
        asiento = crud_asiento.get_asiento_by_id(db, asiento_id)
        if not asiento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Asiento con ID {asiento_id} no encontrado"
            )
        
        if not crud_asiento.is_seat_available(db, asiento_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Asiento {asiento.numero_asiento} no está disponible"
            )
    
    # Calcular monto total
    from app.crud.crud_flight import get_flight_by_id
    
    # Obtener el vuelo del primer asiento para calcular tarifa base
    primer_asiento = crud_asiento.get_asiento_by_id(db, asientos_ids[0])
    vuelo = get_flight_by_id(db, primer_asiento.id_vuelo)
    
    monto_total = crud_reserva.calculate_total(db, asientos_ids, vuelo.tarifa_base)
    
    # Crear la reserva con pasajeros
    try:
        reserva = crud_reserva.create_reserva(
            db,
            user_id=current_user.id,
            monto_total=monto_total,
            pasajeros_data=[p.model_dump() for p in reserva_data.pasajeros]
        )
        
        return reserva
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la reserva: {str(e)}"
        )

# --- CONSULTAR RESERVAS ---

@router.get("/me", response_model=List[reserva_schema.ReservaResponse])
def get_my_reservations(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
    estado: str = None
):
    """
    Obtiene todas las reservas del usuario autenticado.
    
    - **estado** (opcional): Filtrar por estado (Pendiente, Confirmada, Cancelada)
    
    **Requiere autenticación JWT.**
    """
    if estado:
        try:
            estado_enum = EstadoReservaEnum[estado]
            reservas = crud_reserva.get_reservas_by_estado(db, current_user.id, estado_enum)
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Estado inválido. Usar: Pendiente, Confirmada, Cancelada"
            )
    else:
        reservas = crud_reserva.get_reservas_by_user(db, current_user.id)
    
    return reservas

@router.get("/{reserva_id}", response_model=reserva_schema.ReservaDetail)
def get_reservation_details(
    reserva_id: int = Path(..., description="ID de la reserva"),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene los detalles completos de una reserva específica.
    
    Incluye:
    - Información de la reserva
    - Lista de pasajeros
    - Asientos asignados
    - Billete (si ya fue comprado)
    
    **Requiere autenticación JWT.**
    """
    reserva = crud_reserva.get_reserva_by_id(db, reserva_id)
    
    if not reserva:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reserva con ID {reserva_id} no encontrada"
        )
    
    # Verificar que la reserva pertenece al usuario actual
    if reserva.id_usuario != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver esta reserva"
        )
    
    # Obtener resumen completo
    resumen = crud_reserva.get_reserva_summary(db, reserva_id)
    return resumen

# --- MODIFICAR RESERVA ---

@router.patch("/{reserva_id}/cancel", response_model=reserva_schema.ReservaResponse)
def cancel_reservation(
    reserva_id: int = Path(..., description="ID de la reserva"),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cancela una reserva existente.
    
    - Cambia el estado a 'Cancelada'
    - Libera los asientos (Disponible)
    - Solo se pueden cancelar reservas en estado Pendiente o Confirmada
    
    **Requiere autenticación JWT.**
    """
    reserva = crud_reserva.get_reserva_by_id(db, reserva_id)
    
    if not reserva:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reserva con ID {reserva_id} no encontrada"
        )
    
    # Verificar que la reserva pertenece al usuario actual
    if reserva.id_usuario != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para cancelar esta reserva"
        )
    
    # Verificar que se puede cancelar
    if not crud_reserva.is_reserva_cancelable(db, reserva_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Esta reserva no se puede cancelar (ya está cancelada o tiene billete asociado)"
        )
    
    # Cancelar reserva
    reserva_cancelada = crud_reserva.cancel_reserva(db, reserva_id)
    
    if not reserva_cancelada:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al cancelar la reserva"
        )
    
    return reserva_cancelada

@router.put("/{reserva_id}/pasajeros/{pasajero_id}/change-seat", response_model=dict)
def change_passenger_seat(
    reserva_id: int = Path(..., description="ID de la reserva"),
    pasajero_id: int = Path(..., description="ID del pasajero"),
    nuevo_asiento_id: int = None,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cambia el asiento de un pasajero dentro de una reserva.
    
    - Solo para reservas en estado Pendiente
    - Libera el asiento anterior
    - Reserva el nuevo asiento
    
    **Requiere autenticación JWT.**
    """
    # Verificar que la reserva existe y pertenece al usuario
    reserva = crud_reserva.get_reserva_by_id(db, reserva_id)
    
    if not reserva:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reserva con ID {reserva_id} no encontrada"
        )
    
    if reserva.id_usuario != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para modificar esta reserva"
        )
    
    if reserva.estado != EstadoReservaEnum.Pendiente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se pueden cambiar asientos en reservas Pendientes"
        )
    
    # Verificar que el nuevo asiento está disponible
    if not crud_asiento.is_seat_available(db, nuevo_asiento_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nuevo asiento no está disponible"
        )
    
    # Cambiar asiento
    pasajero_actualizado = crud_pasajero.change_pasajero_asiento(db, pasajero_id, nuevo_asiento_id)
    
    if not pasajero_actualizado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al cambiar el asiento"
        )
    
    return {
        "message": "Asiento cambiado exitosamente",
        "pasajero_id": pasajero_id,
        "nuevo_asiento_id": nuevo_asiento_id
    }

# --- ESTADÍSTICAS ---

@router.get("/me/count", response_model=dict)
def count_my_reservations(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cuenta las reservas del usuario por estado.
    
    **Requiere autenticación JWT.**
    """
    total = crud_reserva.count_reservas_by_user(db, current_user.id)
    pendientes = len(crud_reserva.get_reservas_by_estado(db, current_user.id, EstadoReservaEnum.Pendiente))
    confirmadas = len(crud_reserva.get_reservas_by_estado(db, current_user.id, EstadoReservaEnum.Confirmada))
    canceladas = len(crud_reserva.get_reservas_by_estado(db, current_user.id, EstadoReservaEnum.Cancelada))
    
    return {
        "user_id": current_user.id,
        "total_reservas": total,
        "pendientes": pendientes,
        "confirmadas": confirmadas,
        "canceladas": canceladas
    }
