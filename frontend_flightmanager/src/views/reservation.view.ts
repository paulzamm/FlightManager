import type { BookingState } from '../models/types';

export const ReservationView = {
    render: (booking: BookingState) => {
        const { flight, selectedSeats } = booking;

        return `
        <div class="bg-white p-8 rounded-xl shadow-2xl border border-gray-200">
            <div class="flex justify-between items-center mb-6 pb-4 border-b-2 border-gray-200">
            <div>
                <h2 class="text-3xl font-bold text-gray-900">Datos de los Pasajeros</h2>
                <p class="text-gray-600 text-sm mt-1">Completa la información para cada pasajero</p>
            </div>
            <a href="#/flight/${flight.id}" class="text-indigo-600 hover:text-indigo-800 font-semibold transition-colors">&larr; Volver a Asientos</a>
            </div>
            
            <form id="passengers-form" class="space-y-6">
            ${selectedSeats.map((seat, index) => `
                <fieldset class="border-2 border-gray-200 rounded-xl p-6 bg-gradient-to-r from-gray-50 to-gray-100 shadow-sm" data-seat-id="${seat.id}">
                <legend class="text-lg font-bold text-gray-900 px-4 bg-white rounded-lg border-2 border-indigo-200">
                    Pasajero ${index + 1} | Asiento ${seat.numero_asiento} - ${seat.categoria}
                </legend>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-4">
                    <div>
                    <label class="block text-sm font-semibold text-gray-800 mb-2" for="name-${seat.id}">Nombre Completo</label>
                    <input type="text" id="name-${seat.id}" 
                           class="block w-full px-4 py-3 text-base border-2 border-gray-300 rounded-lg shadow-sm 
                                  bg-white placeholder-gray-400 
                                  focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 
                                  hover:border-indigo-300 transition-all duration-200"
                           placeholder="Ej: Juan Pérez García" required>
                    </div>
                    <div>
                    <label class="block text-sm font-semibold text-gray-800 mb-2" for="doc-${seat.id}">Documento (Pasaporte/Cédula)</label>
                    <input type="text" id="doc-${seat.id}" 
                           class="block w-full px-4 py-3 text-base border-2 border-gray-300 rounded-lg shadow-sm 
                                  bg-white placeholder-gray-400 
                                  focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 
                                  hover:border-indigo-300 transition-all duration-200"
                           placeholder="Ej: 1234567890 o ABC123456" required>
                    </div>
                </div>
                </fieldset>
            `).join('')}
            
            <div id="reservation-message" class="text-center font-semibold text-base"></div>
            
            <div class="border-t-2 border-gray-200 pt-6 mt-8">
                <div class="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-xl p-6 mb-6 border-2 border-indigo-200">
                    <p class="text-gray-700 text-lg mb-2">Total a Pagar:</p>
                    <p class="text-4xl font-bold text-indigo-700">$${booking.selectedSeats.reduce((acc, s) => acc + Number(flight.tarifa_base) + Number(s.precio_adicional), 0).toFixed(2)}</p>
                </div>
                <button type="submit" id="btn-confirm-reservation" 
                        class="w-full bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 
                               text-white font-bold py-4 px-8 rounded-xl text-lg 
                               shadow-lg hover:shadow-xl transform hover:scale-[1.02] 
                               transition-all duration-200 
                               focus:outline-none focus:ring-4 focus:ring-green-300">
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