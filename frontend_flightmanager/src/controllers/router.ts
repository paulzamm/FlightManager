import { store } from '../models/store';
import { LayoutView } from '../views/layout.view';
import { LoginView } from '../views/login.view';
import * as AuthController from './auth.controller';
import * as SearchController from './search.controller';
import * as BookingController from './booking.controller';
import * as ProfileController from './profile.controller';

// Definición de Rutas
const routes: { [key: string]: { view: string, controller: (params: any, title: string) => void | Promise<void>, title: string, private: boolean } } = {
    '/login': {
        view: 'LoginView',
        controller: AuthController.init,
        title: 'Login',
        private: false
    },
    '/search': {
        view: 'DashboardView',
        controller: SearchController.init,
        title: 'Buscar Vuelos',
        private: true
    },
    '/flight/:id': {
        view: 'FlightDetailView',
        controller: SearchController.initFlightDetail,
        title: 'Seleccionar Asientos',
        private: true
    },
    '/book/passengers': {
        view: 'ReservationView',
        controller: BookingController.initPassengerStep,
        title: 'Datos de Pasajeros',
        private: true
    },
    '/book/payment/:id': {
        view: 'PaymentView',
        controller: BookingController.initPaymentStep,
        title: 'Realizar Pago',
        private: true
    },
    '/confirmation/:code': {
        view: 'ConfirmationView',
        controller: BookingController.initConfirmationPage,
        title: 'Compra Exitosa',
        private: true
    },
    '/bookings': {
        view: 'MyBookingsView',
        controller: ProfileController.initMyBookings,
        title: 'Mis Viajes',
        private: true
    },
    '/profile': {
        view: 'ProfileView',
        controller: ProfileController.initProfile,
        title: 'Mi Perfil',
        private: true
    }
};

/**
 * Parsea el hash de la URL (ej. /flight/123)
 */
const parseRequestURL = () => {
    const url = location.hash.slice(1).toLowerCase() || '/';
    const r = url.split('/'); // [ '', 'flight', '123' ]

    const request = {
        resource: r[1],
        id: r[2],
        verb: r[3]
    };

    // Genera una ruta genérica para el router: /flight/:id
    const parsedURL = (request.resource ? '/' + request.resource : '/') +
        (request.id ? '/:id' : '') +
        (request.verb ? '/' + request.verb : '');

    return { parsedURL, params: request };
}

/**
* El Controlador del Router. Se activa cuando cambia el hash.
*/
export const handleRouteChange = async () => {
    const { parsedURL, params } = parseRequestURL();
    const route = routes[parsedURL] || routes['/search']; // default a /search

    const isAuthenticated = store.isAuthenticated();

    if (route.private && !isAuthenticated) {
        // Si la ruta es privada y no está logueado, redirige a /login
        window.location.hash = '/login';
        return;
    }

    if (!route.private && isAuthenticated) {
        // Si la ruta es pública (login) y SÍ está logueado, redirige a /search
        window.location.hash = '/search';
        return;
    }

    // Renderizar la vista
    if (route.view === 'LoginView') {
        LoginView.render();
    } else {
        // Para todas las rutas privadas, renderiza primero el Layout
        LayoutView.render();
        LayoutView.bindLogout(AuthController.handleLogout);
        LayoutView.updateActiveLink(parsedURL);
    }

    // Ejecuta el controlador específico de la página
    // Pasamos los params (ej. el ID del vuelo) al controlador
    await route.controller(params, route.title);
};