import { api } from './api.service';
import type { FlightResult, AsientoResponse } from '../models/types';

export const flightService = {
    /**
     * Lista TODOS los vuelos con paginación y filtros opcionales
     */
    listAllFlights: (params: {
        skip?: number,
        limit?: number,
        origen?: string,
        destino?: string,
        fecha_desde?: string,
        fecha_hasta?: string,
        aerolinea?: string,
        ordenar_por?: 'fecha' | 'precio' | 'aerolinea'
    }): Promise<FlightResult[]> => {
        const queryParams = new URLSearchParams();
        if (params.skip !== undefined) queryParams.append('skip', params.skip.toString());
        if (params.limit !== undefined) queryParams.append('limit', params.limit.toString());
        if (params.origen) queryParams.append('origen', params.origen);
        if (params.destino) queryParams.append('destino', params.destino);
        if (params.fecha_desde) queryParams.append('fecha_desde', params.fecha_desde);
        if (params.fecha_hasta) queryParams.append('fecha_hasta', params.fecha_hasta);
        if (params.aerolinea) queryParams.append('aerolinea', params.aerolinea);
        if (params.ordenar_por) queryParams.append('ordenar_por', params.ordenar_por);
        
        return api.get<FlightResult[]>(`/flights/?${queryParams.toString()}`);
    },

    /**
     * Búsqueda simple de vuelos (ordenado por horario)
     */
    searchFlights: (origen: string, destino: string, fecha: string): Promise<FlightResult[]> => {
        const params = new URLSearchParams({ origen, destino, fecha });
        return api.get<FlightResult[]>(`/flights/search?${params.toString()}`);
    },

    /**
     * Búsqueda ordenada por precio
     */
    searchByPrice: (origen: string, destino: string, fecha: string): Promise<FlightResult[]> => {
        const params = new URLSearchParams({ origen, destino, fecha });
        return api.get<FlightResult[]>(`/flights/search/by-price?${params.toString()}`);
    },

    /**
     * Búsqueda avanzada con múltiples filtros
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