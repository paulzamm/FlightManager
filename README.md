# ✈️ FlightManager - Sistema de Reserva de Vuelos

Sistema completo de reserva de vuelos desarrollado con **FastAPI** (Backend) y **TypeScript + Vite** (Frontend). Proyecto académico para la materia de Programación Móvil.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.5-green)
![TypeScript](https://img.shields.io/badge/TypeScript-5.6-blue)
![Vite](https://img.shields.io/badge/Vite-6.0-purple)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)

## 📋 Características

### Backend (FastAPI)
- ✅ **33 endpoints RESTful** organizados en 6 routers
- ✅ Autenticación JWT (30 minutos de expiración)
- ✅ 9 tablas relacionales con SQLAlchemy 2.0
- ✅ Validación con Pydantic v2
- ✅ Documentación automática con Swagger/OpenAPI
- ✅ Seguridad con bcrypt para contraseñas

### Frontend (TypeScript + Vite)
- ✅ Arquitectura **MVC** separada
- ✅ TypeScript puro
- ✅ Enrutamiento SPA con hash routing
- ✅ Componentes reutilizables
- ✅ Estilos con Tailwind CSS
- ✅ Validaciones en cliente

### Funcionalidades
- 🔐 Sistema de autenticación y registro
- 🔍 Búsqueda de vuelos (por horario, precio, aerolínea)
- 💺 Selección de asientos con mapa visual
- 🎫 Gestión de reservas (crear, cancelar, modificar)
- 💳 Gestión de tarjetas de crédito
- 🛫 Compra de billetes
- 👤 Perfil de usuario con estadísticas

---

## 🚀 Instalación y Configuración

### Requisitos Previos

- **Python 3.13+** ([Descargar](https://www.python.org/downloads/))
- **Node.js 18+** y npm ([Descargar](https://nodejs.org/))
- **PostgreSQL 16+** ([Descargar](https://www.postgresql.org/download/))
- **Git** ([Descargar](https://git-scm.com/downloads))

---

## 📦 1. Clonar el Repositorio

```bash
git clone https://github.com/paulzamm/FlightManager.git
cd FlightManager
```

---

## 🔧 2. Configuración del Backend

### 2.1 Crear Base de Datos PostgreSQL

Abre **pgAdmin** o **psql** y ejecuta:

```sql
CREATE DATABASE flightmanager_db;
```

### 2.2 Navegar a la carpeta del backend

```bash
cd backend_flightmanager
```

### 2.3 Crear y activar entorno virtual Python

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### 2.4 Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2.5 Configurar variables de entorno

Crea un archivo `.env` en la carpeta `backend_flightmanager/`:

```env
# Base de datos
DATABASE_URL=postgresql://postgres:tu_password@localhost:5432/flightmanager_db

# JWT Secret (genera uno aleatorio)
SECRET_KEY=tu_secret_key_super_segura_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> **Nota:** Reemplaza `tu_password` con tu contraseña de PostgreSQL.

### 2.6 Crear tablas de la base de datos

Las tablas se crean automáticamente al iniciar el servidor por primera vez.

### 2.7 (Opcional) Poblar con datos de prueba

```bash
python seed_data.py
```

Esto creará:
- 14 aeropuertos (Ecuador + internacional)
- 8 aerolíneas
- 19 vuelos con fechas válidas
- 8 usuarios de prueba
- Asientos automáticos por cada vuelo

### 2.8 Iniciar el servidor backend

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

✅ **Backend corriendo en:** http://localhost:8000  
📚 **Documentación Swagger:** http://localhost:8000/docs

---

## 🎨 3. Configuración del Frontend

### 3.1 Abrir nueva terminal y navegar al frontend

```bash
cd frontend_flightmanager
```

### 3.2 Instalar dependencias

```bash
npm install
```

### 3.3 Configurar variables de entorno

Crea un archivo `.env` en la carpeta `frontend_flightmanager/`:

```env
VITE_API_URL=http://localhost:8000
```

### 3.4 Iniciar el servidor de desarrollo

```bash
npm run dev
```

✅ **Frontend corriendo en:** http://localhost:5173

---

## 👥 Usuarios de Prueba

Después de ejecutar `seed_data.py`, puedes usar estos usuarios:

| Email | Password | Rol |
|-------|----------|-----|
| `juan.perez@example.com` | `password123` | Usuario |
| `maria.garcia@example.com` | `password123` | Usuario |
| `carlos.lopez@example.com` | `password123` | Usuario |
| `admin@flightmanager.com` | `admin123` | Admin |

---

## 📁 Estructura del Proyecto

```
FlightManager/
├── backend_flightmanager/          # API REST con FastAPI
│   ├── app/
│   │   ├── api/endpoints/          # 6 routers (auth, flights, reservas, etc.)
│   │   ├── core/                   # Seguridad, config
│   │   ├── crud/                   # Operaciones de base de datos
│   │   ├── database/               # Modelos SQLAlchemy
│   │   └── schemas/                # Esquemas Pydantic
│   ├── main.py                     # Punto de entrada
│   ├── seed_data.py                # Script de datos de prueba
│   └── requirements.txt
│
├── frontend_flightmanager/         # SPA con TypeScript + Vite
│   ├── src/
│   │   ├── controllers/            # Lógica de negocio (MVC)
│   │   ├── models/                 # Interfaces TypeScript + Store
│   │   ├── services/               # Comunicación con API
│   │   ├── views/                  # Componentes de página
│   │   └── main.ts                 # Entry point
│   ├── index.html
│   ├── package.json
│   └── vite.config.ts
│
└── README.md
```

---

## 🧪 Pruebas de la API

### Opción 1: Swagger UI (Recomendado)
1. Abre http://localhost:8000/docs
3. Clic en "Authorize", luego ingresa las credenciales
4. Prueba todos los endpoints

### Opción 2: REST Client (VS Code)
1. Instala la extensión **REST Client** en VS Code
2. Abre el archivo `backend_flightmanager/api-tests.http`
3. Ejecuta las peticiones con "Send Request"

---

## 🔄 Flujo de Uso Completo

1. **Registrarse** → `/auth/register`
2. **Iniciar sesión** → Obtener JWT token
3. **Buscar vuelos** → Por horario, precio o aerolínea
4. **Seleccionar asientos** → Mapa visual con categorías
5. **Crear reserva** → Agregar pasajeros y asignar asientos
6. **Registrar tarjeta** → Guardar método de pago
7. **Comprar billete** → Procesar pago
8. **Ver confirmación** → Código único de billete

---

## 📚 Tecnologías Utilizadas

### Backend
- **FastAPI 0.115.5** - Framework web moderno
- **SQLAlchemy 2.0.36** - ORM para PostgreSQL
- **Pydantic 2.10.3** - Validación de datos
- **python-jose** - JWT tokens
- **bcrypt 5.0.0** - Hash de contraseñas
- **psycopg2-binary** - Driver PostgreSQL

### Frontend
- **TypeScript 5.6** - Tipado estático
- **Vite 6.0** - Build tool ultra-rápido
- **Tailwind CSS 3.4** - Estilos utility-first
- **date-fns** - Manejo de fechas
- **Axios** - HTTP client

---

## 🐛 Solución de Problemas

### Error: "No module named 'app'"
**Solución:** Asegúrate de estar en la carpeta `backend_flightmanager/` y que el entorno virtual esté activado.

### Error: "FATAL: password authentication failed"
**Solución:** Verifica tu contraseña de PostgreSQL en el archivo `.env`.

### Error: "Port 8000 already in use"
**Solución:** Detén el proceso anterior o usa otro puerto:
```bash
uvicorn main:app --reload --port 8001
```

### Frontend no se conecta al backend
**Solución:** 
1. Verifica que el backend esté corriendo en http://localhost:8000
2. Revisa el archivo `.env` del frontend
3. Verifica CORS en `main.py` del backend

---

