from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database import Usuario
from app.schemas import user as user_schema
from app.crud import crud_user
from app.core.security import get_current_user

router = APIRouter()

# --- PERFIL DE USUARIO ---

@router.get("/me/profile", response_model=user_schema.UserProfile)
def get_my_profile(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene el perfil completo del usuario autenticado.
    
    Incluye:
    - Información básica (nombre, email)
    - Estadísticas (reservas, billetes, tarjetas)
    - Fecha de registro
    
    **Requiere autenticación JWT.**
    """
    from app.crud import crud_reserva, crud_billete, crud_tarjeta
    
    # Obtener estadísticas
    total_reservas = crud_reserva.count_reservas_by_user(db, current_user.id)
    total_billetes = crud_billete.count_billetes_by_user(db, current_user.id)
    total_tarjetas = crud_tarjeta.count_tarjetas_by_user(db, current_user.id)
    
    # Calcular monto total gastado
    billetes = crud_billete.get_billetes_by_user(db, current_user.id)
    monto_total = sum([b.reserva.monto_total for b in billetes])
    
    return {
        "id": current_user.id,
        "nombre_completo": current_user.nombre_completo,
        "email": current_user.email,
        "fecha_creacion": current_user.fecha_creacion,
        "estadisticas": {
            "total_reservas": total_reservas,
            "total_billetes": total_billetes,
            "total_tarjetas": total_tarjetas,
            "monto_total_gastado": float(monto_total)
        }
    }

# --- ACTUALIZAR PERFIL ---

@router.put("/me", response_model=user_schema.User)
def update_my_profile(
    user_update: user_schema.UserUpdate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Actualiza el perfil del usuario autenticado.
    
    Permite actualizar:
    - Nombre completo
    - Email
    - Contraseña
    
    **Requiere autenticación JWT.**
    """
    # Si se actualiza el email, verificar que no esté en uso
    if user_update.email and user_update.email != current_user.email:
        existing_user = crud_user.get_user_by_email(db, user_update.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este email ya está registrado por otro usuario"
            )
    
    # Actualizar usuario
    usuario_actualizado = crud_user.update_user(db, current_user.id, user_update)
    
    if not usuario_actualizado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar el perfil"
        )
    
    return usuario_actualizado

# --- CAMBIAR CONTRASEÑA ---

@router.patch("/me/change-password", response_model=dict)
def change_my_password(
    password_data: user_schema.PasswordChange,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cambia la contraseña del usuario autenticado.
    
    Requiere:
    - Contraseña actual (para validación)
    - Nueva contraseña
    
    **Requiere autenticación JWT.**
    """
    from app.core.security import verify_password, get_password_hash
    
    # Verificar contraseña actual
    if not verify_password(password_data.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña actual es incorrecta"
        )
    
    # Validar que la nueva contraseña sea diferente
    if password_data.current_password == password_data.new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La nueva contraseña debe ser diferente a la actual"
        )
    
    # Actualizar contraseña
    user_update = user_schema.UserUpdate(password=password_data.new_password)
    usuario_actualizado = crud_user.update_user(db, current_user.id, user_update)
    
    if not usuario_actualizado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al cambiar la contraseña"
        )
    
    return {
        "success": True,
        "message": "Contraseña actualizada exitosamente"
    }

# --- ELIMINAR CUENTA ---

@router.delete("/me", status_code=status.HTTP_200_OK, response_model=dict)
def delete_my_account(
    confirmation: user_schema.AccountDeletion,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Elimina la cuenta del usuario autenticado.
    
    **ADVERTENCIA:** Esta acción es IRREVERSIBLE.
    
    Requiere:
    - Contraseña actual para confirmar
    - Confirmación explícita (confirmar_eliminacion = True)
    
    Elimina en cascada:
    - Todas las reservas
    - Todos los billetes
    - Todas las tarjetas
    
    **Requiere autenticación JWT.**
    """
    from app.core.security import verify_password
    
    # Validar confirmación
    if not confirmation.confirmar_eliminacion:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debes confirmar explícitamente la eliminación de tu cuenta"
        )
    
    # Verificar contraseña
    if not verify_password(confirmation.password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contraseña incorrecta"
        )
    
    # Verificar que no tenga reservas confirmadas o billetes pendientes
    from app.crud import crud_reserva
    from app.database import EstadoReservaEnum
    
    reservas_confirmadas = crud_reserva.get_reservas_by_estado(
        db, 
        current_user.id, 
        EstadoReservaEnum.Confirmada
    )
    
    if reservas_confirmadas:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No puedes eliminar tu cuenta mientras tengas {len(reservas_confirmadas)} reserva(s) confirmada(s). Cancélalas primero."
        )
    
    # Eliminar usuario (cascada eliminará todo lo asociado)
    eliminado = crud_user.delete_user(db, current_user.id)
    
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar la cuenta"
        )
    
    return {
        "success": True,
        "message": "Tu cuenta ha sido eliminada permanentemente",
        "user_id": current_user.id,
        "email": current_user.email
    }

# --- ESTADÍSTICAS PÚBLICAS ---

@router.get("/me/summary", response_model=dict)
def get_my_summary(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene un resumen rápido de la actividad del usuario.
    
    **Requiere autenticación JWT.**
    """
    from app.crud import crud_reserva, crud_billete, crud_tarjeta
    from app.database import EstadoReservaEnum
    
    # Estadísticas de reservas
    reservas_pendientes = len(crud_reserva.get_reservas_by_estado(
        db, current_user.id, EstadoReservaEnum.Pendiente
    ))
    reservas_confirmadas = len(crud_reserva.get_reservas_by_estado(
        db, current_user.id, EstadoReservaEnum.Confirmada
    ))
    
    # Estadísticas de billetes
    total_billetes = crud_billete.count_billetes_by_user(db, current_user.id)
    
    # Estadísticas de tarjetas
    total_tarjetas = crud_tarjeta.count_tarjetas_by_user(db, current_user.id)
    
    return {
        "usuario": {
            "nombre": current_user.nombre_completo,
            "email": current_user.email,
            "miembro_desde": current_user.fecha_creacion
        },
        "reservas": {
            "pendientes": reservas_pendientes,
            "confirmadas": reservas_confirmadas
        },
        "compras": {
            "total_billetes": total_billetes
        },
        "pagos": {
            "tarjetas_registradas": total_tarjetas
        }
    }
