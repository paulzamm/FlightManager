import './input.css'
import { handleRouteChange } from './controllers/router';
import { store } from './models/store';
import { authService } from './services/auth.service';

/**
 * Función de inicialización de la App
 */
const initApp = async () => {
    // 3. Escuchar cambios en el 'hash' de la URL
    window.addEventListener('hashchange', handleRouteChange);

    // 4. Cargar la ruta inicial cuando la página se carga
    window.addEventListener('load', async () => {
        // Si hay un token, verifica que sea válido y carga el perfil
        if (store.isAuthenticated()) {
            try {
                await authService.getProfile(); // Carga el usuario en el store
            } catch (error) {
                // El token es inválido o expiró
                store.clearToken();
            }
        }

        // Una vez verificado (o no) el token, maneja la ruta
        handleRouteChange();
    });
};

// Iniciar la aplicación
initApp();