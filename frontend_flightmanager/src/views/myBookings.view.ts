import type { ReservaDetail, BilleteResponse } from '../models/types';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';

export const MyBookingsView = {
    render: () => {
        return `
        <div class="space-y-8">
            <div class="bg-white p-6 rounded-xl shadow-2xl border border-gray-200">
                <div class="mb-6 pb-4 border-b-2 border-gray-200">
                    <h2 class="text-3xl font-bold text-gray-900 flex items-center">
                        Reservas Pendientes de Pago
                    </h2>
                    <p class="text-gray-600 mt-2 text-sm ml-11">Completa el pago de tus reservas antes de que expiren</p>
                </div>
                <div id="pending-reservations-list" class="space-y-4"></div>
            </div>
            
            <div class="bg-white p-6 rounded-xl shadow-2xl border border-gray-200">
                <div class="mb-6 pb-4 border-b-2 border-gray-200">
                    <h2 class="text-3xl font-bold text-gray-900 flex items-center">
                        <svg class="h-8 w-8 mr-3 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        Mis Billetes Comprados
                    </h2>
                    <p class="text-gray-600 mt-2 text-sm ml-11">Tus vuelos confirmados y listos para viajar</p>
                </div>
                <div id="confirmed-tickets-list" class="space-y-4"></div>
            </div>
        </div>
    `;
    },

    renderPending: (reservas: ReservaDetail[], payHandler: (id: number) => void, cancelHandler: (id: number) => void) => {
        const container = document.getElementById('pending-reservations-list')!;
        if (reservas.length === 0) {
            container.innerHTML = `
                <div class="text-center py-8">
                    <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                    </svg>
                    <p class="mt-2 text-gray-600 font-semibold">No tienes reservas pendientes.</p>
                    <p class="text-sm text-gray-500">Tus reservas sin pagar aparecerán aquí.</p>
                </div>
            `;
            return;
        }
        container.innerHTML = reservas.map(r => `
            <div class="bg-white rounded-lg shadow-md hover:shadow-xl transition-all duration-200 p-6">
                <div class="flex flex-col md:flex-row justify-between items-start md:items-center space-y-4 md:space-y-0">
                    
                    <!-- Información de la reserva -->
                    <div class="flex items-center space-x-4">
                        <div class="w-12 h-12 bg-yellow-100 rounded-full flex items-center justify-center">
                            <svg class="h-6 w-6 text-yellow-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                        </div>
                        <div>
                            <div class="text-lg font-bold text-gray-900">Reserva #${r.id}</div>
                            <div class="text-sm text-gray-500">${format(new Date(r.fecha_reserva), "PPp", { locale: es })}</div>
                            <div class="text-xs text-yellow-600 font-semibold mt-1">⏳ Pendiente de Pago</div>
                        </div>
                    </div>
                    
                    <!-- Detalles centrales -->
                    <div class="flex items-center space-x-6 flex-1 justify-center">
                        <div class="text-center">
                            <div class="text-sm text-gray-500 mb-1">Pasajeros</div>
                            <div class="text-2xl font-bold text-indigo-600">${r.pasajeros?.length || 0}</div>
                        </div>
                        
                        <div class="text-center text-gray-400">
                            <svg class="h-6 w-6 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
                            </svg>
                        </div>
                        
                        <div class="text-center">
                            <div class="text-sm text-gray-500 mb-1">Total a Pagar</div>
                            <div class="text-3xl font-bold text-green-600">$${Number(r.monto_total).toFixed(2)}</div>
                        </div>
                    </div>
                    
                    <!-- Acciones -->
                    <div class="w-full md:w-auto">
                        <button class="btn-pay bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white font-bold py-2 px-6 rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl" data-id="${r.id}">
                            Pagar Ahora
                        </button>
                        <button class="btn-cancel bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white font-bold py-2 px-6 rounded-lg transition-all duration-200" data-id="${r.id}">
                            Cancelar
                        </button>
                    </div>
                    
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
            container.innerHTML = `
                <div class="text-center py-8">
                    <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    <p class="mt-2 text-gray-600 font-semibold">No tienes billetes comprados.</p>
                    <p class="text-sm text-gray-500">Tus billetes confirmados aparecerán aquí.</p>
                </div>
            `;
            return;
        }
        container.innerHTML = billetes.map(b => `
            <div class="bg-white rounded-lg shadow-md hover:shadow-xl transition-all duration-200 p-6">
                <div class="flex flex-col md:flex-row justify-between items-start md:items-center space-y-4 md:space-y-0">
                    
                    <!-- Información del billete -->
                    <div class="flex items-center space-x-4">
                        <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                            <svg class="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                        </div>
                        <div>
                            <div class="text-lg font-bold text-indigo-700">${b.codigo_confirmacion}</div>
                            <div class="text-sm text-gray-500">${format(new Date(b.fecha_compra), "PPp", { locale: es })}</div>
                            <div class="text-xs text-green-600 font-semibold mt-1">✓ Confirmado</div>
                        </div>
                    </div>
                    
                    <!-- Detalles centrales -->
                    <div class="flex items-center space-x-6 flex-1 justify-center">
                        <div class="text-center">
                            <div class="text-sm text-gray-500 mb-1">Código de Confirmación</div>
                            <div class="text-xl font-bold text-gray-800 font-mono tracking-wider">${b.codigo_confirmacion}</div>
                        </div>
                        
                        <div class="text-center text-gray-400">
                            <svg class="h-6 w-6 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
                            </svg>
                        </div>
                        
                        <div class="text-center">
                            <div class="text-sm text-gray-500 mb-1">Reserva</div>
                            <div class="text-xl font-bold text-gray-700">#${b.id_reserva}</div>
                        </div>
                    </div>
                    
                    <!-- Acciones -->
                    <div class="text-right">
                        <button class="btn-view-ticket bg-gradient-to-r from-indigo-600 to-indigo-700 hover:from-indigo-700 hover:to-indigo-800 text-white font-bold py-3 px-6 rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl w-full md:w-auto" data-code="${b.codigo_confirmacion}">
                            Ver Detalles
                        </button>
                    </div>
                    
                </div>
            </div>
        `).join('');
        
        // Bind click para ver detalles del billete
        container.querySelectorAll('.btn-view-ticket').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const codigo = (e.currentTarget as HTMLElement).dataset.code;
                window.location.hash = `/confirmation/${codigo}`;
            });
        });
    }
};