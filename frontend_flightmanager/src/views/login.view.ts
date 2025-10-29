export const LoginView = {
    render: () => {
        const appElement = document.getElementById('app') as HTMLDivElement;
        appElement.innerHTML = `
        <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900 p-4">
            <div class="bg-white rounded-2xl shadow-2xl w-full max-w-4xl flex overflow-hidden border border-gray-200">
            
            <div class="w-1/2 p-10 border-r border-gray-200">
                <h2 class="text-3xl font-bold text-gray-900 mb-2 text-center">Registrarse</h2>
                <p class="text-gray-600 text-center mb-6 text-sm">Crea tu cuenta para empezar</p>
                <form id="register-form">
                <div id="register-message" class="mb-4 text-center text-sm font-medium"></div>
                <div class="mb-4">
                    <label class="block text-gray-800 text-sm font-semibold mb-2" for="register-name">Nombre Completo</label>
                    <input class="w-full px-4 py-3 text-base border-2 border-gray-300 rounded-lg shadow-sm 
                                bg-white placeholder-gray-400 
                                focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 
                                hover:border-blue-300 transition-all duration-200" 
                        id="register-name" type="text" placeholder="Nombre Apellido" required>
                </div>
                <div class="mb-4">
                    <label class="block text-gray-800 text-sm font-semibold mb-2" for="register-email">Email</label>
                    <input class="w-full px-4 py-3 text-base border-2 border-gray-300 rounded-lg shadow-sm 
                                bg-white placeholder-gray-400 
                                focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 
                                hover:border-blue-300 transition-all duration-200" 
                        id="register-email" type="email" placeholder="nombre.apellido@example.com" required>
                </div>
                <div class="mb-6">
                    <label class="block text-gray-800 text-sm font-semibold mb-2" for="register-password">Contraseña</label>
                    <input class="w-full px-4 py-3 text-base border-2 border-gray-300 rounded-lg shadow-sm 
                                bg-white placeholder-gray-400 
                                focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 
                                hover:border-blue-300 transition-all duration-200" 
                        id="register-password" type="password" placeholder="Tu contraseña" required>
                </div>
                <button class="w-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 
                            text-white font-bold py-3 px-6 rounded-xl text-base 
                            shadow-lg hover:shadow-xl transform hover:scale-[1.02] 
                            transition-all duration-200 
                            focus:outline-none focus:ring-4 focus:ring-blue-300" type="submit">
                    Crear Cuenta
                </button>
                </form>
            </div>
            
            <div class="w-1/2 p-10 bg-gradient-to-br from-gray-50 to-gray-100">
                <h2 class="text-3xl font-bold text-gray-900 mb-2 text-center">Iniciar Sesión</h2>
                <p class="text-gray-600 text-center mb-6 text-sm">Accede a tu cuenta</p>
                <form id="login-form">
                <div id="login-message" class="mb-4 text-center text-sm font-medium"></div>
                <div class="mb-4">
                    <label class="block text-gray-800 text-sm font-semibold mb-2" for="login-email">Email</label>
                    <input class="w-full px-4 py-3 text-base border-2 border-gray-300 rounded-lg shadow-sm 
                                bg-white placeholder-gray-400 
                                focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 
                                hover:border-green-300 transition-all duration-200" 
                        id="login-email" type="email" placeholder="nombre.apellido@example.com" required>
                </div>
                <div class="mb-6">
                    <label class="block text-gray-800 text-sm font-semibold mb-2" for="login-password">Contraseña</label>
                    <input class="w-full px-4 py-3 text-base border-2 border-gray-300 rounded-lg shadow-sm 
                                bg-white placeholder-gray-400 
                                focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 
                                hover:border-green-300 transition-all duration-200" 
                        id="login-password" type="password" placeholder="Tu contraseña" required>
                </div>
                <button class="w-full bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 
                            text-white font-bold py-3 px-6 rounded-xl text-base 
                            shadow-lg hover:shadow-xl transform hover:scale-[1.02] 
                            transition-all duration-200 
                            focus:outline-none focus:ring-4 focus:ring-green-300" type="submit">
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