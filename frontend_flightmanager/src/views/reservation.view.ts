import type { BookingState } from '../models/types';

export const ReservationView = {
    render: (booking: BookingState) => {
        const { flight, selectedSeats } = booking;

        return `
        <div class="bg-white p-6 rounded-lg shadow-lg">
            <div class="flex justify-between items-center mb-4">
            <h2 class="text-2xl font-bold text-gray-800">Datos de los Pasajeros</h2>
            <a href="#/flight/${flight.id}" class="text-indigo-600 hover:text-indigo-800">&larr; Volver a Asientos</a>
            </div>
            
            <p class="mb-6 text-gray-600">Por favor, rellena la información para cada asiento seleccionado.</p>
            
            <form id="passengers-form" class="space-y-6">
            ${selectedSeats.map((seat, index) => `
                <fieldset class="border rounded-lg p-4" data-seat-id="${seat.id}">
                <legend class="text-lg font-semibold px-2">
                    Pasajero ${index + 1} (Asiento ${seat.numero_asiento} - ${seat.categoria})
                </legend>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                    <label class="block text-sm font-medium text-gray-700" for="name-${seat.id}">Nombre Completo</label>
                    <input type="text" id="name-${seat.id}" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm" required>
                    </div>
                    <div>
                    <label class="block text-sm font-medium text-gray-700" for="doc-${seat.id}">Documento (Pasaporte/Cédula)</label>
                    <input type="text" id="doc-${seat.id}" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm" required>
                    </div>
                </div>
                </fieldset>
            `).join('')}
            
            <div id="reservation-message" class="text-center text-red-500"></div>
            
            <div class="text-right border-t pt-4">
                <p class="text-2xl font-bold">Total: $${booking.selectedSeats.reduce((acc, s) => acc + flight.tarifa_base + s.precio_adicional, 0).toFixed(2)}</p>
                <button type="submit" id="btn-confirm-reservation" class="mt-4 bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-6 rounded-lg">
                Confirmar Reserva
                </button>
            </div>
            </form>
        </div>
    `;
    },

    bindConfirmReservation: (handler: (e: SubmitEvent) => void) => {
        document.getElementById('passengers-form')?.addEventListener('submit', handler);
    },

    getPassengerData: (): { id_asiento: number, nombre_completo: string, documento_identidad: string }[] => {
        const data: any[] = [];
        document.querySelectorAll('fieldset[data-seat-id]').forEach(field => {
            const seatId = Number((field as HTMLElement).dataset.seatId);
            const nombre = (document.getElementById(`name-${seatId}`) as HTMLInputElement).value;
            const doc = (document.getElementById(`doc-${seatId}`) as HTMLInputElement).value;
            data.push({
                id_asiento: seatId,
                nombre_completo: nombre,
                documento_identidad: doc,
            });
        });
        return data;
    },

    displayMessage: (message: string, isError: boolean) => {
        const el = document.getElementById('reservation-message') as HTMLDivElement;
        el.textContent = message;
        el.className = `text-center ${isError ? 'text-red-500' : 'text-green-500'}`;
    },

    setLoading: (isLoading: boolean) => {
        const btn = document.getElementById('btn-confirm-reservation') as HTMLButtonElement;
        if (isLoading) {
            btn.disabled = true;
            btn.innerHTML = 'Procesando...';
            btn.classList.add('opacity-70');
        } else {
            btn.disabled = false;
            btn.innerHTML = 'Confirmar Reserva';
            btn.classList.remove('opacity-70');
        }
    }
};