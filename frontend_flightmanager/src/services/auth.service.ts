import { api } from './api.service';
import type { TokenResponse, User } from '../models/types';
import { store } from '../models/store';

export const authService = {
    /**
     * Login: Usa FormData especial para OAuth2PasswordRequestForm
     */
    login: async (email: string, password: string): Promise<TokenResponse> => {
        const formData = new FormData();
        formData.append('username', email); // FastAPI usa 'username'
        formData.append('password', password);

        // Usamos api.post pero con FormData
        return api.post<TokenResponse>('/auth/token', formData);
    },

    /**
     * Registro: Usa JSON normal
     */
    register: (nombre: string, email: string, password: string): Promise<User> => {
        return api.post<User>('/auth/register', {
            nombre_completo: nombre,
            email,
            password,
        });
    },

    /**
     * Obtiene la info del usuario logueado
     */
    getProfile: async (): Promise<User> => {
        const user = await api.get<User>('/auth/me');
        store.setUser(user); // Guarda el usuario en el store
        return user;
    },

    /**
     * Cierra sesión
     */
    logout: () => {
        store.clearToken();
    }
};