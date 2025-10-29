import type { FlightResult } from '../models/types';
import { format } from 'date-fns'; 
import { es } from 'date-fns/locale';

const formatDateTime = (iso: string) => format(new Date(iso), "PPpp", { locale: es });
const formatTime = (iso: string) => format(new Date(iso), "p", { locale: es });
const formatDate = (iso: string) => format(new Date(iso), "PP", { locale: es });

export const FlightResultsView = {
    /**
     * Renderiza vuelos según el tipo de consulta
     * @param flights - Lista de vuelos
     * @param viewType - 'horarios' | 'tarifas' | 'informacion' | 'browse'
     * @param flightClickHandler - Handler para seleccionar vuelo
     */
    render: (flights: FlightResult[], viewType: string, flightClickHandler: (flightId: number) => void) => {
        const container = document.getElementById('flight-results-container');
        if (!container) return;

        if (flights.length === 0) {
            container.innerHTML = `
                <div class="text-center py-8">
                    <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <p class="mt-2 text-gray-600 font-semibold">No se encontraron vuelos para esta ruta y fecha.</p>
                    <p class="text-sm text-gray-500">Intenta con otros criterios de búsqueda.</p>
                </div>
            `;
            return;
        }

        let headerText = '';
        switch(viewType) {
            case 'horarios':
                headerText = '📅 Vuelos Ordenados por Horario';
                break;
            case 'tarifas':
                headerText = '💰 Vuelos Ordenados por Precio (Menor a Mayor)';
                break;
            case 'informacion':
                headerText = 'ℹ️ Información de Vuelos de Hoy';
                break;
            case 'browse':
                headerText = '✈️ Vuelos Disponibles';
                break;
        }

        container.innerHTML = `
        <div class="flex justify-between items-center mb-4">
            <h3 class="text-xl font-semibold text-gray-800">${headerText}</h3>
            <span class="text-sm text-gray-600">${flights.length} vuelo(s) encontrado(s)</span>
        </div>
        <div class="space-y-4">
            ${flights.map(flight => FlightResultsView.renderFlightCard(flight, viewType)).join('')}
        </div>
    `;

        // Bind Clicks
        container.querySelectorAll('button[data-flight-id]').forEach(button => {
            button.addEventListener('click', (e) => {
                const id = (e.currentTarget as HTMLElement).dataset.flightId;
                flightClickHandler(Number(id));
            });
        });
    },

    /**
     * Renderiza múltiples tarjetas de vuelo (usado para paginación)
     */
    renderFlightCards: (flights: FlightResult[], viewType: string): string => {
        if (flights.length === 0) {
            return `
                <div class="text-center py-8">
                    <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <p class="mt-2 text-gray-600 font-semibold">No se encontraron vuelos.</p>
                </div>
            `;
        }

        return `
        <div class="space-y-4">
            ${flights.map(flight => FlightResultsView.renderFlightCard(flight, viewType)).join('')}
        </div>
        `;
    },

    /**
     * Bind para selección de vuelos (usado con renderFlightCards)
     */
    bindFlightSelection: (handler: (flightId: number) => void) => {
        document.querySelectorAll('button[data-flight-id]').forEach(button => {
            button.addEventListener('click', (e) => {
                const id = (e.currentTarget as HTMLElement).dataset.flightId;
                if (id) handler(Number(id));
            });
        });
    },

    renderFlightCard: (flight: FlightResult, viewType: string): string => {
        // Calcular asientos disponibles (si existe en el objeto)
        const asientosDisponibles = (flight as any).asientos_disponibles || 20; // Fallback a 20
        const estadoVuelo = asientosDisponibles > 10 ? 'Disponible' : asientosDisponibles > 0 ? 'Pocas plazas' : 'Agotado';
        const colorEstado = asientosDisponibles > 10 ? 'text-green-600' : asientosDisponibles > 0 ? 'text-yellow-600' : 'text-red-600';

        return `
        <div class="bg-white rounded-lg shadow-md hover:shadow-xl transition-all duration-200 p-6">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center space-y-4 md:space-y-0">
                
                <!-- Información de la aerolínea -->
                <div class="flex items-center space-x-4">
                    <div class="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center">
                        <span class="text-indigo-600 font-bold text-lg">${flight.aerolinea.nombre.substring(0, 2)}</span>
                    </div>
                    <div>
                        <div class="text-lg font-bold text-gray-900">${flight.aerolinea.nombre}</div>
                        <div class="text-sm text-gray-500">Vuelo ${flight.numero_vuelo}</div>
                        ${viewType === 'informacion' ? `<div class="text-xs ${colorEstado} font-semibold">${estadoVuelo}</div>` : ''}
                    </div>
                </div>
                
                <!-- Ruta y horarios -->
                <div class="flex items-center space-x-6 flex-1 justify-center">
                    <div class="text-center">
                        <div class="text-2xl font-bold text-gray-800">${flight.origen.codigo_iata}</div>
                        <div class="text-sm font-semibold text-indigo-700">${formatTime(flight.hora_salida)}</div>
                        <div class="text-xs text-gray-600 font-medium mt-1">${formatDate(flight.hora_salida)}</div>
                        <div class="text-xs text-gray-500">${flight.origen.ciudad}</div>
                    </div>
                    
                    <div class="text-center text-gray-400">
                        <svg class="h-8 w-8 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
                        </svg>
                        <div class="text-xs mt-1">Directo</div>
                    </div>
                    
                    <div class="text-center">
                        <div class="text-2xl font-bold text-gray-800">${flight.destino.codigo_iata}</div>
                        <div class="text-sm font-semibold text-indigo-700">${formatTime(flight.hora_llegada)}</div>
                        <div class="text-xs text-gray-600 font-medium mt-1">${formatDate(flight.hora_llegada)}</div>
                        <div class="text-xs text-gray-500">${flight.destino.ciudad}</div>
                    </div>
                </div>
                
                <!-- Precio y acción -->
                <div class="text-right">
                    ${viewType === 'tarifas' ? `
                        <div class="mb-1">
                            <span class="text-xs text-gray-500">Desde</span>
                        </div>
                    ` : ''}
                    <div class="text-3xl font-bold text-green-600">$${Number(flight.tarifa_base).toFixed(2)}</div>
                    <div class="text-xs text-gray-500 mb-2">Tarifa base</div>
                    ${viewType === 'informacion' ? `
                        <div class="text-sm mb-2">
                            <span class="text-gray-600">Asientos: </span>
                            <span class="font-semibold ${colorEstado}">${asientosDisponibles}</span>
                        </div>
                    ` : ''}
                    <button 
                        class="w-full md:w-auto bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-6 rounded-lg transition-colors ${asientosDisponibles === 0 ? 'opacity-50 cursor-not-allowed' : ''}" 
                        data-flight-id="${flight.id}"
                        ${asientosDisponibles === 0 ? 'disabled' : ''}
                    >
                        ${asientosDisponibles === 0 ? 'No disponible' : 'Seleccionar'}
                    </button>
                </div>
                
            </div>
        </div>
        `;
    }
};