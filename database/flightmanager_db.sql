-- ENUM para tipos de estado y categoría para mantener la integridad de los datos.
CREATE TYPE "categoria_asiento" AS ENUM ('Economica', 'Business', 'PrimeraClase');

CREATE TYPE "estado_vuelo" AS ENUM ('Programado', 'EnHora', 'Retrasado', 'Cancelado');

CREATE TYPE "estado_reserva" AS ENUM ('Pendiente', 'Confirmada', 'Cancelada');

CREATE TYPE "estado_asiento" AS ENUM ('Disponible', 'Reservado', 'Ocupado');

-- 1. Tabla de Usuarios (Users)
-- Almacena la información de inicio de sesión y perfil.
CREATE TABLE "Usuarios" (
    "id" SERIAL PRIMARY KEY,
    "nombre_completo" VARCHAR(100) NOT NULL,
    "email" VARCHAR(100) UNIQUE NOT NULL,
    "password_hash" VARCHAR(255) NOT NULL, -- Para la contraseña hasheada
    "fecha_creacion" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabla de Tarjetas de Crédito (CreditCards)
-- Vinculada al usuario.
CREATE TABLE "TarjetasCredito" (
    "id" SERIAL PRIMARY KEY,
    "id_usuario" INT NOT NULL,
    "numero_tarjeta" VARCHAR(50) NOT NULL, -- En producción, esto debe ser tokenizado
    "fecha_expiracion" VARCHAR(10) NOT NULL,
    "nombre_titular" VARCHAR(100) NOT NULL,
    "es_predeterminada" BOOLEAN DEFAULT false,
    FOREIGN KEY ("id_usuario") REFERENCES "Usuarios" ("id") ON DELETE CASCADE
);

-- 3. Tabla de Aerolíneas (Airlines)
CREATE TABLE "Aerolineas" (
    "id" SERIAL PRIMARY KEY,
    "nombre" VARCHAR(100) UNIQUE NOT NULL,
    "codigo_iata" VARCHAR(3) UNIQUE NOT NULL -- Ej. "AA", "IB"
);

-- 4. Tabla de Aeropuertos (Airports)
CREATE TABLE "Aeropuertos" (
    "id" SERIAL PRIMARY KEY,
    "nombre" VARCHAR(100) NOT NULL,
    "codigo_iata" VARCHAR(3) UNIQUE NOT NULL, -- Ej. "JFK", "MAD"
    "ciudad" VARCHAR(100) NOT NULL,
    "pais" VARCHAR(100) NOT NULL
);

-- 5. Tabla de Vuelos (Flights)
-- El corazón del sistema de consultas.
CREATE TABLE "Vuelos" (
    "id" SERIAL PRIMARY KEY,
    "id_aerolinea" INT NOT NULL,
    "id_aeropuerto_origen" INT NOT NULL,
    "id_aeropuerto_destino" INT NOT NULL,
    "numero_vuelo" VARCHAR(10) NOT NULL,
    "hora_salida" TIMESTAMP NOT NULL,
    "hora_llegada" TIMESTAMP NOT NULL,
    "tarifa_base" DECIMAL(10, 2) NOT NULL, 
    "estado" "estado_vuelo" DEFAULT 'Programado',
    FOREIGN KEY ("id_aerolinea") REFERENCES "Aerolineas" ("id"),
    FOREIGN KEY ("id_aeropuerto_origen") REFERENCES "Aeropuertos" ("id"),
    FOREIGN KEY ("id_aeropuerto_destino") REFERENCES "Aeropuertos" ("id"),
    UNIQUE ("numero_vuelo", "hora_salida") -- Clave única para un vuelo
);

-- 6. Tabla de Asientos (Seats)
-- Define la capacidad y tipos de asientos de un vuelo.
CREATE TABLE "Asientos" (
    "id" SERIAL PRIMARY KEY,
    "id_vuelo" INT NOT NULL,
    "numero_asiento" VARCHAR(5) NOT NULL, -- Ej. "A1", "22F"
    "categoria" "categoria_asiento" NOT NULL,
    "estado" "estado_asiento" DEFAULT 'Disponible',
    "precio_adicional" DECIMAL(10, 2) DEFAULT 0, -- Costo extra por este asiento
    FOREIGN KEY ("id_vuelo") REFERENCES "Vuelos" ("id") ON DELETE CASCADE,
    UNIQUE ("id_vuelo", "numero_asiento") -- Un asiento es único por vuelo
);

-- 7. Tabla de Reservas (Reservations)
-- Agrupa los asientos/pasajeros que un usuario desea comprar.
CREATE TABLE "Reservas" (
    "id" SERIAL PRIMARY KEY,
    "id_usuario" INT NOT NULL,
    "fecha_reserva" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "estado" "estado_reserva" DEFAULT 'Pendiente',
    "monto_total" DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY ("id_usuario") REFERENCES "Usuarios" ("id")
);

-- 8. Tabla de Pasajeros (Passengers)
-- Tabla intermedia para asociar asientos y pasajeros a una reserva.
-- Esto permite múltiples pasajeros y múltiples vuelos (itinerarios) en una reserva.
CREATE TABLE "Pasajeros" (
    "id" SERIAL PRIMARY KEY,
    "id_reserva" INT NOT NULL,
    "id_asiento" INT NOT NULL,
    "nombre_completo" VARCHAR(100) NOT NULL,
    "documento_identidad" VARCHAR(50), -- Ej. Pasaporte
    FOREIGN KEY ("id_reserva") REFERENCES "Reservas" ("id") ON DELETE CASCADE,
    FOREIGN KEY ("id_asiento") REFERENCES "Asientos" ("id")
    -- Restricción para asegurar que el asiento no esté ya reservado.
    -- Esto se manejará mejor en la lógica del backend (CRUD).
);

-- 9. Tabla de Billetes (Tickets)
-- El resultado final de una compra.
CREATE TABLE "Billetes" (
    "id" SERIAL PRIMARY KEY,
    "id_reserva" INT UNIQUE NOT NULL, -- Un billete por reserva
    "id_tarjeta_credito" INT NOT NULL,
    "fecha_compra" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "codigo_confirmacion" VARCHAR(20) UNIQUE NOT NULL,
    FOREIGN KEY ("id_reserva") REFERENCES "Reservas" ("id"),
    FOREIGN KEY ("id_tarjeta_credito") REFERENCES "TarjetasCredito" ("id")
);