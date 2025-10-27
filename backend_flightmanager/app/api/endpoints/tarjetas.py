from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.database import Usuario
from app.schemas import tarjeta as tarjeta_schema
from app.crud import crud_tarjeta
from app.core.security import get_current_user

router = APIRouter()

# --- CREAR TARJETA ---

@router.post("/", response_model=tarjeta_schema.TarjetaResponse, status_code=status.HTTP_201_CREATED)
def register_credit_card(
    tarjeta_data: tarjeta_schema.TarjetaCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Registra una nueva tarjeta de crédito para el usuario autenticado.
    
    - Si es la primera tarjeta, se marca automáticamente como predeterminada
    - El número de tarjeta se almacena (en producción usar tokenización)
    
    **Requiere autenticación JWT.**
    """
    # Verificar que el usuario no tenga ya una tarjeta con el mismo número
    tarjetas_existentes = crud_tarjeta.get_tarjetas_by_user(db, current_user.id)
    
    for tarjeta in tarjetas_existentes:
        # Comparar últimos 4 dígitos para evitar duplicados
        if tarjeta.numero_tarjeta[-4:] == tarjeta_data.numero_tarjeta[-4:]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya tienes una tarjeta registrada con estos últimos 4 dígitos"
            )
    
    # Crear tarjeta
    try:
        nueva_tarjeta = crud_tarjeta.create_tarjeta(
            db,
            user_id=current_user.id,
            tarjeta_data=tarjeta_data
        )
        
        return nueva_tarjeta
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al registrar la tarjeta: {str(e)}"
        )

# --- CONSULTAR TARJETAS ---

@router.get("/me", response_model=List[tarjeta_schema.TarjetaSegura])
def get_my_credit_cards(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene todas las tarjetas registradas del usuario autenticado.
    
    **IMPORTANTE:** Por seguridad, solo devuelve los últimos 4 dígitos del número.
    
    **Requiere autenticación JWT.**
    """
    tarjetas = crud_tarjeta.get_tarjetas_by_user(db, current_user.id)
    
    # Convertir a formato seguro (solo últimos 4 dígitos)
    tarjetas_seguras = []
    for tarjeta in tarjetas:
        tarjeta_segura = crud_tarjeta.get_tarjeta_segura(db, tarjeta.id)
        tarjetas_seguras.append(tarjeta_segura)
    
    return tarjetas_seguras

@router.get("/me/default", response_model=tarjeta_schema.TarjetaSegura)
def get_default_credit_card(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene la tarjeta predeterminada del usuario.
    
    **Requiere autenticación JWT.**
    """
    tarjeta_default = crud_tarjeta.get_default_tarjeta(db, current_user.id)
    
    if not tarjeta_default:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No tienes tarjetas registradas"
        )
    
    # Devolver en formato seguro
    tarjeta_segura = crud_tarjeta.get_tarjeta_segura(db, tarjeta_default.id)
    
    return tarjeta_segura

@router.get("/{tarjeta_id}", response_model=tarjeta_schema.TarjetaSegura)
def get_credit_card(
    tarjeta_id: int = Path(..., description="ID de la tarjeta"),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene los detalles de una tarjeta específica (solo últimos 4 dígitos).
    
    **Requiere autenticación JWT.**
    """
    tarjeta = crud_tarjeta.get_tarjeta_by_id(db, tarjeta_id)
    
    if not tarjeta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarjeta con ID {tarjeta_id} no encontrada"
        )
    
    # Verificar que la tarjeta pertenece al usuario
    if not crud_tarjeta.user_has_tarjeta(db, current_user.id, tarjeta_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Esta tarjeta no te pertenece"
        )
    
    # Devolver en formato seguro
    tarjeta_segura = crud_tarjeta.get_tarjeta_segura(db, tarjeta_id)
    
    return tarjeta_segura

# --- ACTUALIZAR TARJETA ---

@router.patch("/{tarjeta_id}/set-default", response_model=tarjeta_schema.TarjetaResponse)
def set_default_credit_card(
    tarjeta_id: int = Path(..., description="ID de la tarjeta"),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Marca una tarjeta como predeterminada.
    
    - Desmarca automáticamente cualquier otra tarjeta predeterminada
    - Solo puedes marcar tus propias tarjetas
    
    **Requiere autenticación JWT.**
    """
    # Verificar que la tarjeta existe
    tarjeta = crud_tarjeta.get_tarjeta_by_id(db, tarjeta_id)
    
    if not tarjeta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarjeta con ID {tarjeta_id} no encontrada"
        )
    
    # Verificar que la tarjeta pertenece al usuario
    if not crud_tarjeta.user_has_tarjeta(db, current_user.id, tarjeta_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Esta tarjeta no te pertenece"
        )
    
    # Marcar como predeterminada
    tarjeta_actualizada = crud_tarjeta.set_default_tarjeta(db, current_user.id, tarjeta_id)
    
    if not tarjeta_actualizada:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al marcar la tarjeta como predeterminada"
        )
    
    return tarjeta_actualizada

@router.put("/{tarjeta_id}", response_model=tarjeta_schema.TarjetaResponse)
def update_credit_card(
    tarjeta_id: int = Path(..., description="ID de la tarjeta"),
    tarjeta_update: tarjeta_schema.TarjetaUpdate = None,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Actualiza los datos de una tarjeta.
    
    Permite actualizar:
    - Fecha de expiración
    - Nombre del titular
    
    **NO permite cambiar el número de tarjeta** (por seguridad).
    
    **Requiere autenticación JWT.**
    """
    # Verificar que la tarjeta existe
    tarjeta = crud_tarjeta.get_tarjeta_by_id(db, tarjeta_id)
    
    if not tarjeta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarjeta con ID {tarjeta_id} no encontrada"
        )
    
    # Verificar que la tarjeta pertenece al usuario
    if not crud_tarjeta.user_has_tarjeta(db, current_user.id, tarjeta_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Esta tarjeta no te pertenece"
        )
    
    # Actualizar tarjeta
    tarjeta_actualizada = crud_tarjeta.update_tarjeta(db, tarjeta_id, tarjeta_update)
    
    if not tarjeta_actualizada:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar la tarjeta"
        )
    
    return tarjeta_actualizada

