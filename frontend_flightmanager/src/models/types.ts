// --- Autenticación y Usuario ---
export interface TokenResponse {
    access_token: string;
    token_type: string;
}

export interface User {
    id: number;
    email: string;
    nombre_completo: string;
    fecha_creacion: string;
}

export interface UserProfile extends User {
    estadisticas: {
        total_reservas: number;
        total_billetes: number;
        total_tarjetas: number;
        monto_total_gastado: number;
    };
}

// --- Vuelos y Aeropuertos ---
export interface Aeropuerto {
    id: number;
    codigo_iata: string;
    nombre: string;
    ciudad: string;
    pais: string;
}

export interface Aerolinea {
    id: number;
    nombre: string;
    codigo_iata: string;
}

export interface FlightResult {
    id: number;
    numero_vuelo: string;
    hora_salida: string; // ISO DateTime String
    hora_llegada: string; // ISO DateTime String
    tarifa_base: number;
    estado: string;
    aerolinea: Aerolinea;
    origen: Aeropuerto;
    destino: Aeropuerto;
}

export interface AsientoResponse {
    id: number;
    numero_asiento: string;
    categoria: 'Economica' | 'Business' | 'PrimeraClase';
    precio_adicional: number;
    estado: 'Disponible' | 'Reservado' | 'Ocupado';
}

// --- Reservas y Pasajeros ---
export interface PasajeroCreate {
    id_asiento: number;
    nombre_completo: string;
    documento_identidad: string;
}

export interface PasajeroResponse extends PasajeroCreate {
    id: number;
    id_reserva: number;
}

export interface ReservaResponse {
    id: number;
    id_usuario: number;
    fecha_reserva: string;
    estado: 'Pendiente' | 'Confirmada' | 'Cancelada';
    monto_total: number;
}

export interface ReservaDetail extends ReservaResponse {
    pasajeros: PasajeroResponse[];
    billete: BilleteResponse | null;
}

// --- Pagos y Billetes ---
export interface TarjetaSegura {
    id: number;
    ultimos_4_digitos: string;
    fecha_expiracion: string;
    nombre_titular: string;
    es_predeterminada: boolean;
}

export interface BilleteResponse {
    id: number;
    id_reserva: number;
    id_tarjeta_credito: number;
    codigo_confirmacion: string;
    fecha_compra: string;
}

export interface BilleteConfirmacion {
    id: number;
    codigo_confirmacion: string;
    fecha_compra: string;
    monto_total: number;
    mensaje: string;
}

// --- Estado de la App (para el flujo de reserva) ---
export interface BookingState {
    flight: FlightResult;
    selectedSeats: AsientoResponse[];
}