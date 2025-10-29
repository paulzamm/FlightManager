import type { ReservaDetail, TarjetaSegura } from '../models/types';

export const PaymentView = {
    render: (reserva: ReservaDetail, tarjetas: TarjetaSegura[]) => {
        return `
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            
            <div class="md:col-span-2 bg-white p-8 rounded-xl shadow-2xl border border-gray-200">
            <h2 class="text-3xl font-bold text-gray-900 mb-2">Realizar Pago</h2>
            <p class="text-gray-600 text-sm mb-6">Selecciona o añade un método de pago</p>
            
            <div id="payment-message" class="text-center mb-4 font-semibold"></div>
            
            <div id="saved-cards-section">
                <h3 class="text-xl font-semibold text-gray-800 mb-4">Tus Tarjetas Guardadas</h3>
                ${tarjetas.length > 0 ? `
                <div class="space-y-3">
                    ${tarjetas.map(t => `
                    <label class="flex items-center p-4 border-2 border-gray-300 rounded-xl hover:bg-gradient-to-r hover:from-indigo-50 hover:to-purple-50 hover:border-indigo-400 cursor-pointer transition-all duration-200 shadow-sm">
                        <input type="radio" name="tarjeta_id" value="${t.id}" class="mr-4 w-5 h-5 text-indigo-600" ${t.es_predeterminada ? 'checked' : ''}>
                        <div class="flex-1">
                            <span class="font-mono font-bold text-gray-800">**** **** **** ${t.ultimos_4_digitos}</span>
                            <div class="text-sm text-gray-600 mt-1">${t.nombre_titular} • Exp: ${t.fecha_expiracion}</div>
                        </div>
                        ${t.es_predeterminada ? '<span class="text-xs bg-green-100 text-green-800 px-3 py-1 rounded-full font-semibold">Predeterminada</span>' : ''}
                    </label>
                    `).join('')}
                </div>
                ` : `
                <p class="text-gray-500 bg-gray-50 p-4 rounded-lg border-2 border-dashed border-gray-300">No tienes tarjetas guardadas. Añade una nueva.</p>
                `}
                <button id="btn-toggle-new-card" class="text-indigo-600 hover:text-indigo-800 font-semibold text-base mt-4 transition-colors">
                + Añadir nueva tarjeta
                </button>
            </div>
            
            <form id="new-card-form" class="mt-6 border-t-2 border-gray-200 pt-6 ${tarjetas.length > 0 ? 'hidden' : ''}">
                <h3 class="text-xl font-semibold text-gray-800 mb-4">Añadir Nueva Tarjeta</h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                    <label class="block text-sm font-semibold text-gray-800 mb-2" for="card-name">Nombre en la Tarjeta</label>
                    <input type="text" id="card-name" 
                           class="block w-full px-4 py-3 text-base border-2 border-gray-300 rounded-lg shadow-sm 
                                  bg-white placeholder-gray-400 
                                  focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 
                                  hover:border-indigo-300 transition-all duration-200"
                           placeholder="Ej: Juan Pérez" required>
                </div>
                <div>
                    <label class="block text-sm font-semibold text-gray-800 mb-2" for="card-number">Número de Tarjeta</label>
                    <input type="text" id="card-number" 
                           class="block w-full px-4 py-3 text-base border-2 border-gray-300 rounded-lg shadow-sm 
                                  bg-white placeholder-gray-400 font-mono
                                  focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 
                                  hover:border-indigo-300 transition-all duration-200" 
                           placeholder="**** **** **** ****" required>
                </div>
                <div>
                    <label class="block text-sm font-semibold text-gray-800 mb-2" for="card-exp">Expiración (MM/YY)</label>
                    <input type="text" id="card-exp" 
                           class="block w-full px-4 py-3 text-base border-2 border-gray-300 rounded-lg shadow-sm 
                                  bg-white placeholder-gray-400 font-mono
                                  focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 
                                  hover:border-indigo-300 transition-all duration-200" 
                           placeholder="MM/YY" required>
                </div>
                </div>
                <button type="submit" id="btn-save-card" 
                        class="mt-6 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 
                               text-white font-bold py-3 px-6 rounded-xl 
                               shadow-lg hover:shadow-xl transform hover:scale-[1.02] 
                               transition-all duration-200 
                               focus:outline-none focus:ring-4 focus:ring-blue-300">
                Guardar y Usar esta Tarjeta
                </button>
            </form>
            </div>
            
            <div class="md:col-span-1 bg-gradient-to-br from-gray-50 to-gray-100 p-8 rounded-xl shadow-2xl border border-gray-200">
            <h3 class="text-2xl font-bold mb-6 text-gray-900 border-b-2 border-gray-300 pb-3">Resumen de Compra</h3>
            <div class="space-y-3 mb-6">
                <p class="flex justify-between text-base"><span class="text-gray-700">Reserva ID:</span> <span class="font-bold text-gray-900">#${reserva.id}</span></p>
                <p class="flex justify-between text-base"><span class="text-gray-700">Pasajeros:</span> <span class="font-bold text-gray-900">${reserva.pasajeros.length}</span></p>
                <p class="flex justify-between text-base"><span class="text-gray-700">Estado:</span> <span class="font-bold text-yellow-600">${reserva.estado}</span></p>
            </div>
            
            <div class="border-t-2 border-b-2 border-gray-300 py-6 my-6 bg-white rounded-lg px-4">
                <p class="text-gray-700 text-base mb-2">Total a Pagar:</p>
                <p class="text-4xl font-bold text-green-600">$${Number(reserva.monto_total).toFixed(2)}</p>
            </div>
            
            <button id="btn-confirm-purchase" 
                    class="w-full bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 
                           text-white font-bold py-4 px-8 rounded-xl text-lg 
                           shadow-lg hover:shadow-xl transform hover:scale-[1.02] 
                           transition-all duration-200 
                           focus:outline-none focus:ring-4 focus:ring-green-300">
                Comprar Ahora
            </button>
            </div>
            
        </div>
    `;
    },

    bindToggleNewCard: (handler: () => void) => {
        document.getElementById('btn-toggle-new-card')?.addEventListener('click', handler);
    },

    toggleNewCardForm: (show: boolean) => {
        document.getElementById('new-card-form')?.classList.toggle('hidden', !show);
    },

    bindSaveCard: (handler: (e: SubmitEvent) => void) => {
        document.getElementById('new-card-form')?.addEventListener('submit', handler);
    },

    bindPurchase: (handler: () => void) => {
        document.getElementById('btn-confirm-purchase')?.addEventListener('click', handler);
    },

    getNewCardData: () => ({
        nombre: (document.getElementById('card-name') as HTMLInputElement).value,
        numero: (document.getElementById('card-number') as HTMLInputElement).value,
        expiracion: (document.getElementById('card-exp') as HTMLInputElement).value,
    }),

    getSelectedCardId: (): number | null => {
        const selectedCard = document.querySelector<HTMLInputElement>('input[name="tarjeta_id"]:checked');
        return selectedCard ? Number(selectedCard.value) : null;
    },

    displayMessage: (message: string, isError: boolean) => {
        const el = document.getElementById('payment-message') as HTMLDivElement;
        el.textContent = message;
        el.className = `text-center mb-4 ${isError ? 'text-red-500' : 'text-green-500'}`;
    },

    setLoading: (isLoading: boolean) => {
        const btn = document.getElementById('btn-confirm-purchase') as HTMLButtonElement;
        if (isLoading) {
            btn.disabled = true;
            btn.innerHTML = 'Procesando Pago...';
        } else {
            btn.disabled = false;
            btn.innerHTML = 'Comprar Ahora';
        }
    }
};