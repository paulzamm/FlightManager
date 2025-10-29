from fastapi import APIRouter, Depends, HTTPException, Query, status, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.database.database import get_db
from app.schemas import flight as flight_schema, asiento as asiento_schema
from app.crud import crud_flight, crud_asiento

router = APIRouter()

# --- LISTAR TODOS LOS VUELOS (PAGINADO) ---

@router.get("/", response_model=List[flight_schema.FlightResult])
def list_all_flights(
    skip: int = Query(0, ge=0, description="Número de registros a saltar (paginación)"),
    limit: int = Query(50, ge=1, le=100, description="Cantidad máxima de vuelos a devolver"),
    origen: Optional[str] = Query(None, description="Filtrar por código IATA de origen"),
    destino: Optional[str] = Query(None, description="Filtrar por código IATA de destino"),
    fecha_desde: Optional[date] = Query(None, description="Filtrar vuelos desde esta fecha"),
    fecha_hasta: Optional[date] = Query(None, description="Filtrar vuelos hasta esta fecha"),
    aerolinea: Optional[str] = Query(None, description="Filtrar por código o nombre de aerolínea"),
    ordenar_por: str = Query("fecha", description="Ordenar por: 'fecha', 'precio', 'aerolinea'"),
    db: Session = Depends(get_db)
):
    """
    **NUEVO:** Lista TODOS los vuelos disponibles con paginación y filtros opcionales.
    
    Permite al usuario ver todos los vuelos sin necesidad de especificar origen/destino.
    
    **Filtros opcionales:**
    - origen: Código IATA del aeropuerto de origen
    - destino: Código IATA del aeropuerto de destino
    - fecha_desde/fecha_hasta: Rango de fechas
    - aerolinea: Nombre o código de aerolínea
    - ordenar_por: 'fecha', 'precio', 'aerolinea'
    
    **Paginación:**
    - skip: Saltar N registros (para páginas)
    - limit: Máximo de resultados (1-100)
    """
    # Obtener todos los vuelos con filtros
    vuelos = crud_flight.get_all_flights_filtered(
        db,
        skip=skip,
        limit=limit,
        origen_iata=origen.upper() if origen else None,
        destino_iata=destino.upper() if destino else None,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        aerolinea=aerolinea
    )
    
    # Ordenar según preferencia
    if ordenar_por == "precio":
        vuelos = sorted(vuelos, key=lambda v: v.tarifa_base)
    elif ordenar_por == "aerolinea":
        vuelos = sorted(vuelos, key=lambda v: v.aerolinea.nombre)
    else:  # Por defecto por fecha/hora
        vuelos = sorted(vuelos, key=lambda v: v.hora_salida)
    
    return vuelos

# --- BÚSQUEDA DE VUELOS ---

