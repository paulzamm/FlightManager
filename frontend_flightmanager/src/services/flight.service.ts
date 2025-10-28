import { api } from './api.service';
import type { FlightResult, AsientoResponse } from '../models/types';

export const flightService = {
    /**
     * Búsqueda simple de vuelos
     */
    searchFlights: (origen: string, destino: string, fecha: string): Promise<FlightResult[]> => {
        const params = new URLSearchParams({ origen, destino, fecha });
        return api.get<FlightResult[]>(`/flights/search?${params.toString()}`);
    },

    /**
     * Búsqueda avanzada
     */
    searchFlightsAdvanced: (params: {
        origen: string,
        destino: string,
        fecha: string,
        aerolinea?: string,
        categoria_asiento?: string,
        ordenar_por?: 'horario' | 'precio'
    }): Promise<FlightResult[]> => {
        const queryParams = new URLSearchParams(params as any);
        return api.get<FlightResult[]>(`/flights/search/advanced?${queryParams.toString()}`);
    },

    /**
     * Obtiene detalles de un vuelo
     */
    getFlightDetails: (id: number): Promise<FlightResult> => {
        return api.get<FlightResult>(`/flights/${id}`);
    },

    /**
     * Obtiene asientos de un vuelo
     */
    getFlightSeats: (id: number): Promise<AsientoResponse[]> => {
        return api.get<AsientoResponse[]>(`/flights/${id}/seats`);
    },
};