import type { UserProfile, TarjetaSegura } from '../models/types';

export const ProfileView = {
    render: (profile: UserProfile, tarjetas: TarjetaSegura[]) => {
        return `
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            
            <div class="md:col-span-2 space-y-6">
            
            <form id="profile-form" class="bg-white p-8 rounded-xl shadow-2xl border border-gray-200">
                <h2 class="text-3xl font-bold text-gray-900 mb-2">Mi Perfil</h2>
                <p class="text-gray-600 text-sm mb-6">Actualiza tu información personal</p>
                <div id="profile-message" class="text-center mb-4 font-semibold"></div>
                <div class="space-y-6">
                <div>
                    <label class="block text-sm font-semibold text-gray-800 mb-2" for="profile-name">Nombre Completo</label>
                    <input type="text" id="profile-name" 
                           class="block w-full px-4 py-3 text-base border-2 border-gray-300 rounded-lg shadow-sm 
                                  bg-white placeholder-gray-400 
                                  focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 
                                  hover:border-indigo-300 transition-all duration-200" 
                           value="${profile.nombre_completo}">
                </div>
                <div>
                    <label class="block text-sm font-semibold text-gray-800 mb-2" for="profile-email">Email</label>
                    <input type="email" id="profile-email" 
                           class="block w-full px-4 py-3 text-base border-2 border-gray-300 rounded-lg shadow-sm 
                                  bg-white placeholder-gray-400 
                                  focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 
                                  hover:border-indigo-300 transition-all duration-200" 
                           value="${profile.email}">
                </div>
                <button type="submit" 
                        class="bg-gradient-to-r from-indigo-600 to-indigo-700 hover:from-indigo-700 hover:to-indigo-800 
                               text-white font-bold py-3 px-6 rounded-xl 
                               shadow-lg hover:shadow-xl transform hover:scale-[1.02] 
                               transition-all duration-200 
                               focus:outline-none focus:ring-4 focus:ring-indigo-300">
                    Guardar Cambios
                </button>
                </div>
            </form>
            
            <form id="password-form" class="bg-white p-8 rounded-xl shadow-2xl border border-gray-200">
                <h2 class="text-3xl font-bold text-gray-900 mb-2">Cambiar Contraseña</h2>
                <p class="text-gray-600 text-sm mb-6">Actualiza tu contraseña de acceso</p>
                <div id="password-message" class="text-center mb-4 font-semibold"></div>
                <div class="space-y-6">
                <div>
                    <label class="block text-sm font-semibold text-gray-800 mb-2" for="pass-current">Contraseña Actual</label>
                    <input type="password" id="pass-current" 
                           class="block w-full px-4 py-3 text-base border-2 border-gray-300 rounded-lg shadow-sm 
                                  bg-white placeholder-gray-400 
                                  focus:outline-none focus:ring-2 focus:ring-gray-500 focus:border-gray-500 
                                  hover:border-gray-300 transition-all duration-200" 
                           placeholder="Tu contraseña actual" required>
                </div>
                <div>
                    <label class="block text-sm font-semibold text-gray-800 mb-2" for="pass-new">Nueva Contraseña</label>
                    <input type="password" id="pass-new" 
                           class="block w-full px-4 py-3 text-base border-2 border-gray-300 rounded-lg shadow-sm 
                                  bg-white placeholder-gray-400 
                                  focus:outline-none focus:ring-2 focus:ring-gray-500 focus:border-gray-500 
                                  hover:border-gray-300 transition-all duration-200" 
                           placeholder="Mínimo 6 caracteres" required>
                </div>
                <button type="submit" 
                        class="bg-gradient-to-r from-gray-700 to-gray-800 hover:from-gray-800 hover:to-gray-900 
                               text-white font-bold py-3 px-6 rounded-xl 
                               shadow-lg hover:shadow-xl transform hover:scale-[1.02] 
                               transition-all duration-200 
                               focus:outline-none focus:ring-4 focus:ring-gray-300">
                    Actualizar Contraseña
                </button>
                </div>
            </form>
            
            </div>
            
            <div class="md:col-span-1 bg-white p-8 rounded-xl shadow-2xl border border-gray-200">
            <h2 class="text-3xl font-bold text-gray-900 mb-2">Mis Tarjetas</h2>
            <p class="text-gray-600 text-sm mb-6">Gestiona tus métodos de pago</p>
            <div id="cards-message" class="text-center mb-4 font-semibold"></div>
            <div id="cards-list" class="space-y-3 mb-6">
                ${tarjetas.map(t => `
                <div class="border-2 border-gray-300 rounded-xl p-4 flex justify-between items-center hover:border-indigo-400 transition-all duration-200 shadow-sm">
                    <div>
                    <p class="font-mono text-base font-bold text-gray-800">**** **** **** ${t.ultimos_4_digitos}</p>
                    <p class="text-sm text-gray-600 mt-1">${t.nombre_titular}</p>
                    ${t.es_predeterminada ? '<span class="text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full font-semibold inline-block mt-1">Predeterminada</span>' : ''}
                    </div>
                    <button class="btn-delete-card text-red-600 hover:text-red-800 font-semibold transition-colors" data-id="${t.id}">Eliminar</button>
                </div>
                `).join('')}
                ${tarjetas.length === 0 ? '<p class="text-gray-500 bg-gray-50 p-4 rounded-lg border-2 border-dashed border-gray-300 text-center">No tienes tarjetas guardadas</p>' : ''}
            </div>
            <form id="add-card-form" class="border-t-2 border-gray-200 pt-6 space-y-5">
                <h3 class="font-bold text-xl text-gray-900 mb-4">Añadir Nueva Tarjeta</h3>
                <div>
                    <label class="block text-sm font-semibold text-gray-800 mb-2" for="card-name-new">Nombre en la Tarjeta</label>
                    <input type="text" id="card-name-new" 
                           class="block w-full px-4 py-3 text-base border-2 border-gray-300 rounded-lg shadow-sm 
                                  bg-white placeholder-gray-400 
                                  focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 
                                  hover:border-blue-300 transition-all duration-200" 
                           placeholder="Ej: Juan Pérez" 
                           minlength="3"
                           maxlength="100"
                           required>
                </div>
                <div>
                    <label class="block text-sm font-semibold text-gray-800 mb-2" for="card-num-new">Número de Tarjeta (16 dígitos)</label>
                    <input type="text" id="card-num-new" 
                           class="block w-full px-4 py-3 text-base border-2 border-gray-300 rounded-lg shadow-sm 
                                  bg-white placeholder-gray-400 font-mono
                                  focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 
                                  hover:border-blue-300 transition-all duration-200" 
                           placeholder="1234567890123456" 
                           pattern="[0-9]{13,19}"
                           minlength="13"
                           maxlength="19"
                           title="Ingresa 13-19 dígitos sin espacios"
                           required>
                    <p class="text-xs text-gray-500 mt-1 italic">Solo números, sin espacios ni guiones</p>
                </div>
                <div>
                    <label class="block text-sm font-semibold text-gray-800 mb-2" for="card-exp-new">Fecha de Expiración (MM/YY)</label>
                    <input type="text" id="card-exp-new" 
                           class="block w-full px-4 py-3 text-base border-2 border-gray-300 rounded-lg shadow-sm 
                                  bg-white placeholder-gray-400 font-mono
                                  focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 
                                  hover:border-blue-300 transition-all duration-200" 
                           placeholder="12/25" 
                           pattern="^(0[1-9]|1[0-2])\\/[0-9]{2}$"
                           maxlength="5"
                           title="Formato: MM/YY (ej: 12/25)"
                           required>
                    <p class="text-xs text-gray-500 mt-1 italic">Formato: MM/YY (ej: 12/25)</p>
                </div>
                <button type="submit" 
                        class="w-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 
                               text-white font-bold py-3 px-6 rounded-xl text-base
                               shadow-lg hover:shadow-xl transform hover:scale-[1.02] 
                               transition-all duration-200 
                               focus:outline-none focus:ring-4 focus:ring-blue-300">
                    Añadir Tarjeta
                </button>
            </form>
            </div>
            
        </div>
    `;
    },

    // Binds
    bindUpdateProfile: (handler: (e: SubmitEvent) => void) => {
        document.getElementById('profile-form')?.addEventListener('submit', handler);
    },
    bindChangePassword: (handler: (e: SubmitEvent) => void) => {
        document.getElementById('password-form')?.addEventListener('submit', handler);
    },
    bindAddCard: (handler: (e: SubmitEvent) => void) => {
        document.getElementById('add-card-form')?.addEventListener('submit', handler);
    },
    bindDeleteCard: (handler: (id: number) => void) => {
        document.querySelectorAll('.btn-delete-card').forEach(btn => {
            btn.addEventListener('click', (e) => handler(Number((e.currentTarget as HTMLElement).dataset.id)));
        });
    },

    // Getters
    getProfileData: () => ({
        nombre: (document.getElementById('profile-name') as HTMLInputElement).value,
        email: (document.getElementById('profile-email') as HTMLInputElement).value,
    }),
    getPasswordData: () => ({
        actual: (document.getElementById('pass-current') as HTMLInputElement).value,
        nueva: (document.getElementById('pass-new') as HTMLInputElement).value,
    }),
    getNewCardData: () => ({
        nombre: (document.getElementById('card-name-new') as HTMLInputElement).value,
        numero: (document.getElementById('card-num-new') as HTMLInputElement).value,
        expiracion: (document.getElementById('card-exp-new') as HTMLInputElement).value,
    }),

    // Messages
    displayProfileMessage: (msg: string, isError: boolean) => {
        const el = document.getElementById('profile-message')!;
        el.textContent = msg;
        el.className = `text-center mb-4 ${isError ? 'text-red-500' : 'text-green-500'}`;
    },
    displayPasswordMessage: (msg: string, isError: boolean) => {
        const el = document.getElementById('password-message')!;
        el.textContent = msg;
        el.className = `text-center mb-4 ${isError ? 'text-red-500' : 'text-green-500'}`;
    },
    displayCardMessage: (msg: string, isError: boolean) => {
        const el = document.getElementById('cards-message')!;
        el.textContent = msg;
        el.className = `text-center mb-4 ${isError ? 'text-red-500' : 'text-green-500'}`;
    }
};