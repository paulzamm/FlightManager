import type { FlightResult } from '../models/types';
import { format } from 'date-fns'; 
import { es } from 'date-fns/locale';

const formatDateTime = (iso: string) => format(new Date(iso), "PPpp", { locale: es });
const formatTime = (iso: string) => format(new Date(iso), "p", { locale: es });

export const FlightResultsView = {
    render: (flights: FlightResult[], flightClickHandler: (flightId: number) => void) => {
        const container = document.getElementById('flight-results-container');
        if (!container) return;

        if (flights.length === 0) {
            container.innerHTML = `<p class="text-gray-600 text-center font-semibold">No se encontraron vuelos para esta ruta y fecha.</p>`;
            return;
        }

        container.innerHTML = `
        <h3 class="text-xl font-semibold mb-4 text-gray-800">Vuelos Encontrados</h3>
        <div class="space-y-4">
            ${flights.map(flight => `
            <div class="bg-white p-4 rounded-lg shadow-md flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
                
                <div class="flex items-center space-x-4">
                <img src="https://logo.clearbit.com/${flight.aerolinea.nombre.toLowerCase().replace(/\s/g, '')}.com" alt="${flight.aerolinea.nombre}" class="h-10 w-10 rounded-full bg-gray-200" onerror="this.style.display='none'">
                <div>
                    <div class="text-lg font-bold text-gray-900">${flight.aerolinea.nombre}</div>
                    <div class="text-sm text-gray-500">Vuelo ${flight.numero_vuelo}</div>
                </div>
                </div>
                
                <div class="text-center">
                <div class="text-xl font-bold text-gray-800">${flight.origen.codigo_iata}</div>
                <div class="text-sm text-gray-600">${formatTime(flight.hora_salida)}</div>
                <div class="text-xs text-gray-500">${flight.origen.ciudad}</div>
                </div>
                
                <div class="text-center text-gray-500">
                <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path></svg>
                </div>
                
                <div class="text-center">
                <div class="text-xl font-bold text-gray-800">${flight.destino.codigo_iata}</div>
                <div class="text-sm text-gray-600">${formatTime(flight.hora_llegada)}</div>
                <div class="text-xs text-gray-500">${flight.destino.ciudad}</div>
                </div>
                
                <div class="text-right">
                <div class="text-2xl font-bold text-green-600">$${flight.tarifa_base.toFixed(2)}</div>
                <button class="mt-1 w-full md:w-auto bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded-lg" data-flight-id="${flight.id}">
                    Seleccionar Asientos
                </button>
                </div>
                
            </div>
            `).join('')}
        </div>
    `;

        // Bind Clicks
        container.querySelectorAll('button[data-flight-id]').forEach(button => {
            button.addEventListener('click', (e) => {
                const id = (e.currentTarget as HTMLElement).dataset.flightId;
                flightClickHandler(Number(id));
            });
        });
    }
};