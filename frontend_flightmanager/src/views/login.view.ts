export const LoginView = {
    render: () => {
        const appElement = document.getElementById('app') as HTMLDivElement;
        appElement.innerHTML = `
        <div class="min-h-screen flex items-center justify-center bg-gray-900 p-4">
            <div class="bg-white rounded-lg shadow-xl w-full max-w-4xl flex overflow-hidden">
            
            <div class="w-1/2 p-8 border-r border-gray-200">
                <h2 class="text-2xl font-bold text-gray-800 mb-6 text-center">Registrarse</h2>
                <form id="register-form">
                <div id="register-message" class="mb-4 text-center text-sm"></div>
                <div class="mb-4">
                    <label class="block text-gray-700 text-sm font-bold mb-2" for="register-name">Nombre Completo</label>
                    <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700" id="register-name" type="text" placeholder="Nombre Apellido" required>
                </div>
                <div class="mb-4">
                    <label class="block text-gray-700 text-sm font-bold mb-2" for="register-email">Email</label>
                    <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700" id="register-email" type="email" placeholder="nombre.apellido@example.com" required>
                </div>
                <div class="mb-6">
                    <label class="block text-gray-700 text-sm font-bold mb-2" for="register-password">Contraseña</label>
                    <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700" id="register-password" type="password" required>
                </div>
                <button class="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" type="submit">
                    Crear Cuenta
                </button>
                </form>
            </div>
            
            <div class="w-1/2 p-8 bg-gray-50">
                <h2 class="text-2xl font-bold text-gray-800 mb-6 text-center">Iniciar Sesión</h2>
                <form id="login-form">
                <div id="login-message" class="mb-4 text-center text-sm text-red-500"></div>
                <div class="mb-4">
                    <label class="block text-gray-700 text-sm font-bold mb-2" for="login-email">Email</label>
                    <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700" id="login-email" type="email" placeholder="nombre.apellido@example.com" required>
                </div>
                <div class="mb-6">
                    <label class="block text-gray-700 text-sm font-bold mb-2" for="login-password">Contraseña</label>
                    <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700" id="login-password" type="password" required>
                </div>
                <button class="w-full bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded" type="submit">
                    Entrar
                </button>
                </form>
            </div>
            </div>
        </div>
    `;
    },

    // Métodos para interactuar con esta vista
    displayLoginMessage: (message: string, isError: boolean) => {
        const el = document.getElementById('login-message') as HTMLDivElement;
        el.textContent = message;
        el.className = `mb-4 text-center text-sm ${isError ? 'text-red-500' : 'text-green-500'}`;
    },

    displayRegisterMessage: (message: string, isError: boolean) => {
        const el = document.getElementById('register-message') as HTMLDivElement;
        el.textContent = message;
        el.className = `mb-4 text-center text-sm ${isError ? 'text-red-500' : 'text-green-500'}`;
    },

    bindLogin: (handler: (e: SubmitEvent) => void) => {
        document.getElementById('login-form')?.addEventListener('submit', handler);
    },

    bindRegister: (handler: (e: SubmitEvent) => void) => {
        document.getElementById('register-form')?.addEventListener('submit', handler);
    }
};