@router.get("/search", response_model=List[flight_schema.FlightResult])
def search_available_flights(
    origen: str = Query(..., description="Código IATA de origen (ej. 'UIO', 'GYE')"),
    destino: str = Query(..., description="Código IATA de destino (ej. 'UIO', 'GYE')"),
    fecha: date = Query(..., description="Fecha de salida (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    Busca vuelos disponibles entre dos ciudades para una fecha específica.
    
    - **origen**: Código IATA del aeropuerto de origen
    - **destino**: Código IATA del aeropuerto de destino
    - **fecha**: Fecha de salida en formato YYYY-MM-DD
    
    Devuelve lista vacía si no hay vuelos disponibles.
    """
    vuelos = crud_flight.search_flights(
        db, 
        origen_iata=origen.upper(), 
        destino_iata=destino.upper(), 
        fecha=fecha
    )
    
    return vuelos

# --- BÚSQUEDA POR PRECIO ---

@router.get("/search/by-price", response_model=List[flight_schema.FlightResult])
def search_flights_by_price(
    origen: str = Query(..., description="Código IATA de origen"),
    destino: str = Query(..., description="Código IATA de destino"),
    fecha: date = Query(..., description="Fecha de salida"),
    db: Session = Depends(get_db)
):
    """
    **REQUISITO:** Consulta de vuelos ordenados por TARIFA (más baratos primero).
    
    Busca vuelos y los ordena por precio (tarifa_base + precio promedio de asientos).
    
    - **origen**: Código IATA del aeropuerto de origen
    - **destino**: Código IATA del aeropuerto de destino
    - **fecha**: Fecha de salida en formato YYYY-MM-DD
    """
    # Buscar vuelos
    vuelos = crud_flight.search_flights(
        db, 
        origen_iata=origen.upper(), 
        destino_iata=destino.upper(), 
        fecha=fecha
    )
    
    # Ordenar por tarifa_base (de menor a mayor)
    vuelos_ordenados = sorted(vuelos, key=lambda v: v.tarifa_base)
    
    return vuelos_ordenados

# --- BÚSQUEDA AVANZADA CON PREFERENCIAS ---

@router.get("/search/advanced", response_model=List[flight_schema.FlightResult])
def advanced_flight_search(
    origen: str = Query(..., description="Código IATA de origen"),
    destino: str = Query(..., description="Código IATA de destino"),
    fecha: date = Query(..., description="Fecha de salida"),
    aerolinea: Optional[str] = Query(None, description="Código IATA de aerolínea preferida (ej. 'LA', 'AV')"),
    categoria_asiento: Optional[str] = Query(None, description="Categoría preferida: Economica, Business, PrimeraClase"),
    ordenar_por: str = Query("horario", description="Ordenar por: 'horario' o 'precio'"),
    db: Session = Depends(get_db)
):
    """
    **REQUISITO:** Búsqueda con PREFERENCIAS.
    
    Permite filtrar y ordenar vuelos según:
    - Aerolínea preferida
    - Categoría de asiento deseada
    - Orden por horario o precio
    
    **NOTA:** La opción "solo_directos" está implementada por defecto 
    (el sistema actual solo maneja vuelos directos, no conexiones).
    """
    # Buscar vuelos base
    vuelos = crud_flight.search_flights(
        db, 
        origen_iata=origen.upper(), 
        destino_iata=destino.upper(), 
        fecha=fecha
    )
    
    # Filtrar por aerolínea si se especifica
    if aerolinea:
        vuelos = [v for v in vuelos if v.aerolinea.codigo_iata.upper() == aerolinea.upper()]
    
    # Filtrar por disponibilidad de categoría de asiento
    if categoria_asiento:
        vuelos_con_categoria = []
        for vuelo in vuelos:
            asientos_categoria = crud_asiento.get_seats_by_category(db, vuelo.id, categoria_asiento)
            if asientos_categoria:  # Si tiene asientos disponibles en esa categoría
                vuelos_con_categoria.append(vuelo)
        vuelos = vuelos_con_categoria
    
    # Ordenar según preferencia
    if ordenar_por == "precio":
        vuelos = sorted(vuelos, key=lambda v: v.tarifa_base)
    else:  # por defecto ordenar por horario
        vuelos = sorted(vuelos, key=lambda v: v.hora_salida)
    
    return vuelos

# --- DETALLES DE VUELO ---

@router.get("/{flight_id}", response_model=flight_schema.FlightResult)
def get_flight_details(flight_id: int = Path(..., description="ID del vuelo"), db: Session = Depends(get_db)):
    """
    Obtiene los detalles completos de un vuelo específico por su ID.
    """
    vuelo = crud_flight.get_flight_by_id(db, flight_id)
    
    if not vuelo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vuelo con ID {flight_id} no encontrado"
        )
    
    return vuelo

# --- ASIENTOS DISPONIBLES ---

@router.get("/{flight_id}/seats", response_model=List[asiento_schema.AsientoResponse])
def get_available_seats(
    flight_id: int = Path(..., description="ID del vuelo"),
    categoria: Optional[str] = Query(None, description="Filtrar por categoría: Economica, Business, PrimeraClase"),
    db: Session = Depends(get_db)
):
    """
    Obtiene todos los asientos disponibles de un vuelo.
    
    - **flight_id**: ID del vuelo
    - **categoria** (opcional): Filtrar por categoría de asiento
    
    Devuelve lista de asientos disponibles ordenados por número.
    """
    # Verificar que el vuelo existe
    vuelo = crud_flight.get_flight_by_id(db, flight_id)
    if not vuelo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vuelo con ID {flight_id} no encontrado"
        )
    
    # Verificar que el vuelo es reservable
    if not crud_flight.is_flight_bookable(db, flight_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este vuelo no está disponible para reservas (cancelado o sin asientos)"
        )
    
    # Obtener asientos según filtro
    if categoria:
        asientos = crud_asiento.get_seats_by_category(db, flight_id, categoria)
    else:
        asientos = crud_asiento.get_available_seats(db, flight_id)
    
    return asientos

@router.get("/{flight_id}/seats/count", response_model=dict)
def count_available_seats(
    flight_id: int = Path(..., description="ID del vuelo"),
    db: Session = Depends(get_db)
):
    """
    Cuenta los asientos disponibles por categoría para un vuelo.
    
    Devuelve un diccionario con el conteo por categoría y total.
    """
    # Verificar que el vuelo existe
    vuelo = crud_flight.get_flight_by_id(db, flight_id)
    if not vuelo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vuelo con ID {flight_id} no encontrado"
        )
    
    # Contar por categoría
    from app.database import CategoriaAsientosEnum
    
    economica = len(crud_asiento.get_seats_by_category(db, flight_id, CategoriaAsientosEnum.Economica.value))
    business = len(crud_asiento.get_seats_by_category(db, flight_id, CategoriaAsientosEnum.Business.value))
    primera = len(crud_asiento.get_seats_by_category(db, flight_id, CategoriaAsientosEnum.PrimeraClase.value))
    
    total = crud_asiento.count_available_seats(db, flight_id)
    
    return {
        "flight_id": flight_id,
        "total_disponibles": total,
        "por_categoria": {
            "economica": economica,
            "business": business,
            "primera_clase": primera
        }
    }