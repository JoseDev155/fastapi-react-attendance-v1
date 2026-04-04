// config.js — Configuración global del frontend.
// Centraliza las variables de entorno y valida que estén definidas
// antes de que la app arranque, evitando errores silenciosos en producción.

const apiBase = import.meta.env.VITE_API_BASE_URL;

if (!apiBase) {
  throw new Error(
    '[Config] VITE_API_BASE_URL no está definida.\n' +
    'Crea el archivo frontend/.env con la variable:\n' +
    '  VITE_API_BASE_URL=http://127.0.0.1:8000'
  );
}

export const API_BASE = apiBase;
