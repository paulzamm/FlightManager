"""
Script para poblar la base de datos con datos de prueba.
Ejecutar: python seed_data.py
"""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database.database import SessionLocal, engine
from app.database.models import (
    Usuario, Vuelo, Aeropuerto, Aerolinea, 
    Asiento, CategoriaAsientosEnum, EstadoAsientoEnum,
    EstadoVueloEnum
)
from app.core.security import get_password_hash
import random

def clear_database(db: Session):
    """Limpia todas las tablas (opcional, usar con cuidado)"""
    print("\n⚠️  LIMPIANDO BASE DE DATOS...")
    try:
        from sqlalchemy import text
        
        print("🔄 Reiniciando secuencias de IDs...")
        
        # Desactivar temporalmente las foreign key constraints
        db.execute(text("SET session_replication_role = 'replica';"))
        
        # Truncar tablas con CASCADE para resetear secuencias
        # TRUNCATE elimina todos los datos Y resetea los autoincrementables
        db.execute(text('TRUNCATE TABLE "Asientos", "Vuelos", "Aeropuertos", "Aerolineas", "Usuarios", "Reservas", "Pasajeros", "Billetes", "TarjetasCredito" RESTART IDENTITY CASCADE;'))
        
        # Reactivar las foreign key constraints
        db.execute(text("SET session_replication_role = 'origin';"))
        
        db.commit()
        
        print("✅ Base de datos limpiada y secuencias reiniciadas")
    except Exception as e:
        print(f"❌ Error al limpiar: {str(e)}")
        db.rollback()
        raise  # Re-lanzar el error para que se vea completo
        db.rollback()

def seed_aeropuertos(db: Session):
    """Crear aeropuertos de Ecuador e internacionales"""
    print("\n🏢 CREANDO AEROPUERTOS...")
    
    aeropuertos_data = [
        # Ecuador
        {"nombre": "Aeropuerto Internacional Mariscal Sucre", "codigo_iata": "UIO", "ciudad": "Quito", "pais": "Ecuador"},
        {"nombre": "Aeropuerto Internacional José Joaquín de Olmedo", "codigo_iata": "GYE", "ciudad": "Guayaquil", "pais": "Ecuador"},
        {"nombre": "Aeropuerto Mariscal Lamar", "codigo_iata": "CUE", "ciudad": "Cuenca", "pais": "Ecuador"},
        {"nombre": "Aeropuerto General Manuel Serrano", "codigo_iata": "MCH", "ciudad": "Machala", "pais": "Ecuador"},
        {"nombre": "Aeropuerto General Rivadeneira", "codigo_iata": "ESM", "ciudad": "Esmeraldas", "pais": "Ecuador"},
        
        # Internacional - América Latina
        {"nombre": "Aeropuerto Internacional El Dorado", "codigo_iata": "BOG", "ciudad": "Bogotá", "pais": "Colombia"},
        {"nombre": "Aeropuerto Internacional Jorge Chávez", "codigo_iata": "LIM", "ciudad": "Lima", "pais": "Perú"},
        {"nombre": "Aeropuerto Internacional Comodoro Arturo Merino Benítez", "codigo_iata": "SCL", "ciudad": "Santiago", "pais": "Chile"},
        {"nombre": "Aeropuerto Internacional de la Ciudad de México", "codigo_iata": "MEX", "ciudad": "Ciudad de México", "pais": "México"},
        {"nombre": "Aeropuerto Internacional de Tocumen", "codigo_iata": "PTY", "ciudad": "Ciudad de Panamá", "pais": "Panamá"},
        
        # Internacional - Norte América
        {"nombre": "Aeropuerto Internacional de Miami", "codigo_iata": "MIA", "ciudad": "Miami", "pais": "Estados Unidos"},
        {"nombre": "Aeropuerto Internacional John F. Kennedy", "codigo_iata": "JFK", "ciudad": "Nueva York", "pais": "Estados Unidos"},
        
        # Internacional - Europa
        {"nombre": "Aeropuerto Adolfo Suárez Madrid-Barajas", "codigo_iata": "MAD", "ciudad": "Madrid", "pais": "España"},
        {"nombre": "Aeropuerto Internacional Schiphol", "codigo_iata": "AMS", "ciudad": "Ámsterdam", "pais": "Países Bajos"},
    ]
    
    aeropuertos = []
    for data in aeropuertos_data:
        aeropuerto = Aeropuerto(**data)
        db.add(aeropuerto)
        aeropuertos.append(aeropuerto)
    
    db.commit()
    print(f"✅ {len(aeropuertos)} aeropuertos creados")
    return aeropuertos

