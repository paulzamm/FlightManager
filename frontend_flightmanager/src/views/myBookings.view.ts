import type { ReservaDetail, BilleteResponse } from '../models/types';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';

export const MyBookingsView = {
    render: () => {
        return `
        <div class="space-y-8">
            <div class="bg-white p-6 rounded-lg shadow-lg">
            <h2 class="text-2xl font-bold text-gray-800 mb-4">Reservas Pendientes de Pago</h2>
            <div id="pending-reservations-list" class="space-y-4">
                </div>
            </div>
            
            <div class="bg-white p-6 rounded-lg shadow-lg">
            <h2 class="text-2xl font-bold text-gray-800 mb-4">Mis Billetes Comprados</h2>
            <div id="confirmed-tickets-list" class="space-y-4">
                </div>
            </div>
        </div>
    `;
    },

    renderPending: (reservas: ReservaDetail[], payHandler: (id: number) => void, cancelHandler: (id: number) => void) => {
        const container = document.getElementById('pending-reservations-list')!;
        if (reservas.length === 0) {
            container.innerHTML = `<p class="text-gray-500">No tienes reservas pendientes.</p>`;
            return;
        }
        container.innerHTML = reservas.map(r => `
        <div class="border rounded-lg p-4 flex justify-between items-center">
            <div>
            <p class="font-bold text-lg">Reserva #${r.id}</p>
            <p class="text-sm text-gray-600">Creada: ${format(new Date(r.fecha_reserva), "PPp", { locale: es })}</p>
            <p class="text-sm text-gray-600">${r.pasajeros.length} pasajero(s)</p>
            <p class="text-lg font-semibold text-green-600">Total: $${r.monto_total.toFixed(2)}</p>
            </div>
            <div class="flex space-x-2">
            <button class="btn-cancel bg-red-100 text-red-700 hover:bg-red-200" data-id="${r.id}">Cancelar</button>
            <button class="btn-pay bg-green-500 text-white hover:bg-green-600" data-id="${r.id}">Pagar Ahora</button>
            </div>
        </div>
    `).join('');

        // Binds
        container.querySelectorAll('.btn-pay').forEach(btn => btn.addEventListener('click', (e) => payHandler(Number((e.currentTarget as HTMLElement).dataset.id))));
        container.querySelectorAll('.btn-cancel').forEach(btn => btn.addEventListener('click', (e) => cancelHandler(Number((e.currentTarget as HTMLElement).dataset.id))));
    },

    renderConfirmed: (billetes: BilleteResponse[]) => {
        const container = document.getElementById('confirmed-tickets-list')!;
        if (billetes.length === 0) {
            container.innerHTML = `<p class="text-gray-500">No tienes billetes comprados.</p>`;
            return;
        }
        container.innerHTML = billetes.map(b => `
        <div class="border rounded-lg p-4 flex justify-between items-center">
            <div>
            <p class="font-bold text-lg text-indigo-600">Código: ${b.codigo_confirmacion}</p>
            <p class="text-sm text-gray-600">Comprado: ${format(new Date(b.fecha_compra), "PPp", { locale: es })}</p>
            <p class="text-sm text-gray-600">Reserva ID: #${b.id_reserva}</p>
            </div>
            <button class="btn-view-ticket bg-blue-500 text-white hover:bg-blue-600" data-code="${b.codigo_confirmacion}">Ver Detalles</button>
        </div>
    `).join('');
        // TODO: Bind click para ver detalles del billete
    }
};