// apiClient.js — Wrapper sobre fetch para las páginas del dashboard.
import { API_BASE } from '../config';


/**
 * Realiza una petición autenticada a la API.
 * @param {string} endpoint - Ruta relativa, ej: '/groups'
 * @param {object} opts
 * @param {string} opts.token - JWT de acceso
 * @param {string} [opts.method='GET']
 * @param {object} [opts.body] - Cuerpo de la petición (se serializa a JSON)
 * @returns {Promise<any>} JSON de respuesta o undefined (204 No Content)
 */
export async function apiFetch(endpoint, { token, method = 'GET', body } = {}) {
  const headers = { Authorization: `Bearer ${token}` };
  if (body !== undefined) headers['Content-Type'] = 'application/json';

  const res = await fetch(`${API_BASE}${endpoint}`, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });

  // Sesión expirada → redirigir al login
  if (res.status === 401) {
    localStorage.removeItem('accessToken');
    window.location.href = '/login';
    throw new Error('Sesión expirada. Redirigiendo al login...');
  }

  // No Content (DELETE exitoso, etc.)
  if (res.status === 204) return undefined;

  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    const detail = data?.detail;
    const msg = typeof detail === 'string'
      ? detail
      : Array.isArray(detail)
        ? detail.map(e => e.msg ?? JSON.stringify(e)).join(', ')
        : `Error ${res.status}`;
    throw new Error(msg);
  }

  return data;
}
