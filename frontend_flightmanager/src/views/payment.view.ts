import type { ReservaDetail, TarjetaSegura } from '../models/types';

export const PaymentView = {
    render: (reserva: ReservaDetail, tarjetas: TarjetaSegura[]) => {
        return `
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            
            <div class="md:col-span-2 bg-white p-6 rounded-lg shadow-lg">
            <h2 class="text-2xl font-bold text-gray-800 mb-6">Realizar Pago</h2>
            
            <div id="payment-message" class="text-center mb-4"></div>
            
            <div id="saved-cards-section">
                <h3 class="text-lg font-semibold mb-3">Tus Tarjetas Guardadas</h3>
                ${tarjetas.length > 0 ? `
                <div class="space-y-3">
                    ${tarjetas.map(t => `
                    <label class="flex items-center p-3 border rounded-lg hover:bg-gray-50 cursor-pointer">
                        <input type="radio" name="tarjeta_id" value="${t.id}" class="mr-3" ${t.es_predeterminada ? 'checked' : ''}>
                        <span class="font-mono">**** **** **** ${t.ultimos_4_digitos}</span>
                        <span class="ml-auto text-sm text-gray-600">${t.nombre_titular} (${t.fecha_expiracion})</span>
                    </label>
                    `).join('')}
                </div>
                ` : `
                <p class="text-gray-500">No tienes tarjetas guardadas. Añade una nueva.</p>
                `}
                <button id="btn-toggle-new-card" class="text-indigo-600 hover:text-indigo-800 text-sm mt-4">
                + Añadir nueva tarjeta
                </button>
            </div>
            
            <form id="new-card-form" class="mt-6 border-t pt-6 ${tarjetas.length > 0 ? 'hidden' : ''}">
                <h3 class="text-lg font-semibold mb-3">Añadir Nueva Tarjeta</h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700" for="card-name">Nombre en la Tarjeta</label>
                    <input type="text" id="card-name" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm" required>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700" for="card-number">Número de Tarjeta</label>
                    <input type="text" id="card-number" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm" placeholder="**** **** **** ****" required>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700" for="card-exp">Expiración (MM/YY)</label>
                    <input type="text" id="card-exp" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm" placeholder="MM/YY" required>
                </div>
                </div>
                <button type="submit" id="btn-save-card" class="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg">
                Guardar y Usar esta Tarjeta
                </button>
            </form>
            </div>
            
            <div class="md:col-span-1 bg-gray-50 p-6 rounded-lg shadow-inner">
            <h3 class="text-xl font-bold mb-4 border-b pb-2">Resumen de Compra</h3>
            <p class="flex justify-between"><span>Reserva ID:</span> <span class="font-semibold">#${reserva.id}</span></p>
            <p class="flex justify-between"><span>Pasajeros:</span> <span class="font-semibold">${reserva.pasajeros.length}</span></p>
            <p class="flex justify-between mb-4"><span>Estado:</span> <span class="font-semibold text-yellow-600">${reserva.estado}</span></p>
            
            <div class="border-t border-b py-4 my-4">
                <p class="text-2xl font-bold flex justify-between">
                <span>Total a Pagar:</span>
                <span class="text-green-600">$${reserva.monto_total.toFixed(2)}</span>
                </p>
            </div>
            
            <button id="btn-confirm-purchase" class="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-lg text-lg">
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