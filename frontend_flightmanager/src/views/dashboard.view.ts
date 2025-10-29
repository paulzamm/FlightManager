
export const DashboardView = {
    render: () => {
        const today = new Date().toISOString().split('T')[0];
        const maxDate = new Date();
        maxDate.setDate(maxDate.getDate() + 30);
        const maxDateStr = maxDate.toISOString().split('T')[0];
        
        return `
        <div class="bg-white p-6 rounded-lg shadow-lg">
            <h2 class="text-2xl font-bold mb-6 text-gray-800">Vuelos Disponibles</h2>
            
            <!-- Formulario de filtros -->
            <form id="filter-flights-form" class="mb-6">
                <div class="grid grid-cols-1 md:grid-cols-5 gap-4 mb-4">
                    <div>
                        <label for="origen" class="block text-sm font-medium text-gray-700">Origen (IATA)</label>
                        <input type="text" id="origen" name="origen" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500" placeholder="Ej: UIO">
                        <p class="text-xs text-gray-500 mt-1">Opcional</p>
                    </div>
                    <div>
                        <label for="destino" class="block text-sm font-medium text-gray-700">Destino (IATA)</label>
                        <input type="text" id="destino" name="destino" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500" placeholder="Ej: GYE">
                        <p class="text-xs text-gray-500 mt-1">Opcional</p>
                    </div>
                    <div>
                        <label for="fecha_desde" class="block text-sm font-medium text-gray-700">Desde</label>
                        <input type="date" id="fecha_desde" name="fecha_desde" value="${today}" min="${today}" max="${maxDateStr}" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                    </div>
                    <div>
                        <label for="fecha_hasta" class="block text-sm font-medium text-gray-700">Hasta</label>
                        <input type="date" id="fecha_hasta" name="fecha_hasta" value="${maxDateStr}" min="${today}" max="${maxDateStr}" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                    </div>
                    <div>
                        <label for="aerolinea" class="block text-sm font-medium text-gray-700">Aerolínea</label>
                        <input type="text" id="aerolinea" name="aerolinea" placeholder="Ej: LATAM" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                        <p class="text-xs text-gray-500 mt-1">Opcional</p>
                    </div>
                </div>

                <!-- Filtros avanzados -->
                <div class="border rounded-lg p-4 bg-gray-50 mb-4">
                    <button type="button" id="toggle-filters" class="flex items-center justify-between w-full text-left font-medium text-gray-700">
                        <span>Opciones de Ordenamiento</span>
                        <span id="filter-icon">▼</span>
                    </button>
                    <div id="advanced-filters" class="mt-4 hidden">
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                            <div>
                                <label for="ordenar_por" class="block text-sm font-medium text-gray-700">Ordenar por</label>
                                <select id="ordenar_por" name="ordenar_por" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm">
                                    <option value="fecha">Fecha y Hora</option>
                                    <option value="precio">Precio (Menor a Mayor)</option>
                                    <option value="aerolinea">Aerolinea (A-Z)</option>
                                </select>
                            </div>
                            <div>
                                <label for="resultados_por_pagina" class="block text-sm font-medium text-gray-700">Resultados por página</label>
                                <select id="resultados_por_pagina" name="resultados_por_pagina" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm">
                                    <option value="10" selected>10</option>
                                    <option value="20">20</option>
                                    <option value="50">50</option>
                                    <option value="100">100</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="flex gap-2">
                    <button type="submit" class="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-4 rounded-lg text-lg transition-colors">
                        Aplicar Filtros
                    </button>
                    <button type="button" id="btn-reset-filters" class="bg-gray-500 hover:bg-gray-600 text-white font-bold py-3 px-4 rounded-lg transition-colors">
                        Limpiar
                    </button>
                </div>
            </form>

            <!-- Contador de resultados -->
            <div id="results-info" class="mb-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
                <p class="text-blue-800 font-medium text-center">Cargando vuelos disponibles...</p>
            </div>

            <!-- Contenedor de resultados con paginación -->
            <div id="flight-results-container" class="mt-6">
                <p class="text-gray-500 text-center">Cargando vuelos...</p>
            </div>

            <!-- Paginación -->
            <div id="pagination-container" class="mt-6 flex justify-center gap-2">
            </div>
        </div>
    `;
    },

    // Métodos para interactuar
    bindFilterSubmit: (handler: (e: SubmitEvent) => void) => {
        document.getElementById('filter-flights-form')?.addEventListener('submit', handler);
    },

    bindResetFilters: (handler: () => void) => {
        document.getElementById('btn-reset-filters')?.addEventListener('click', handler);
    },

    bindToggleFilters: () => {
        document.getElementById('toggle-filters')?.addEventListener('click', () => {
            const filters = document.getElementById('advanced-filters');
            const icon = document.getElementById('filter-icon');
            if (filters && icon) {
                filters.classList.toggle('hidden');
                icon.textContent = filters.classList.contains('hidden') ? '▼' : '▲';
            }
        });
    },

    showLoading: () => {
        const container = document.getElementById('flight-results-container');
        if (container) {
            container.innerHTML = `
                <div class="text-center py-12">
                    <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
                    <p class="mt-4 text-gray-600 font-semibold">Cargando vuelos...</p>
                </div>
            `;
        }
    },

    showError: (message: string) => {
        const container = document.getElementById('flight-results-container');
        if (container) {
            container.innerHTML = `
                <div class="text-center py-12">
                    <svg class="mx-auto h-12 w-12 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <p class="mt-4 text-red-600 font-semibold">❌ ${message}</p>
                </div>
            `;
        }
    },

    updateResultsInfo: (total: number, showing: number, page: number, totalPages: number) => {
        const container = document.getElementById('results-info');
        if (container) {
            container.innerHTML = `
                <p class="text-blue-800 font-medium text-center">
                    Mostrando ${showing} de ${total} vuelos disponibles 
                    <span class="text-sm">(Página ${page} de ${totalPages})</span>
                </p>
            `;
        }
    },

    renderPagination: (currentPage: number, totalPages: number, onPageChange: (page: number) => void) => {
        const container = document.getElementById('pagination-container');
        if (!container || totalPages <= 1) {
            if (container) container.innerHTML = '';
            return;
        }

        let html = '';
        
        // Botón anterior
        if (currentPage > 1) {
            html += `<button data-page="${currentPage - 1}" class="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-lg font-medium">← Anterior</button>`;
        }

        // Números de página (mostrar máximo 5)
        const startPage = Math.max(1, currentPage - 2);
        const endPage = Math.min(totalPages, currentPage + 2);

        if (startPage > 1) {
            html += `<button data-page="1" class="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-lg font-medium">1</button>`;
            if (startPage > 2) html += `<span class="px-2">...</span>`;
        }

        for (let i = startPage; i <= endPage; i++) {
            const isActive = i === currentPage;
            html += `<button data-page="${i}" class="px-4 py-2 ${isActive ? 'bg-indigo-600 text-white' : 'bg-gray-200 hover:bg-gray-300'} rounded-lg font-medium">${i}</button>`;
        }

        if (endPage < totalPages) {
            if (endPage < totalPages - 1) html += `<span class="px-2">...</span>`;
            html += `<button data-page="${totalPages}" class="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-lg font-medium">${totalPages}</button>`;
        }

        // Botón siguiente
        if (currentPage < totalPages) {
            html += `<button data-page="${currentPage + 1}" class="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-lg font-medium">Siguiente →</button>`;
        }

        container.innerHTML = html;

        // Bind eventos
        container.querySelectorAll('button[data-page]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const page = Number((e.currentTarget as HTMLElement).dataset.page);
                onPageChange(page);
            });
        });
    },

    getFilters: () => {
        const form = document.getElementById('filter-flights-form') as HTMLFormElement;
        const formData = new FormData(form);
        return {
            origen: (formData.get('origen') as string)?.trim() || undefined,
            destino: (formData.get('destino') as string)?.trim() || undefined,
            fecha_desde: formData.get('fecha_desde') as string,
            fecha_hasta: formData.get('fecha_hasta') as string,
            aerolinea: (formData.get('aerolinea') as string)?.trim() || undefined,
            ordenar_por: (formData.get('ordenar_por') as string) || 'fecha',
            limit: Number(formData.get('resultados_por_pagina')) || 20
        };
    },

    resetFilters: () => {
        const form = document.getElementById('filter-flights-form') as HTMLFormElement;
        form.reset();
        const today = new Date().toISOString().split('T')[0];
        const maxDate = new Date();
        maxDate.setDate(maxDate.getDate() + 30);
        (document.getElementById('fecha_desde') as HTMLInputElement).value = today;
        (document.getElementById('fecha_hasta') as HTMLInputElement).value = maxDate.toISOString().split('T')[0];
    }
};