def seed_aerolineas(db: Session):
    """Crear aerolíneas"""
    print("\n✈️  CREANDO AEROLÍNEAS...")
    
    aerolineas_data = [
        {"nombre": "LATAM Airlines", "codigo_iata": "LA"},
        {"nombre": "Avianca", "codigo_iata": "AV"},
        {"nombre": "Copa Airlines", "codigo_iata": "CM"},
        {"nombre": "TAME", "codigo_iata": "EQ"},
        {"nombre": "Aeromexico", "codigo_iata": "AM"},
        {"nombre": "American Airlines", "codigo_iata": "AA"},
        {"nombre": "Iberia", "codigo_iata": "IB"},
        {"nombre": "KLM", "codigo_iata": "KL"},
    ]
    
    aerolineas = []
    for data in aerolineas_data:
        aerolinea = Aerolinea(**data)
        db.add(aerolinea)
        aerolineas.append(aerolinea)
    
    db.commit()
    print(f"✅ {len(aerolineas)} aerolíneas creadas")
    return aerolineas

def seed_vuelos(db: Session, aeropuertos: list, aerolineas: list):
    """Crear vuelos de prueba con mayor variedad"""
    print("\n🛫 CREANDO VUELOS VARIADOS...")
    
    # Obtener aeropuertos específicos
    uio = next(a for a in aeropuertos if a.codigo_iata == "UIO")
    gye = next(a for a in aeropuertos if a.codigo_iata == "GYE")
    cue = next(a for a in aeropuertos if a.codigo_iata == "CUE")
    mch = next(a for a in aeropuertos if a.codigo_iata == "MCH")
    esm = next(a for a in aeropuertos if a.codigo_iata == "ESM")
    bog = next(a for a in aeropuertos if a.codigo_iata == "BOG")
    lim = next(a for a in aeropuertos if a.codigo_iata == "LIM")
    scl = next(a for a in aeropuertos if a.codigo_iata == "SCL")
    mex = next(a for a in aeropuertos if a.codigo_iata == "MEX")
    pty = next(a for a in aeropuertos if a.codigo_iata == "PTY")
    mia = next(a for a in aeropuertos if a.codigo_iata == "MIA")
    jfk = next(a for a in aeropuertos if a.codigo_iata == "JFK")
    mad = next(a for a in aeropuertos if a.codigo_iata == "MAD")
    ams = next(a for a in aeropuertos if a.codigo_iata == "AMS")
    
    # Fecha base (hoy)
    base_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Definir rutas con múltiples horarios
    rutas_config = [
        # VUELOS NACIONALES ECUADOR (alta frecuencia)
        {
            "ruta": (uio, gye, "Quito-Guayaquil"),
            "vuelos": [
                {"num": "LA2401", "aerolinea": 0, "hora": 6, "duracion": 0.75, "precio": 85.00},
                {"num": "AV9801", "aerolinea": 1, "hora": 8, "duracion": 0.75, "precio": 89.99},
                {"num": "LA2403", "aerolinea": 0, "hora": 10, "duracion": 0.75, "precio": 95.00},
                {"num": "EQ301", "aerolinea": 3, "hora": 12, "duracion": 0.75, "precio": 79.50},
                {"num": "LA2405", "aerolinea": 0, "hora": 14, "duracion": 0.75, "precio": 92.00},
                {"num": "AV9803", "aerolinea": 1, "hora": 16, "duracion": 0.75, "precio": 88.00},
                {"num": "LA2407", "aerolinea": 0, "hora": 18, "duracion": 0.75, "precio": 98.00},
                {"num": "EQ303", "aerolinea": 3, "hora": 20, "duracion": 0.75, "precio": 82.00},
            ]
        },
        {
            "ruta": (gye, uio, "Guayaquil-Quito"),
            "vuelos": [
                {"num": "LA2402", "aerolinea": 0, "hora": 7, "duracion": 0.75, "precio": 85.00},
                {"num": "AV9802", "aerolinea": 1, "hora": 9, "duracion": 0.75, "precio": 89.99},
                {"num": "LA2404", "aerolinea": 0, "hora": 11, "duracion": 0.75, "precio": 95.00},
                {"num": "EQ302", "aerolinea": 3, "hora": 13, "duracion": 0.75, "precio": 79.50},
                {"num": "LA2406", "aerolinea": 0, "hora": 15, "duracion": 0.75, "precio": 92.00},
                {"num": "AV9804", "aerolinea": 1, "hora": 17, "duracion": 0.75, "precio": 88.00},
                {"num": "LA2408", "aerolinea": 0, "hora": 19, "duracion": 0.75, "precio": 98.00},
            ]
        },
        {
            "ruta": (uio, cue, "Quito-Cuenca"),
            "vuelos": [
                {"num": "AV9810", "aerolinea": 1, "hora": 7, "duracion": 0.75, "precio": 72.00},
                {"num": "LA2420", "aerolinea": 0, "hora": 12, "duracion": 0.75, "precio": 75.50},
                {"num": "EQ310", "aerolinea": 3, "hora": 16, "duracion": 0.75, "precio": 68.00},
            ]
        },
        {
            "ruta": (cue, uio, "Cuenca-Quito"),
            "vuelos": [
                {"num": "AV9811", "aerolinea": 1, "hora": 9, "duracion": 0.75, "precio": 72.00},
                {"num": "LA2421", "aerolinea": 0, "hora": 14, "duracion": 0.75, "precio": 75.50},
                {"num": "EQ311", "aerolinea": 3, "hora": 18, "duracion": 0.75, "precio": 68.00},
            ]
        },
        {
            "ruta": (gye, mch, "Guayaquil-Machala"),
            "vuelos": [
                {"num": "EQ140", "aerolinea": 3, "hora": 8, "duracion": 0.5, "precio": 62.00},
                {"num": "EQ142", "aerolinea": 3, "hora": 14, "duracion": 0.5, "precio": 65.00},
                {"num": "EQ144", "aerolinea": 3, "hora": 19, "duracion": 0.5, "precio": 67.00},
            ]
        },
        {
            "ruta": (mch, gye, "Machala-Guayaquil"),
            "vuelos": [
                {"num": "EQ141", "aerolinea": 3, "hora": 10, "duracion": 0.5, "precio": 62.00},
                {"num": "EQ143", "aerolinea": 3, "hora": 16, "duracion": 0.5, "precio": 65.00},
            ]
        },
        {
            "ruta": (gye, esm, "Guayaquil-Esmeraldas"),
            "vuelos": [
                {"num": "EQ150", "aerolinea": 3, "hora": 9, "duracion": 0.67, "precio": 70.00},
                {"num": "EQ152", "aerolinea": 3, "hora": 15, "duracion": 0.67, "precio": 73.00},
            ]
        },
        
        # VUELOS INTERNACIONALES SUDAMÉRICA
        {
            "ruta": (uio, bog, "Quito-Bogotá"),
            "vuelos": [
                {"num": "AV8001", "aerolinea": 1, "hora": 8, "duracion": 2, "precio": 185.00},
                {"num": "LA2500", "aerolinea": 0, "hora": 14, "duracion": 2, "precio": 195.00},
                {"num": "AV8003", "aerolinea": 1, "hora": 19, "duracion": 2, "precio": 189.99},
            ]
        },
        {
            "ruta": (bog, uio, "Bogotá-Quito"),
            "vuelos": [
                {"num": "AV8002", "aerolinea": 1, "hora": 11, "duracion": 2, "precio": 185.00},
                {"num": "LA2501", "aerolinea": 0, "hora": 17, "duracion": 2, "precio": 195.00},
            ]
        },
        {
            "ruta": (gye, lim, "Guayaquil-Lima"),
            "vuelos": [
                {"num": "LA2550", "aerolinea": 0, "hora": 10, "duracion": 2.5, "precio": 205.00},
                {"num": "CM491", "aerolinea": 2, "hora": 15, "duracion": 2.5, "precio": 199.50},
                {"num": "LA2552", "aerolinea": 0, "hora": 20, "duracion": 2.5, "precio": 215.00},
            ]
        },
        {
            "ruta": (lim, gye, "Lima-Guayaquil"),
            "vuelos": [
                {"num": "LA2551", "aerolinea": 0, "hora": 13, "duracion": 2.5, "precio": 205.00},
                {"num": "CM492", "aerolinea": 2, "hora": 18, "duracion": 2.5, "precio": 199.50},
            ]
        },
        {
            "ruta": (uio, lim, "Quito-Lima"),
            "vuelos": [
                {"num": "LA2560", "aerolinea": 0, "hora": 9, "duracion": 2.5, "precio": 210.00},
                {"num": "CM493", "aerolinea": 2, "hora": 16, "duracion": 2.5, "precio": 205.00},
            ]
        },
        {
            "ruta": (gye, scl, "Guayaquil-Santiago"),
            "vuelos": [
                {"num": "LA2600", "aerolinea": 0, "hora": 22, "duracion": 6, "precio": 380.00},
                {"num": "LA2602", "aerolinea": 0, "hora": 8, "duracion": 6, "precio": 395.00},
            ]
        },
        {
            "ruta": (uio, pty, "Quito-Panamá"),
            "vuelos": [
                {"num": "CM111", "aerolinea": 2, "hora": 11, "duracion": 3, "precio": 245.00},
                {"num": "CM113", "aerolinea": 2, "hora": 18, "duracion": 3, "precio": 255.00},
            ]
        },
        
        # VUELOS INTERNACIONALES NORTEAMÉRICA
        {
            "ruta": (gye, mia, "Guayaquil-Miami"),
            "vuelos": [
                {"num": "AA940", "aerolinea": 5, "hora": 22, "duracion": 5, "precio": 445.00},
                {"num": "LA2700", "aerolinea": 0, "hora": 1, "duracion": 5, "precio": 460.00},
                {"num": "AA942", "aerolinea": 5, "hora": 14, "duracion": 5, "precio": 455.00},
            ]
        },
        {
            "ruta": (mia, gye, "Miami-Guayaquil"),
            "vuelos": [
                {"num": "AA941", "aerolinea": 5, "hora": 11, "duracion": 5, "precio": 445.00},
                {"num": "LA2701", "aerolinea": 0, "hora": 18, "duracion": 5, "precio": 460.00},
            ]
        },
        {
            "ruta": (uio, mia, "Quito-Miami"),
            "vuelos": [
                {"num": "LA2710", "aerolinea": 0, "hora": 23, "duracion": 5, "precio": 470.00},
                {"num": "AA950", "aerolinea": 5, "hora": 15, "duracion": 5, "precio": 485.00},
            ]
        },
        {
            "ruta": (uio, jfk, "Quito-Nueva York"),
            "vuelos": [
                {"num": "LA2720", "aerolinea": 0, "hora": 22, "duracion": 7, "precio": 590.00},
            ]
        },
        {
            "ruta": (gye, mex, "Guayaquil-México"),
            "vuelos": [
                {"num": "AM600", "aerolinea": 4, "hora": 10, "duracion": 6, "precio": 520.00},
                {"num": "AM602", "aerolinea": 4, "hora": 20, "duracion": 6, "precio": 535.00},
            ]
        },
        
        # VUELOS INTERNACIONALES EUROPA
        {
            "ruta": (uio, mad, "Quito-Madrid"),
            "vuelos": [
                {"num": "IB6301", "aerolinea": 6, "hora": 20, "duracion": 11, "precio": 880.00},
                {"num": "LA2800", "aerolinea": 0, "hora": 21, "duracion": 11, "precio": 920.00},
            ]
        },
        {
            "ruta": (mad, uio, "Madrid-Quito"),
            "vuelos": [
                {"num": "IB6302", "aerolinea": 6, "hora": 10, "duracion": 11, "precio": 880.00},
                {"num": "LA2801", "aerolinea": 0, "hora": 12, "duracion": 11, "precio": 920.00},
            ]
        },
        {
            "ruta": (gye, mad, "Guayaquil-Madrid"),
            "vuelos": [
                {"num": "KL755", "aerolinea": 7, "hora": 21, "duracion": 11, "precio": 910.00},
            ]
        },
        {
            "ruta": (uio, ams, "Quito-Amsterdam"),
            "vuelos": [
                {"num": "KL751", "aerolinea": 7, "hora": 22, "duracion": 12, "precio": 950.00},
            ]
        },
    ]
    
    vuelos = []
    
    # Generar vuelos para los próximos 15 días
    for dia_offset in range(0, 15):
        fecha_vuelo = base_date + timedelta(days=dia_offset)
        
        for ruta_config in rutas_config:
            origen, destino, nombre_ruta = ruta_config["ruta"]
            
            # No todos los vuelos operan todos los días
            # Vuelos nacionales: todos los días
            # Vuelos internacionales: algunos días
            if "Internacional" in nombre_ruta or "-" in nombre_ruta and nombre_ruta.split("-")[1] not in ["Guayaquil", "Quito", "Cuenca", "Machala", "Esmeraldas"]:
                if dia_offset % 2 != 0:  # Solo días pares para algunos internacionales
                    continue
            
            for vuelo_data in ruta_config["vuelos"]:
                fecha_salida = fecha_vuelo + timedelta(hours=vuelo_data["hora"])
                fecha_llegada = fecha_salida + timedelta(hours=vuelo_data["duracion"])
                
                vuelo = Vuelo(
                    numero_vuelo=f"{vuelo_data['num']}-D{dia_offset}",
                    hora_salida=fecha_salida,
                    hora_llegada=fecha_llegada,
                    tarifa_base=vuelo_data["precio"],
                    estado=EstadoVueloEnum.Programado,
                    id_aerolinea=aerolineas[vuelo_data["aerolinea"]].id,
                    id_aeropuerto_origen=origen.id,
                    id_aeropuerto_destino=destino.id
                )
                db.add(vuelo)
                vuelos.append(vuelo)
    
    db.commit()
    print(f"✅ {len(vuelos)} vuelos creados (múltiples horarios y fechas)")
    return vuelos

