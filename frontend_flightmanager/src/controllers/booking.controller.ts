import { LayoutView } from '../views/layout.view';
import { ReservationView } from '../views/reservation.view';
import { PaymentView } from '../views/payment.view';
import { ConfirmationView } from '../views/confirmation.view';
import { store } from '../models/store';
import { reservationService } from '../services/reservation.service';
import { paymentService } from '../services/payment.service';
import type { PasajeroCreate } from '../models/types';

/**
 * Inicializa la página de Pasajeros
 */
export const initPassengerStep = (params: any, title: string) => {
    const bookingState = store.getBookingFlow();
    if (!bookingState || bookingState.selectedSeats.length === 0) {
        window.location.hash = '/search'; // No hay selección, volver
        return;
    }

    LayoutView.renderPageContent(title, ReservationView.render(bookingState));
    ReservationView.bindConfirmReservation(handlePassengerSubmit);
};

/**
 * Maneja el submit del formulario de pasajeros
 */
const handlePassengerSubmit = async (e: SubmitEvent) => {
    e.preventDefault();
    ReservationView.setLoading(true);

    try {
        const passengerData: PasajeroCreate[] = ReservationView.getPassengerData();
        // Validar que todos los campos estén llenos
        if (passengerData.some(p => !p.nombre_completo || !p.documento_identidad)) {
            throw new Error('Por favor, completa los datos de todos los pasajeros.');
        }

        // Llamar a la API para crear la reserva
        const reserva = await reservationService.createReservation(passengerData);

        // Limpiar el flujo de asientos y redirigir al pago
        store.clearBookingFlow();
        window.location.hash = `/book/payment/${reserva.id}`;

    } catch (error: any) {
        ReservationView.displayMessage(error.message, true);
    } finally {
        ReservationView.setLoading(false);
    }
};

/**
 * Inicializa la página de Pago
 */
export const initPaymentStep = async (params: { id: string }, title: string) => {
    try {
        const reservaId = Number(params.id);
        const [reserva, tarjetas] = await Promise.all([
            reservationService.getReservationDetails(reservaId),
            paymentService.getMyCards()
        ]);

        if (reserva.estado !== 'Pendiente') {
            window.location.hash = '/bookings'; // La reserva ya no está pendiente
            return;
        }

        LayoutView.renderPageContent(title, PaymentView.render(reserva, tarjetas));

        // Binds
        PaymentView.bindToggleNewCard(() => PaymentView.toggleNewCardForm(true));
        PaymentView.bindSaveCard(handleSaveCard);
        PaymentView.bindPurchase(() => handlePurchase(reservaId));

    } catch (error: any) {
        LayoutView.renderPageContent('Error', `<p class="text-red-500">${error.message}</p>`);
    }
};

/**
 * Maneja el guardado de una nueva tarjeta
 */
const handleSaveCard = async (e: SubmitEvent) => {
    e.preventDefault();
    PaymentView.displayMessage('Guardando tarjeta...', false);
    try {
        const { nombre, numero, expiracion } = PaymentView.getNewCardData();
        await paymentService.addCard(numero, expiracion, nombre);

        // Recargar la vista de pago con la nueva tarjeta
        await initPaymentStep({ id: (window.location.hash.split('/')[3]) }, 'Realizar Pago');
        PaymentView.displayMessage('Tarjeta añadida exitosamente.', false);

    } catch (error: any) {
        PaymentView.displayMessage(error.message, true);
    }
};

/**
 * Maneja la compra final
 */
const handlePurchase = async (reservaId: number) => {
    PaymentView.setLoading(true);
    PaymentView.displayMessage('Procesando pago...', false);

    try {
        const tarjetaId = PaymentView.getSelectedCardId();
        if (!tarjetaId) {
            throw new Error('Por favor, selecciona o añade una tarjeta de crédito.');
        }

        const billete = await paymentService.purchaseTicket(reservaId, tarjetaId);

        // Redirigir a la confirmación
        window.location.hash = `/confirmation/${billete.codigo_confirmacion}`;

    } catch (error: any) {
        PaymentView.displayMessage(error.message, true);
    } finally {
        PaymentView.setLoading(false);
    }
};

/**
 * Inicializa la página de Confirmación
 */
export const initConfirmationPage = async (params: any, title: string) => {
    try {
        const codigo = params.code || params.id; // Soporta ambos por compatibilidad
        const confirmacion = await paymentService.getConfirmation(codigo);
        LayoutView.renderPageContent(title, ConfirmationView.render(confirmacion));
    } catch (error: any) {
        LayoutView.renderPageContent('Error', `<p class="text-red-500">${error.message}</p>`);
    }
};