import type { UserProfile, TarjetaSegura } from '../models/types';

export const ProfileView = {
    render: (profile: UserProfile, tarjetas: TarjetaSegura[]) => {
        return `
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            
            <div class="md:col-span-2 space-y-6">
            
            <form id="profile-form" class="bg-white p-6 rounded-lg shadow-lg">
                <h2 class="text-2xl font-bold text-gray-800 mb-4">Mi Perfil</h2>
                <div id="profile-message" class="text-center mb-4"></div>
                <div class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700" for="profile-name">Nombre Completo</label>
                    <input type="text" id="profile-name" class="mt-1 block w-full rounded-md border-gray-300" value="${profile.nombre_completo}">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700" for="profile-email">Email</label>
                    <input type="email" id="profile-email" class="mt-1 block w-full rounded-md border-gray-300" value="${profile.email}">
                </div>
                <button type="submit" class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded-lg">Guardar Cambios</button>
                </div>
            </form>
            
            <form id="password-form" class="bg-white p-6 rounded-lg shadow-lg">
                <h2 class="text-2xl font-bold text-gray-800 mb-4">Cambiar Contraseña</h2>
                <div id="password-message" class="text-center mb-4"></div>
                <div class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700" for="pass-current">Contraseña Actual</label>
                    <input type="password" id="pass-current" class="mt-1 block w-full rounded-md border-gray-300" required>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700" for="pass-new">Nueva Contraseña</label>
                    <input type="password" id="pass-new" class="mt-1 block w-full rounded-md border-gray-300" required>
                </div>
                <button type="submit" class="bg-gray-700 hover:bg-gray-800 text-white font-bold py-2 px-4 rounded-lg">Actualizar Contraseña</button>
                </div>
            </form>
            
            </div>
            
            <div class="md:col-span-1 bg-white p-6 rounded-lg shadow-lg">
            <h2 class="text-2xl font-bold text-gray-800 mb-4">Mis Tarjetas</h2>
            <div id="cards-message" class="text-center mb-4"></div>
            <div id="cards-list" class="space-y-3">
                ${tarjetas.map(t => `
                <div class="border rounded-lg p-3 flex justify-between items-center">
                    <div>
                    <p class="font-mono text-sm">**** ${t.ultimos_4_digitos}</p>
                    <p class="text-xs text-gray-500">${t.nombre_titular} ${t.es_predeterminada ? '(Predeterminada)' : ''}</p>
                    </div>
                    <button class="btn-delete-card text-red-500 hover:text-red-700 text-sm" data-id="${t.id}">Eliminar</button>
                </div>
                `).join('')}
                ${tarjetas.length === 0 ? '<p class="text-gray-500">No tienes tarjetas.</p>' : ''}
            </div>
            <form id="add-card-form" class="mt-6 border-t pt-4 space-y-3">
                <h3 class_="font-semibold">Añadir Tarjeta</h3>
                <input type="text" id="card-name-new" placeholder="Nombre" class="block w-full rounded-md border-gray-300 text-sm" required>
                <input type="text" id="card-num-new" placeholder="Número Tarjeta" class="block w-full rounded-md border-gray-300 text-sm" required>
                <input type="text" id="card-exp-new" placeholder="MM/YY" class="block w-full rounded-md border-gray-300 text-sm" required>
                <button type="submit" class="w-full bg-blue-500 hover:bg-blue-700 text-white py-2 rounded-lg text-sm">Añadir</button>
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