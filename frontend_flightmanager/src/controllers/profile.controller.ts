import { LayoutView } from '../views/layout.view';
import { MyBookingsView } from '../views/myBookings.view';
import { ProfileView } from '../views/profile.view';
import { reservationService } from '../services/reservation.service';
import { paymentService } from '../services/payment.service';
import { userService } from '../services/user.service';

/**
 * Inicializa la página "Mis Viajes"
 */
export const initMyBookings = async (params: any, title: string) => {
    LayoutView.renderPageContent(title, MyBookingsView.render());

    try {
        // Cargar ambas listas en paralelo
        const [pendientes, comprados] = await Promise.all([
            reservationService.getMyReservations('Pendiente'),
            paymentService.getMyTickets()
        ]);

        MyBookingsView.renderPending(pendientes, handlePayNow, handleCancelBooking);
        MyBookingsView.renderConfirmed(comprados);

    } catch (error: any) {
        (document.getElementById('pending-reservations-list') as HTMLDivElement).innerHTML = `<p class="text-red-500">${error.message}</p>`;
    }
};

const handlePayNow = (id: number) => {
    window.location.hash = `/book/payment/${id}`;
};

const handleCancelBooking = async (id: number) => {
    if (confirm('¿Estás seguro de que deseas cancelar esta reserva?')) {
        try {
            await reservationService.cancelReservation(id);
            await initMyBookings(null, 'Mis Viajes'); // Recargar la vista
        } catch (error: any) {
            alert(error.message);
        }
    }
};

/**
 * Inicializa la página "Mi Perfil"
 */
export const initProfile = async (params: any, title: string) => {
    try {
        const [profile, tarjetas] = await Promise.all([
            userService.getFullProfile(),
            paymentService.getMyCards()
        ]);

        LayoutView.renderPageContent(title, ProfileView.render(profile, tarjetas));

        // Binds
        ProfileView.bindUpdateProfile(handleUpdateProfile);
        ProfileView.bindChangePassword(handleChangePassword);
        ProfileView.bindAddCard(handleAddCard);
        ProfileView.bindDeleteCard(handleDeleteCard);
        
        // Formateo automático del campo de expiración
        setupCardExpirationFormatting();
        // Validación de solo números en tarjeta
        setupCardNumberValidation();

    } catch (error: any) {
        LayoutView.renderPageContent('Error', `<p class="text-red-500">${error.message}</p>`);
    }
};

// Helper para formatear automáticamente MM/YY
const setupCardExpirationFormatting = () => {
    const expInput = document.getElementById('card-exp-new') as HTMLInputElement;
    if (!expInput) return;
    
    expInput.addEventListener('input', (e) => {
        let value = (e.target as HTMLInputElement).value.replace(/\D/g, ''); // Solo números
        
        if (value.length >= 2) {
            value = value.substring(0, 2) + '/' + value.substring(2, 4);
        }
        
        (e.target as HTMLInputElement).value = value;
    });
};

// Helper para validar solo números en el campo de tarjeta
const setupCardNumberValidation = () => {
    const cardInput = document.getElementById('card-num-new') as HTMLInputElement;
    if (!cardInput) return;
    
    cardInput.addEventListener('input', (e) => {
        let value = (e.target as HTMLInputElement).value.replace(/\D/g, ''); // Solo números
        (e.target as HTMLInputElement).value = value;
    });
};

const handleUpdateProfile = async (e: SubmitEvent) => {
    e.preventDefault();
    const { nombre, email } = ProfileView.getProfileData();
    try {
        await userService.updateProfile(nombre, email);
        ProfileView.displayProfileMessage('Perfil actualizado.', false);
    } catch (error: any) {
        ProfileView.displayProfileMessage(error.message, true);
    }
};

const handleChangePassword = async (e: SubmitEvent) => {
    e.preventDefault();
    const { actual, nueva } = ProfileView.getPasswordData();
    try {
        await userService.changePassword(actual, nueva);
        ProfileView.displayPasswordMessage('Contraseña actualizada.', false);
        (e.target as HTMLFormElement).reset();
    } catch (error: any) {
        ProfileView.displayPasswordMessage(error.message, true);
    }
};

const handleAddCard = async (e: SubmitEvent) => {
    e.preventDefault();
    const { nombre, numero, expiracion } = ProfileView.getNewCardData();
    try {
        await paymentService.addCard(numero, expiracion, nombre);
        ProfileView.displayCardMessage('Tarjeta añadida.', false);
        (e.target as HTMLFormElement).reset();
        await initProfile(null, 'Mi Perfil'); // Recargar
    } catch (error: any) {
        ProfileView.displayCardMessage(error.message, true);
    }
};

const handleDeleteCard = async (id: number) => {
    if (confirm('¿Eliminar esta tarjeta?')) {
        try {
            await paymentService.deleteCard(id);
            ProfileView.displayCardMessage('Tarjeta eliminada.', false);
            await initProfile(null, 'Mi Perfil'); // Recargar
        } catch (error: any) {
            ProfileView.displayCardMessage(error.message, true);
        }
    }
};