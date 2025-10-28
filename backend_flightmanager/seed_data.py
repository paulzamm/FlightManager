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
    """Crear vuelos de prueba"""
    print("\n🛫 CREANDO VUELOS...")
    
    # Obtener aeropuertos específicos para rutas comunes
    uio = next(a for a in aeropuertos if a.codigo_iata == "UIO")
    gye = next(a for a in aeropuertos if a.codigo_iata == "GYE")
    cue = next(a for a in aeropuertos if a.codigo_iata == "CUE")
    mch = next(a for a in aeropuertos if a.codigo_iata == "MCH")
    bog = next(a for a in aeropuertos if a.codigo_iata == "BOG")
    lim = next(a for a in aeropuertos if a.codigo_iata == "LIM")
    mia = next(a for a in aeropuertos if a.codigo_iata == "MIA")
    mad = next(a for a in aeropuertos if a.codigo_iata == "MAD")
    
    # Fecha base para los vuelos (hoy + varios días)
    base_date = datetime.now()
    
    vuelos_data = [
        # Vuelos nacionales Ecuador
        {"numero_vuelo": "LA2451", "origen": uio, "destino": gye, "aerolinea": aerolineas[0], "dias": 1, "hora": 6, "duracion": 1, "precio": 89.99},
        {"numero_vuelo": "LA2452", "origen": gye, "destino": uio, "aerolinea": aerolineas[0], "dias": 1, "hora": 8, "duracion": 1, "precio": 89.99},
        {"numero_vuelo": "AV9823", "origen": uio, "destino": cue, "aerolinea": aerolineas[1], "dias": 2, "hora": 9, "duracion": 1, "precio": 75.50},
        {"numero_vuelo": "AV9824", "origen": cue, "destino": uio, "aerolinea": aerolineas[1], "dias": 2, "hora": 11, "duracion": 1, "precio": 75.50},
        {"numero_vuelo": "EQ142", "origen": gye, "destino": mch, "aerolinea": aerolineas[3], "dias": 1, "hora": 14, "duracion": 0.5, "precio": 65.00},
        {"numero_vuelo": "EQ143", "origen": mch, "destino": gye, "aerolinea": aerolineas[3], "dias": 1, "hora": 16, "duracion": 0.5, "precio": 65.00},
        {"numero_vuelo": "LA2489", "origen": uio, "destino": gye, "aerolinea": aerolineas[0], "dias": 2, "hora": 18, "duracion": 1, "precio": 95.00},
        {"numero_vuelo": "AV9801", "origen": gye, "destino": cue, "aerolinea": aerolineas[1], "dias": 3, "hora": 7, "duracion": 1, "precio": 80.00},
        
        # Vuelos internacionales - Sudamérica
        {"numero_vuelo": "AV8075", "origen": uio, "destino": bog, "aerolinea": aerolineas[1], "dias": 2, "hora": 10, "duracion": 2, "precio": 189.99},
        {"numero_vuelo": "AV8076", "origen": bog, "destino": uio, "aerolinea": aerolineas[1], "dias": 2, "hora": 14, "duracion": 2, "precio": 189.99},
        {"numero_vuelo": "LA2401", "origen": gye, "destino": lim, "aerolinea": aerolineas[0], "dias": 3, "hora": 11, "duracion": 2.5, "precio": 210.00},
        {"numero_vuelo": "LA2402", "origen": lim, "destino": gye, "aerolinea": aerolineas[0], "dias": 3, "hora": 15, "duracion": 2.5, "precio": 210.00},
        {"numero_vuelo": "CM491", "origen": uio, "destino": lim, "aerolinea": aerolineas[2], "dias": 4, "hora": 8, "duracion": 2.5, "precio": 199.50},
        
        # Vuelos internacionales - Norte América
        {"numero_vuelo": "AA945", "origen": gye, "destino": mia, "aerolinea": aerolineas[5], "dias": 5, "hora": 22, "duracion": 5, "precio": 450.00},
        {"numero_vuelo": "AA946", "origen": mia, "destino": gye, "aerolinea": aerolineas[5], "dias": 5, "hora": 15, "duracion": 5, "precio": 450.00},
        {"numero_vuelo": "LA2475", "origen": uio, "destino": mia, "aerolinea": aerolineas[0], "dias": 6, "hora": 23, "duracion": 5, "precio": 475.00},
        
        # Vuelos internacionales - Europa
        {"numero_vuelo": "IB6301", "origen": uio, "destino": mad, "aerolinea": aerolineas[6], "dias": 7, "hora": 20, "duracion": 11, "precio": 890.00},
        {"numero_vuelo": "IB6302", "origen": mad, "destino": uio, "aerolinea": aerolineas[6], "dias": 7, "hora": 10, "duracion": 11, "precio": 890.00},
        {"numero_vuelo": "KL755", "origen": gye, "destino": mad, "aerolinea": aerolineas[7], "dias": 8, "hora": 21, "duracion": 11, "precio": 920.00},
    ]
    
    vuelos = []
    for data in vuelos_data:
        fecha_salida = base_date + timedelta(days=data["dias"], hours=data["hora"])
        fecha_llegada = fecha_salida + timedelta(hours=data["duracion"])
        
        vuelo = Vuelo(
            numero_vuelo=data["numero_vuelo"],
            hora_salida=fecha_salida,
            hora_llegada=fecha_llegada,
            tarifa_base=data["precio"],
            estado=EstadoVueloEnum.Programado,
            id_aerolinea=data["aerolinea"].id,
            id_aeropuerto_origen=data["origen"].id,
            id_aeropuerto_destino=data["destino"].id
        )
        db.add(vuelo)
        vuelos.append(vuelo)
    
    db.commit()
    print(f"✅ {len(vuelos)} vuelos creados")
    return vuelos

