import { api } from './api.service';
import type { UserProfile } from '../models/types';

export const userService = {

    getFullProfile: (): Promise<UserProfile> => {
        return api.get<UserProfile>('/users/me/profile');
    },

    updateProfile: (nombre: string, email: string): Promise<UserProfile> => {
        return api.put<UserProfile>('/users/me', {
            nombre_completo: nombre,
            email: email,
        });
    },

    changePassword: (actual: string, nueva: string): Promise<{ message: string }> => {
        return api.patch<{ message: string }>('/users/me/change-password', {
            current_password: actual,
            new_password: nueva,
        });
    },
};