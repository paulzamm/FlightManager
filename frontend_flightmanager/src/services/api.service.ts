import { store } from '../models/store';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

type HttpMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';

async function apiFetch<T>(endpoint: string, method: HttpMethod, body: any = null): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    const token = store.getToken();

    const headers = new Headers();
    headers.set('Accept', 'application/json');

    // No poner Content-Type si es FormData (para el login)
    if (body && !(body instanceof FormData)) {
        headers.set('Content-Type', 'application/json');
    }

    if (token) {
        headers.set('Authorization', `Bearer ${token}`);
    }

    const config: RequestInit = {
        method,
        headers,
    };

    if (body) {
        config.body = (body instanceof FormData) ? body : JSON.stringify(body);
    }

    try {
        const response = await fetch(url, config);

        if (response.status === 401) {
            if(endpoint.includes('/auth/token')){
                const errorText = await response.text();
                try{
                    const errorData = JSON.parse(errorText);
                    throw new Error(errorData.detail || 'Email o contraseña incorrectos.');
                } catch {
                    throw new Error('Email o contraseña incorrectos.');
                }
            }else{
                store.clearToken();
                window.location.hash = '/login'; // Redirigir al login
                throw new Error('Sesión expirada. Por favor, inicia sesión de nuevo.');
            }
        }

        if (!response.ok) {
            const errorData = await response.json();
            
            // Manejo especial para errores de validación (422)
            if (response.status === 422 && errorData.detail) {
                // Si detail es un array de errores de validación
                if (Array.isArray(errorData.detail)) {
                    const errors = errorData.detail.map((err: any) => {
                        const field = err.loc ? err.loc[err.loc.length - 1] : 'campo';
                        return `${field}: ${err.msg}`;
                    }).join(', ');
                    throw new Error(`Error de validación: ${errors}`);
                }
                throw new Error(errorData.detail);
            }
            
            throw new Error(errorData.detail || 'Ocurrió un error en la petición.');
        }

        if (response.status === 204) { // No Content
            return null as T;
        }

        return (await response.json()) as T;

    } catch (error) {
        console.error(`Error en apiFetch (${method} ${endpoint}):`, error);
        throw error;
    }
}

// Exportamos métodos específicos
export const api = {
    get: <T>(endpoint: string) => apiFetch<T>(endpoint, 'GET'),
    post: <T>(endpoint: string, body: any) => apiFetch<T>(endpoint, 'POST', body),
    put: <T>(endpoint: string, body: any) => apiFetch<T>(endpoint, 'PUT', body),
    patch: <T>(endpoint: string, body: any) => apiFetch<T>(endpoint, 'PATCH', body),
    delete: <T>(endpoint: string) => apiFetch<T>(endpoint, 'DELETE'),
};