// frontend_flightmanager/src/views/Layout.view.ts
import { store } from '../models/store';

export const LayoutView = {
    render: () => {
        const user = store.getUser();
        const appElement = document.getElementById('app') as HTMLDivElement;

        appElement.innerHTML = `
        <div class="flex h-screen bg-gray-100 font-sans">

            <aside class="w-64 bg-gray-900 text-gray-200 shrink-0">
            <div class="p-6 text-2xl font-bold text-white border-b border-gray-700 flex items-center">
                <!-- Ícono de avión SVG -->
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-8 h-8 mr-2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 12 3.269 3.125A59.769 59.769 0 0 1 21.485 12 59.768 59.768 0 0 1 3.27 20.875L5.999 12Zm0 0h7.5" />
                </svg>
                FlightManager
            </div>
            <nav class="mt-6">
                <a href="#/search" class="nav-link" data-route="/search">
                <!-- Ícono de búsqueda SVG -->
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 mr-3">
                    <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
                </svg>
                Buscar Vuelos
                </a>
                <a href="#/bookings" class="nav-link" data-route="/bookings">
                <!-- Ícono de ticket SVG -->
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 mr-3">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 6v.75m0 3v.75m0 3v.75m0 3V18m-9-1.5h5.25m-7.5 0h7.5m-7.5 0h7.5M3 12.75h7.5m-7.5 0h7.5m-7.5-3h7.5m-7.5-3h7.5m-7.5-3h7.5M6.75 6v.75m0 3v.75m0 3v.75m0 3V18m2.25-15H18a2.25 2.25 0 0 1 2.25 2.25v13.5A2.25 2.25 0 0 1 18 21H6a2.25 2.25 0 0 1-2.25-2.25V5.25A2.25 2.25 0 0 1 6 3Z" />
                </svg>
                Mis Viajes
                </a>
                <a href="#/profile" class="nav-link" data-route="/profile">
                <!-- Ícono de usuario SVG -->
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 mr-3">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z" />
                </svg>
                Mi Perfil
                </a>
            </nav>
            </aside>

            <div class="flex-1 flex flex-col overflow-hidden">

            <header class="bg-white shadow-md p-4 flex justify-between items-center z-10">
                <h1 id="page-title" class="text-xl font-semibold text-gray-800">Dashboard</h1>
                <div class="flex items-center">
                <span class="text-gray-600 mr-4">Hola, ${user?.nombre_completo || 'Usuario'}</span>
                <button id="logout-button" class="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded-lg transition duration-200 flex items-center">
                    <!-- Ícono de logout SVG -->
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 mr-2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0 0 13.5 3h-6a2.25 2.25 0 0 0-2.25 2.25v13.5A2.25 2.25 0 0 0 7.5 21h6a2.25 2.25 0 0 0 2.25-2.25V15M12 9l-3 3m0 0 3 3m-3-3h12.75" />
                    </svg>
                    Cerrar Sesión
                </button>
                </div>
            </header>

            <main class="flex-1 overflow-x-hidden overflow-y-auto bg-gray-200 p-6">
                <div id="page-content">
                <p>Cargando contenido...</p>
                </div>
            </main>

            </div>
        </div>

        <style>
            .nav-link {
            display: flex; /* Cambiado a flex */
            align-items: center; /* Alinea ícono y texto verticalmente */
            padding: 0.75rem 1.5rem;
            margin: 0.25rem 0.5rem;
            border-radius: 0.5rem;
            color: #D1D5DB; /* text-gray-300 */
            font-weight: 500;
            transition: background-color 0.2s, color 0.2s;
            }
            .nav-link:hover {
            background-color: #374151; /* bg-gray-700 */
            color: white;
            }
            .nav-link.active {
            background-color: #4F46E5; /* bg-indigo-600 */
            color: white;
            }
        </style>
    `;
    },

    // ... (resto de los métodos: renderPageContent, updateActiveLink, bindLogout)
    renderPageContent: (title: string, htmlContent: string) => {
        (document.getElementById('page-title') as HTMLHeadingElement).innerText = title;
        (document.getElementById('page-content') as HTMLDivElement).innerHTML = htmlContent;
    },
    updateActiveLink: (path: string) => {
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
            const route = (link as HTMLElement).dataset.route;
            // Ajusta la lógica para que coincida con la ruta base
            const routeBase = route?.split('/:')[0]; // Ej: '/flight' de '/flight/:id'
            if (route && path.startsWith(routeBase || route)) {
                link.classList.add('active');
            }
            // Caso especial para la ruta raíz o login si es necesario
            if (path === '/' || path === '/login') {
                // Podrías resaltar 'Buscar Vuelos' por defecto o ninguno
            }
        });
    },
    bindLogout: (handler: () => void) => {
        document.getElementById('logout-button')?.addEventListener('click', handler);
    }
};