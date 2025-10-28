import { api } from './api.service';
import type { TarjetaSegura, BilleteResponse, BilleteConfirmacion } from '../models/types';

export const paymentService = {
    // --- Tarjetas ---
    getMyCards: (): Promise<TarjetaSegura[]> => {
        return api.get<TarjetaSegura[]>('/tarjetas/me');
    },

    addCard: (numero: string, expiracion: string, nombre: string): Promise<TarjetaSegura> => {
        return api.post<TarjetaSegura>('/tarjetas/', {
            numero_tarjeta: numero,
            fecha_expiracion: expiracion,
            nombre_titular: nombre,
        });
    },

    deleteCard: (id: number): Promise<void> => {
        return api.delete<void>(`/tarjetas/${id}`);
    },

    // --- Billetes (Compra) ---
    purchaseTicket: (id_reserva: number, id_tarjeta: number): Promise<BilleteResponse> => {
        return api.post<BilleteResponse>('/billetes/purchase', {
            id_reserva,
            id_tarjeta,
        });
    },

    getMyTickets: (): Promise<BilleteResponse[]> => {
        return api.get<BilleteResponse[]>('/billetes/me');
    },

    getConfirmation: (codigo: string): Promise<BilleteConfirmacion> => {
        return api.get<BilleteConfirmacion>(`/billetes/confirmation/${codigo}`);
    }
};