import { LayoutView } from '../views/layout.view';
import { DashboardView } from '../views/dashboard.view';
import { FlightResultsView } from '../views/flightsResults.view';
import { FlightDetailView } from '../views/flightDetail.view';
import { flightService } from '../services/flight.service';
import { store } from '../models/store';
import type { AsientoResponse } from '../models/types';

/**
 * Inicializa la página de Búsqueda (Dashboard)
 */
export const init = async (params: any, title: string) => {
    LayoutView.renderPageContent(title, DashboardView.render());
    DashboardView.bindSearch(handleFlightSearch);
};

/**
 * Maneja el submit del formulario de búsqueda
 */
const handleFlightSearch = async (e: SubmitEvent) => {
    e.preventDefault();
    DashboardView.showLoading();
    const form = e.target as HTMLFormElement;
    const origen = (form.elements.namedItem('origen') as HTMLInputElement).value;
    const destino = (form.elements.namedItem('destino') as HTMLInputElement).value;
    const fecha = (form.elements.namedItem('fecha') as HTMLInputElement).value;

    try {
        // Usamos la búsqueda simple
        const flights = await flightService.searchFlights(origen, destino, fecha);
        FlightResultsView.render(flights, (flightId) => {
            window.location.hash = `/flight/${flightId}`;
        });
    } catch (error: any) {
        DashboardView.showError(error.message);
    }
};

/**
 * Inicializa la página de Detalle de Vuelo (Selección de Asientos)
 */
export const initFlightDetail = async (params: { id: string }, title: string) => {
    try {
        const flightId = Number(params.id);
        const [flight, seats] = await Promise.all([
            flightService.getFlightDetails(flightId),
            flightService.getFlightSeats(flightId)
        ]);

        LayoutView.renderPageContent(`${title}: ${flight.numero_vuelo}`, FlightDetailView.render(flight, seats));

        // Lógica del controlador para la selección de asientos
        const selectedSeats = new Map<number, AsientoResponse>();

        FlightDetailView.bindSeatSelection((seat, el) => {
            if (selectedSeats.has(seat.id)) {
                selectedSeats.delete(seat.id);
                el.classList.remove('selected');
            } else {
                selectedSeats.set(seat.id, seat);
                el.classList.add('selected');
            }

            // Actualizar resumen
            const total = Array.from(selectedSeats.values()).reduce((acc, s) => {
                return acc + Number(flight.tarifa_base) + Number(s.precio_adicional);
            }, 0);
            FlightDetailView.updateSummary(selectedSeats.size, total);
        });

        // Bind al botón de continuar
        FlightDetailView.bindContinueToPassengers(() => {
            // Guardar selección en el store y navegar
            store.setBookingFlow(flight, Array.from(selectedSeats.values()));
            window.location.hash = '/book/passengers';
        });

    } catch (error: any) {
        LayoutView.renderPageContent('Error', `<p class="text-red-500">${error.message}</p>`);
    }
};