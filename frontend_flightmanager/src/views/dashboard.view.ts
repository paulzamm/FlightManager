
export const DashboardView = {
    render: () => {
        // Retorna el HTML que se inyectará en #page-content
        return `
        <div class="bg-white p-6 rounded-lg shadow-lg">
            <h2 class="text-2xl font-bold mb-6 text-gray-800">Buscar Vuelos</h2>
            
            <form id="search-flight-form" class="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
            <div>
                <label for="origen" class="block text-sm font-medium text-gray-700">Origen (IATA)</label>
                <input type="text" id="origen" name="origen" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500" placeholder="Ej: UIO" required>
            </div>
            <div>
                <label for="destino" class="block text-sm font-medium text-gray-700">Destino (IATA)</label>
                <input type="text" id="destino" name="destino" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500" placeholder="Ej: GYE" required>
            </div>
            <div>
                <label for="fecha" class="block text-sm font-medium text-gray-700">Fecha</label>
                <input type="date" id="fecha" name="fecha" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500" required>
            </div>
            <button type="submit" class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded-lg">
                Buscar
            </button>
            </form>
            
            <div id="search-options" class="mt-4">
            </div>

            <div id="flight-results-container" class="mt-8">
            <p class="text-gray-500 text-center">Ingrese sus criterios de búsqueda.</p>
            </div>
        </div>
    `;
    },

    // Métodos para interactuar
    bindSearch: (handler: (e: SubmitEvent) => void) => {
        document.getElementById('search-flight-form')?.addEventListener('submit', handler);
    },

    showLoading: () => {
        const container = document.getElementById('flight-results-container');
        if (container) {
            container.innerHTML = `<p class="text-blue-500 text-center font-semibold">Buscando vuelos...</p>`;
        }
    },

    showError: (message: string) => {
        const container = document.getElementById('flight-results-container');
        if (container) {
            container.innerHTML = `<p class="text-red-500 text-center font-semibold">${message}</p>`;
        }
    }
};