def seed_asientos(db: Session, vuelos: list):
    """Crear asientos variados para cada vuelo según su tipo"""
    print("\n💺 CREANDO ASIENTOS CON CONFIGURACIONES VARIADAS...")
    
    # Configuraciones de asientos por tipo de avión/duración
    configuraciones = {
        "largo_recorrido": {  # Vuelos > 8 horas (Transatlánticos)
            CategoriaAsientosEnum.PrimeraClase: {
                "filas": [1, 2], 
                "columnas": ["A", "B", "D", "E"], 
                "precio_adicional": 600.00
            },
            CategoriaAsientosEnum.Business: {
                "filas": range(3, 8), 
                "columnas": ["A", "B", "D", "E"], 
                "precio_adicional": 300.00
            },
            CategoriaAsientosEnum.Economica: {
                "filas": range(8, 35), 
                "columnas": ["A", "B", "C", "D", "E", "F", "G"], 
                "precio_adicional": 0.00
            },
        },
        "medio_recorrido": {  # Vuelos 3-8 horas (Internacional Américas)
            CategoriaAsientosEnum.Business: {
                "filas": range(1, 5), 
                "columnas": ["A", "B", "D", "E"], 
                "precio_adicional": 180.00
            },
            CategoriaAsientosEnum.Economica: {
                "filas": range(5, 28), 
                "columnas": ["A", "B", "C", "D", "E", "F"], 
                "precio_adicional": 0.00
            },
        },
        "corto_regional": {  # Vuelos 1.5-3 horas (Regional internacional)
            CategoriaAsientosEnum.Business: {
                "filas": range(1, 4), 
                "columnas": ["A", "B", "C", "D"], 
                "precio_adicional": 80.00
            },
            CategoriaAsientosEnum.Economica: {
                "filas": range(4, 22), 
                "columnas": ["A", "B", "C", "D", "E", "F"], 
                "precio_adicional": 0.00
            },
        },
        "nacional_grande": {  # Vuelos nacionales de rutas populares
            CategoriaAsientosEnum.Business: {
                "filas": range(1, 3), 
                "columnas": ["A", "B", "C", "D"], 
                "precio_adicional": 50.00
            },
            CategoriaAsientosEnum.Economica: {
                "filas": range(3, 25), 
                "columnas": ["A", "B", "C", "D", "E", "F"], 
                "precio_adicional": 0.00
            },
        },
        "nacional_pequeno": {  # Vuelos nacionales de rutas menos frecuentes
            CategoriaAsientosEnum.Business: {
                "filas": [1, 2], 
                "columnas": ["A", "B", "C", "D"], 
                "precio_adicional": 40.00
            },
            CategoriaAsientosEnum.Economica: {
                "filas": range(3, 16), 
                "columnas": ["A", "B", "C", "D"], 
                "precio_adicional": 0.00
            },
        },
    }
    
    total_asientos = 0
    vuelos_por_tipo = {
        "largo_recorrido": 0,
        "medio_recorrido": 0,
        "corto_regional": 0,
        "nacional_grande": 0,
        "nacional_pequeno": 0
    }
    
    for vuelo in vuelos:
        # Calcular duración del vuelo en horas
        duracion_horas = (vuelo.hora_llegada - vuelo.hora_salida).total_seconds() / 3600
        
        # Determinar tipo de configuración según duración
        if duracion_horas > 8:
            config_tipo = "largo_recorrido"
        elif duracion_horas > 3:
            config_tipo = "medio_recorrido"
        elif duracion_horas > 1.5:
            config_tipo = "corto_regional"
        elif duracion_horas > 0.6:
            config_tipo = "nacional_grande"
        else:
            config_tipo = "nacional_pequeno"
        
        vuelos_por_tipo[config_tipo] += 1
        config = configuraciones[config_tipo]
        
        # Crear asientos según configuración
        for categoria, detalles in config.items():
            filas = detalles["filas"]
            columnas = detalles["columnas"]
            precio_adicional = detalles["precio_adicional"]
            
            for fila in filas:
                for columna in columnas:
                    numero_asiento = f"{fila}{columna}"
                    
                    # Simular ocupación realista
                    # Primera Clase: 30% ocupada
                    # Business: 50% ocupada
                    # Económica: 70% ocupada
                    if categoria == CategoriaAsientosEnum.PrimeraClase:
                        estados_pool = [EstadoAsientoEnum.Disponible] * 7 + [EstadoAsientoEnum.Ocupado] * 2 + [EstadoAsientoEnum.Reservado] * 1
                    elif categoria == CategoriaAsientosEnum.Business:
                        estados_pool = [EstadoAsientoEnum.Disponible] * 5 + [EstadoAsientoEnum.Ocupado] * 4 + [EstadoAsientoEnum.Reservado] * 1
                    else:  # Económica
                        estados_pool = [EstadoAsientoEnum.Disponible] * 3 + [EstadoAsientoEnum.Ocupado] * 6 + [EstadoAsientoEnum.Reservado] * 1
                    
                    estado = random.choice(estados_pool)
                    
                    asiento = Asiento(
                        id_vuelo=vuelo.id,
                        numero_asiento=numero_asiento,
                        categoria=categoria,
                        estado=estado,
                        precio_adicional=precio_adicional
                    )
                    db.add(asiento)
                    total_asientos += 1
    
    db.commit()
    
    print(f"✅ {total_asientos} asientos creados")
    print(f"   Distribución por tipo de vuelo:")
    for tipo, cantidad in vuelos_por_tipo.items():
        print(f"   - {tipo.replace('_', ' ').title()}: {cantidad} vuelos")
    
    # Mostrar estadísticas de asientos por categoría
    print(f"\n   Asientos por categoría:")
    for categoria in [CategoriaAsientosEnum.PrimeraClase, CategoriaAsientosEnum.Business, CategoriaAsientosEnum.Economica]:
        count = db.query(Asiento).filter(Asiento.categoria == categoria).count()
        disponibles = db.query(Asiento).filter(
            Asiento.categoria == categoria,
            Asiento.estado == EstadoAsientoEnum.Disponible
        ).count()
        print(f"   - {categoria.value}: {count} total ({disponibles} disponibles)")


