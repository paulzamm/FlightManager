from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect

from app.api.endpoints import auth, flights, reservas, billetes, tarjetas, users
from app.core.config import settings
from app.database.database import Base, engine
from app.database.models import (
    Usuario, Vuelo, Aeropuerto, Aerolinea, 
    TarjetaCredito, Asiento, Reserva, Pasajero, Billete
)

def create_tables():
    """
    Crea todas las tablas en la base de datos si no existen.
    Muestra información útil sobre el proceso.
    """
    try:
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        
        print("\n" + "="*60)
        print("🔍 VERIFICANDO BASE DE DATOS")
        print("="*60)
        
        if existing_tables:
            print(f"✅ Tablas existentes encontradas: {len(existing_tables)}")
            for table in existing_tables:
                print(f"   - {table}")
        else:
            print("⚠️  No se encontraron tablas existentes")
        
        print("\n🛠️  Creando tablas faltantes...")
        Base.metadata.create_all(bind=engine)
        
        # Verificar tablas después de la creación
        inspector = inspect(engine)
        final_tables = inspector.get_table_names()
        
        print(f"✅ Total de tablas en la base de datos: {len(final_tables)}")
        print("="*60 + "\n")
        
    except Exception as e:
        print("\n" + "="*60)
        print("❌ ERROR AL CREAR TABLAS")
        print("="*60)
        print(f"Error: {str(e)}")
        print("Verifica tu conexión a PostgreSQL y las credenciales en .env")
        print("="*60 + "\n")
        raise

# Creación de tablas (si no existen)
create_tables()

# Crear instancia de FastAPI
app = FastAPI(
    title="Flight Manager API",
    description="Sistema de Reserva de Vuelos - API REST completa",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc
)

# Configurar CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las fuentes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Autenticación"]
)

app.include_router(
    flights.router,
    prefix="/flights",
    tags=["Vuelos"]
)

app.include_router(
    reservas.router,
    prefix="/reservas",
    tags=["Reservas"]
)

app.include_router(
    billetes.router,
    prefix="/billetes",
    tags=["Billetes y Compra"]
)

app.include_router(
    tarjetas.router,
    prefix="/tarjetas",
    tags=["Tarjetas de Crédito"]
)

app.include_router(
    users.router,
    prefix="/users",
    tags=["Gestión de Usuario"]
)

# Endpoint raíz
@app.get("/", tags=["Root"])
def read_root():
    """
    Mensaje de bienvenida del sistema.
    """
    return {
        "message": "Bienvenido al Sistema de Reserva de Vuelos",
        "version": "1.0.0",
        "servicios_disponibles": [
            "Registro e inicio de sesión de usuarios",
            "Consulta de vuelos por horarios y tarifas",
            "Búsqueda avanzada con preferencias",
            "Reserva de vuelos con selección de asientos",
            "Compra de billetes con tarjeta de crédito",
            "Gestión de tarjetas de crédito",
            "Historial de reservas y billetes",
            "Modificación y cancelación de reservas",
            "Gestión de perfil de usuario"
        ],
        "documentacion": {
            "swagger_ui": "/docs",
            "redoc": "/redoc"
        },
        "endpoints_principales": {
            "autenticacion": "/auth",
            "vuelos": "/flights",
            "reservas": "/reservas",
            "billetes": "/billetes",
            "tarjetas": "/tarjetas",
            "usuario": "/users"
        }
    }

# Endpoint de health check
@app.get("/health", tags=["Health"])
def health_check():
    """
    Verifica que la API esté funcionando correctamente.
    """
    return {
        "status": "healthy",
        "service": "Flight Manager API",
        "version": "1.0.0"
    }

# Manejador de inicio
@app.on_event("startup")
async def startup_event():
    """
    Evento que se ejecuta al iniciar la aplicación.
    """
    print("\n" + "="*60)
    print("🚀 FLIGHT MANAGER API INICIADA")
    print("="*60)
    print("📝 Documentación Swagger: http://localhost:8000/docs")
    print("📘 Documentación ReDoc:   http://localhost:8000/redoc")
    print("🏥 Health Check:         http://localhost:8000/health")
    print("🔄 Servidor ejecutándose en: http://0.0.0.0:8000")
    print("="*60 + "\n")

# Manejador de cierre
@app.on_event("shutdown")
async def shutdown_event():
    """
    Evento que se ejecuta al cerrar la aplicación.
    """
    print("\n" + "="*60)
    print("👋 CERRANDO FLIGHT MANAGER API")
    print("="*60 + "\n")