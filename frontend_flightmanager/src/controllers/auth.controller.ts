import { LoginView } from '../views/login.view';
import { authService } from '../services/auth.service';
import { store } from '../models/store';

/**
 * Inicializa la página de Login
 */
export const init = (_params: any, title: string) => {
    document.title = title;
    LoginView.bindLogin(handleLogin);
    LoginView.bindRegister(handleRegister);
};

/**
 * Maneja el evento de submit del formulario de Login
 */
const handleLogin = async (e: SubmitEvent) => {
    e.preventDefault();
    const form = e.target as HTMLFormElement;
    const email = (form.elements.namedItem('login-email') as HTMLInputElement).value;
    const password = (form.elements.namedItem('login-password') as HTMLInputElement).value;

    try {
        const { access_token } = await authService.login(email, password);
        store.setToken(access_token);
        await authService.getProfile(); // Obtener y guardar datos del usuario

        window.location.hash = '/search'; // Redirigir al dashboard

    } catch (error: any) {
        LoginView.displayLoginMessage(error.message, true);
    }
};

/**
 * Maneja el evento de submit del formulario de Registro
 */
const handleRegister = async (e: SubmitEvent) => {
    e.preventDefault();
    const form = e.target as HTMLFormElement;
    const nombre = (form.elements.namedItem('register-name') as HTMLInputElement).value;
    const email = (form.elements.namedItem('register-email') as HTMLInputElement).value;
    const password = (form.elements.namedItem('register-password') as HTMLInputElement).value;

    try {
        await authService.register(nombre, email, password);
        LoginView.displayRegisterMessage('¡Registro exitoso! Ahora puedes iniciar sesión.', false);
        form.reset();
    } catch (error: any) {
        LoginView.displayRegisterMessage(error.message, true);
    }
};

/**
 * Maneja el clic en el botón de Logout
 */
export const handleLogout = () => {
    authService.logout();
    window.location.hash = '/login';
};