def seed_usuarios(db: Session):
    """Crear usuarios de prueba"""
    print("\n👤 CREANDO USUARIOS...")
    
    usuarios_data = [
        {"nombre": "Admin Usuario", "email": "admin@flightmanager.com", "password": "admin123"},
        {"nombre": "Juan Pérez", "email": "juan.perez@example.com", "password": "password123"},
        {"nombre": "María García", "email": "maria.garcia@example.com", "password": "password123"},
        {"nombre": "Carlos López", "email": "carlos.lopez@example.com", "password": "password123"},
        {"nombre": "Ana Martínez", "email": "ana.martinez@example.com", "password": "password123"},
        {"nombre": "Luis Torres", "email": "luis.torres@example.com", "password": "password123"},
        {"nombre": "Sofia Ramírez", "email": "sofia.ramirez@example.com", "password": "password123"},
        {"nombre": "Diego Flores", "email": "diego.flores@example.com", "password": "password123"},
    ]
    
    usuarios = []
    for data in usuarios_data:
        usuario = Usuario(
            nombre_completo=data["nombre"],
            email=data["email"],
            password_hash=get_password_hash(data["password"])
        )
        db.add(usuario)
        usuarios.append(usuario)
    
    db.commit()
    print(f"✅ {len(usuarios)} usuarios creados")
    
    # Mostrar credenciales de prueba
    print("\n" + "="*60)
    print("🔑 CREDENCIALES DE PRUEBA")
    print("="*60)
    for data in usuarios_data:
        print(f"📧 Email: {data['email']}")
        print(f"🔒 Password: {data['password']}")
        print("-" * 60)
    
    return usuarios