# --- ELIMINAR TARJETA ---

@router.delete("/{tarjeta_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_credit_card(
    tarjeta_id: int = Path(..., description="ID de la tarjeta"),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Elimina una tarjeta de crédito.
    
    - Si era la predeterminada, automáticamente asigna otra como predeterminada
    - No se puede eliminar si tiene compras asociadas (protección de integridad)
    
    **Requiere autenticación JWT.**
    """
    # Verificar que la tarjeta existe
    tarjeta = crud_tarjeta.get_tarjeta_by_id(db, tarjeta_id)
    
    if not tarjeta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarjeta con ID {tarjeta_id} no encontrada"
        )
    
    # Verificar que la tarjeta pertenece al usuario
    if not crud_tarjeta.user_has_tarjeta(db, current_user.id, tarjeta_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Esta tarjeta no te pertenece"
        )
    
    # Verificar que no tenga billetes asociados
    from app.crud import crud_billete
    if hasattr(tarjeta, 'billetes') and len(tarjeta.billetes) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar una tarjeta con compras asociadas"
        )
    
    # Eliminar tarjeta
    eliminada = crud_tarjeta.delete_tarjeta(db, tarjeta_id)
    
    if not eliminada:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar la tarjeta"
        )
    
    return None

# --- ESTADÍSTICAS ---

@router.get("/me/count", response_model=dict)
def count_my_credit_cards(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cuenta las tarjetas registradas del usuario.
    
    **Requiere autenticación JWT.**
    """
    total = crud_tarjeta.count_tarjetas_by_user(db, current_user.id)
    
    return {
        "user_id": current_user.id,
        "total_tarjetas": total
    }
