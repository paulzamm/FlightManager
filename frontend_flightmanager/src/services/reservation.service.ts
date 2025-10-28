import { api } from './api.service';
import type { PasajeroCreate, ReservaDetail, ReservaResponse } from '../models/types';

export const reservationService = {
    /**
     * Crea una nueva reserva
     */
    createReservation: (pasajeros: PasajeroCreate[]): Promise<ReservaResponse> => {
        return api.post<ReservaResponse>('/reservas/', { pasajeros });
    },

    /**
     * Obtiene todas las reservas del usuario
     */
    getMyReservations: (estado?: 'Pendiente' | 'Confirmada' | 'Cancelada'): Promise<ReservaDetail[]> => {
        let endpoint = '/reservas/me';
        if (estado) {
            endpoint += `?estado=${estado}`;
        }
        return api.get<ReservaDetail[]>(endpoint);
    },

    /**
     * Obtiene el detalle de una reserva
     */
    getReservationDetails: (id: number): Promise<ReservaDetail> => {
        return api.get<ReservaDetail>(`/reservas/${id}`);
    },

    /**
     * Cancela una reserva
     */
    cancelReservation: (id: number): Promise<ReservaResponse> => {
        return api.patch<ReservaResponse>(`/reservas/${id}/cancel`, {});
    },
};