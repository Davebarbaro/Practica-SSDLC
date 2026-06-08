/**
 * Configuración de la aplicación frontend
 */

// URL base del API backend
// Usar rutas relativas para que pasen por el proxy de NGINX
// En HTTPS: las peticiones irán a https://localhost:8443/auth/*, etc.
// NGINX hará proxy interno a http://backend:8000
const API_BASE_URL = '';

// Exportar para uso en otros módulos
window.API_BASE_URL = API_BASE_URL;
