import type { BilleteConfirmacion } from '../models/types';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';

export const ConfirmationView = {
    render: (confirmation: BilleteConfirmacion) => {
        return `
        <div class="bg-white p-8 rounded-lg shadow-lg text-center max-w-2xl mx-auto">
            <svg class="w-24 h-24 text-green-500 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            <h2 class="text-3xl font-bold text-gray-800 mt-4">¡Compra Exitosa!</h2>
            <p class="text-gray-600 mt-2">${confirmation.mensaje}</p>
            
            <div class="my-6 p-6 bg-gray-50 rounded-lg border">
            <p class="text-lg text-gray-700">Tu código de confirmación es:</p>
            <p class="text-4xl font-mono font-bold text-indigo-600 my-2">${confirmation.codigo_confirmacion}</p>
            <p class="text-sm text-gray-500">Fecha de Compra: ${format(new Date(confirmation.fecha_compra), "PPpp", { locale: es })}</p>
            <p class="text-lg text-gray-700 mt-2">Monto Total: <span class="font-bold text-green-600">$${Number(confirmation.monto_total).toFixed(2)}</span></p>
            </div>
            
            <p class="text-gray-600">Recibirás un email con los detalles (simulado). También puedes ver tus billetes en la sección "Mis Viajes".</p>
            
            <div class="mt-8">
            <a href="#/bookings" class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-6 rounded-lg mr-4">
                Ver Mis Viajes
            </a>
            <a href="#/search" class="text-indigo-600 hover:text-indigo-800">
                Buscar más vuelos
            </a>
            </div>
        </div>
    `;
    }
};