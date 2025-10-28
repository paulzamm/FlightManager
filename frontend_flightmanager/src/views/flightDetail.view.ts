import type { FlightResult, AsientoResponse } from '../models/types';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';

const formatDateTime = (iso: string) => format(new Date(iso), "PPpp", { locale: es });

export const FlightDetailView = {
    render: (flight: FlightResult, seats: AsientoResponse[]) => {
        const seatCategories = {
            Economica: seats.filter(s => s.categoria === 'Economica'),
            Business: seats.filter(s => s.categoria === 'Business'),
            PrimeraClase: seats.filter(s => s.categoria === 'PrimeraClase'),
        };

        return `
        <div class="bg-white p-6 rounded-lg shadow-lg mb-6">
            <div class="flex justify-between items-center mb-4">
            <div>
                <h2 class="text-2xl font-bold text-gray-800">${flight.aerolinea.nombre} - ${flight.numero_vuelo}</h2>
                <p class="text-lg text-gray-600">${flight.origen.ciudad} (${flight.origen.codigo_iata}) a ${flight.destino.ciudad} (${flight.destino.codigo_iata})</p>
            </div>
            <a href="#/search" class="text-indigo-600 hover:text-indigo-800">&larr; Volver a la búsqueda</a>
            </div>
            <p class="text-gray-700"><strong>Salida:</strong> ${formatDateTime(flight.hora_salida)}</p>
            <p class="text-gray-700"><strong>Llegada:</strong> ${formatDateTime(flight.hora_llegada)}</p>
            <p class="text-gray-700"><strong>Tarifa Base:</strong> <span class="font-bold text-green-600">$${flight.tarifa_base.toFixed(2)}</span></p>
        </div>
        
        <div class="bg-white p-6 rounded-lg shadow-lg">
            <h3 class="text-xl font-bold mb-4">Selecciona tus Asientos</h3>
            <div id="seat-map-container" class="space-y-6">
            ${Object.entries(seatCategories).map(([categoria, asientos]) =>
                asientos.length > 0 ? `
                <div>
                    <h4 class="text-lg font-semibold border-b pb-2 mb-3">${categoria} (+ $${Number(asientos[0].precio_adicional).toFixed(2)})</h4>
                    <div class="grid grid-cols-6 gap-2">
                    ${asientos.map(asiento => `
                        <button 
                        class="seat-button ${asiento.estado === 'Disponible' ? 'bg-blue-100 hover:bg-blue-300' : 'bg-gray-300 cursor-not-allowed'}"
                        data-seat-id="${asiento.id}"
                        data-seat-info='${JSON.stringify(asiento)}'
                        ${asiento.estado !== 'Disponible' ? 'disabled' : ''}
                        title="${asiento.estado}">
                        ${asiento.numero_asiento}
                        </button>
                    `).join('')}
                    </div>
                </div>
                ` : ''
            ).join('')}
            </div>
            
            <div id="selection-summary" class="mt-6 border-t pt-4 text-right">
            <p class="text-lg">Asientos seleccionados: <span id="selected-count" class="font-bold">0</span></p>
            <p class="text-xl">Total: <span id="selected-total" class="font-bold text-green-700">$0.00</span></p>
            <button id="btn-goto-passengers" class="mt-4 bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-lg opacity-50 cursor-not-allowed" disabled>
                Añadir Pasajeros
            </button>
            </div>
        </div>
        
        <style>
            .seat-button {
            border: 1px solid #B0B0B0;
            border-radius: 0.25rem;
            padding: 0.5rem;
            text-align: center;
            font-family: monospace;
            font-size: 0.875rem;
            transition: all 0.2s;
            }
            .seat-button.selected {
            background-color: #3B82F6 !important; /* bg-blue-500 */
            color: white;
            font-weight: bold;
            }
        </style>
    `;
    },

    // Métodos de la vista...
    bindSeatSelection: (handler: (seat: AsientoResponse, el: HTMLElement) => void) => {
        document.querySelectorAll('.seat-button[data-seat-id]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const el = e.currentTarget as HTMLElement;
                const seatData = JSON.parse(el.dataset.seatInfo || '{}');
                handler(seatData, el);
            });
        });
    },

    updateSummary: (count: number, total: number) => {
        (document.getElementById('selected-count') as HTMLSpanElement).innerText = count.toString();
        (document.getElementById('selected-total') as HTMLSpanElement).innerText = `$${total.toFixed(2)}`;

        const btn = document.getElementById('btn-goto-passengers') as HTMLButtonElement;
        if (count > 0) {
            btn.disabled = false;
            btn.classList.remove('opacity-50', 'cursor-not-allowed');
        } else {
            btn.disabled = true;
            btn.classList.add('opacity-50', 'cursor-not-allowed');
        }
    },

    bindContinueToPassengers: (handler: () => void) => {
        document.getElementById('btn-goto-passengers')?.addEventListener('click', handler);
    }
};