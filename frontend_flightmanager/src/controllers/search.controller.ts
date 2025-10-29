import { LayoutView } from '../views/layout.view';
import { DashboardView } from '../views/dashboard.view';
import { FlightResultsView } from '../views/flightsResults.view';
import { FlightDetailView } from '../views/flightDetail.view';
import { flightService } from '../services/flight.service';
import { store } from '../models/store';
import type { AsientoResponse, FlightResult } from '../models/types';

// Variables de estado para paginación
let currentPage: number = 1;
let currentFilters: any = {};
let currentResults: FlightResult[] = [];
let totalFlights: number = 0;
let limit: number = 20;

/**
 * Inicializa la página de Búsqueda (Dashboard) con todos los vuelos
 */
export const init = async (params: any, title: string) => {
    LayoutView.renderPageContent(title, DashboardView.render());
    DashboardView.bindFilterSubmit(handleFilterSubmit);
    DashboardView.bindResetFilters(handleResetFilters);
    DashboardView.bindToggleFilters();
    
    // Cargar todos los vuelos al iniciar
    await loadAllFlights(1);
};

/**
 * Carga todos los vuelos con paginación y filtros
 */
const loadAllFlights = async (page: number = 1) => {
    try {
        DashboardView.showLoading();
        
        const filters = DashboardView.getFilters();
        currentFilters = filters;
        limit = filters.limit || 20;
        currentPage = page;
        
        const skip = (page - 1) * limit;
        
        const flights = await flightService.listAllFlights({
            skip,
            limit,
            origen: filters.origen,
            destino: filters.destino,
            fecha_desde: filters.fecha_desde,
            fecha_hasta: filters.fecha_hasta,
            aerolinea: filters.aerolinea,
            ordenar_por: filters.ordenar_por as 'fecha' | 'precio' | 'aerolinea'
        });

        currentResults = flights;
        
        // Estimación del total basada en los resultados
        totalFlights = flights.length < limit 
            ? skip + flights.length 
            : (page + 1) * limit;
        
        renderResults();
        
    } catch (error: any) {
        console.error('Error al cargar vuelos:', error);
        DashboardView.showError(error.message || 'Error al cargar los vuelos disponibles');
    }
};

/**
 * Renderiza los resultados actuales
 */
const renderResults = () => {
    const container = document.getElementById('flight-results-container');
    if (!container) return;

    if (currentResults.length === 0) {
        container.innerHTML = `
            <div class="text-center py-12">
                <svg class="mx-auto h-16 w-16 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M12 12h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p class="mt-4 text-gray-600 text-lg font-medium">No se encontraron vuelos con estos filtros</p>
                <p class="mt-2 text-gray-500">Intenta ajustar tus criterios de búsqueda</p>
            </div>
        `;
        DashboardView.updateResultsInfo(0, 0, currentPage, 1);
        DashboardView.renderPagination(1, 1, () => {});
        return;
    }

    // Renderizar vuelos
    container.innerHTML = FlightResultsView.renderFlightCards(
        currentResults,
        'browse'
    );

    // Bind eventos de selección
    FlightResultsView.bindFlightSelection((flightId) => {
        window.location.hash = `#/flight/${flightId}`;
    });

    // Actualizar información de resultados
    const showing = currentResults.length;
    const totalPages = Math.ceil(totalFlights / limit);
    
    DashboardView.updateResultsInfo(
        totalFlights,
        showing,
        currentPage,
        totalPages
    );

    // Renderizar paginación
    DashboardView.renderPagination(
        currentPage,
        totalPages,
        handlePageChange
    );

    // Scroll suave al inicio de resultados
    container.scrollIntoView({ behavior: 'smooth', block: 'start' });
};

/**
 * Maneja el submit del formulario de filtros
 */
const handleFilterSubmit = async (e: SubmitEvent) => {
    e.preventDefault();
    currentPage = 1;
    await loadAllFlights(1);
};

/**
 * Maneja el reset de filtros
 */
const handleResetFilters = async () => {
    DashboardView.resetFilters();
    currentPage = 1;
    currentFilters = {};
    await loadAllFlights(1);
};

/**
 * Maneja el cambio de página
 */
const handlePageChange = async (page: number) => {
    if (page < 1) return;
    await loadAllFlights(page);
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