def seed_asientos(db: Session, vuelos: list):
    """Crear asientos para cada vuelo"""
    print("\n💺 CREANDO ASIENTOS...")
    
    # Configuración de asientos por categoría
    configuraciones = {
        "internacional_largo": {  # Vuelos > 5 horas
            CategoriaAsientosEnum.PrimeraClase: {"filas": [1, 2], "columnas": ["A", "B", "C", "D"], "precio_adicional": 500.00},
            CategoriaAsientosEnum.Business: {"filas": [3, 4, 5, 6], "columnas": ["A", "B", "C", "D"], "precio_adicional": 250.00},
            CategoriaAsientosEnum.Economica: {"filas": range(7, 31), "columnas": ["A", "B", "C", "D", "E", "F"], "precio_adicional": 0.00},
        },
        "internacional_corto": {  # Vuelos 2-5 horas
            CategoriaAsientosEnum.Business: {"filas": [1, 2, 3], "columnas": ["A", "B", "C", "D"], "precio_adicional": 150.00},
            CategoriaAsientosEnum.Economica: {"filas": range(4, 25), "columnas": ["A", "B", "C", "D", "E", "F"], "precio_adicional": 0.00},
        },
        "nacional": {  # Vuelos < 2 horas
            CategoriaAsientosEnum.Economica: {"filas": range(1, 20), "columnas": ["A", "B", "C", "D", "E", "F"], "precio_adicional": 0.00},
        }
    }
    
    total_asientos = 0
    
    for vuelo in vuelos:
        # Determinar tipo de vuelo por duración
        duracion = (vuelo.hora_llegada - vuelo.hora_salida).total_seconds() / 3600
        
        if duracion > 5:
            config = configuraciones["internacional_largo"]
        elif duracion > 2:
            config = configuraciones["internacional_corto"]
        else:
            config = configuraciones["nacional"]
        
        # Crear asientos según configuración
        for categoria, detalles in config.items():
            filas = detalles["filas"]
            columnas = detalles["columnas"]
            precio_adicional = detalles["precio_adicional"]
            
            for fila in filas:
                for columna in columnas:
                    numero_asiento = f"{fila}{columna}"
                    
                    # Reservar algunos asientos aleatoriamente
                    estados = [EstadoAsientoEnum.Disponible] * 7 + [EstadoAsientoEnum.Ocupado] * 2 + [EstadoAsientoEnum.Reservado]
                    estado = random.choice(estados)
                    
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