def main():
    """Función principal para ejecutar el seed"""
    print("\n" + "="*60)
    print("INICIANDO SEED DE DATOS DE PRUEBA")
    print("="*60)
    
    db = SessionLocal()
    
    try:
        # Preguntar si desea limpiar la base de datos
        respuesta = input("\n¿Deseas limpiar la base de datos antes de insertar? (s/n): ").lower()
        if respuesta == 's':
            clear_database(db)
        
        # Ejecutar seeds en orden
        aeropuertos = seed_aeropuertos(db)
        aerolineas = seed_aerolineas(db)
        vuelos = seed_vuelos(db, aeropuertos, aerolineas)
        seed_asientos(db, vuelos)
        usuarios = seed_usuarios(db)
        
        print("\n" + "="*60)
        print("✅ SEED COMPLETADO EXITOSAMENTE")
        print("="*60)
        print(f"📊 Resumen:")
        print(f"   - {len(aeropuertos)} aeropuertos")
        print(f"   - {len(aerolineas)} aerolíneas")
        print(f"   - {len(vuelos)} vuelos")
        print(f"   - {db.query(Asiento).count()} asientos")
        print(f"   - {len(usuarios)} usuarios")
        print("="*60)
        print("\n🚀 Ya puedes probar la API en: http://localhost:8000/docs")
        print("💡 Usa cualquiera de las credenciales mostradas arriba para hacer login\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    main()
