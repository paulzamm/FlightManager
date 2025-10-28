import type { User, BookingState, FlightResult, AsientoResponse } from './types';

interface AppState {
    token: string | null;
    user: User | null;
    bookingFlow: BookingState | null; // Para pasar datos entre vistas
}

// Estado inicial cargado desde localStorage
const state: AppState = {
    token: localStorage.getItem('authToken'),
    user: JSON.parse(localStorage.getItem('authUser') || 'null'),
    bookingFlow: JSON.parse(sessionStorage.getItem('bookingFlow') || 'null'),
};

export const store = {
    // --- Autenticación ---
    setToken: (token: string): void => {
        state.token = token;
        localStorage.setItem('authToken', token);
    },

    clearToken: (): void => {
        state.token = null;
        state.user = null;
        localStorage.removeItem('authToken');
        localStorage.removeItem('authUser');
    },

    getToken: (): string | null => {
        return state.token;
    },

    isAuthenticated: (): boolean => {
        return state.token !== null;
    },

    // --- Usuario ---
    setUser: (user: User): void => {
        state.user = user;
        localStorage.setItem('authUser', JSON.stringify(user));
    },

    getUser: (): User | null => {
        return state.user;
    },

    // --- Flujo de Reserva ---
    setBookingFlow: (flight: FlightResult, selectedSeats: AsientoResponse[]): void => {
        const bookingData: BookingState = { flight, selectedSeats };
        state.bookingFlow = bookingData;
        // Usamos sessionStorage para que se borre al cerrar la pestaña
        sessionStorage.setItem('bookingFlow', JSON.stringify(bookingData));
    },

    getBookingFlow: (): BookingState | null => {
        return state.bookingFlow;
    },

    clearBookingFlow: (): void => {
        state.bookingFlow = null;
        sessionStorage.removeItem('bookingFlow');
    }
};