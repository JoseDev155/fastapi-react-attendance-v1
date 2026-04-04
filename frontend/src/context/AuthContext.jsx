import { createContext, useContext, useState, useEffect } from 'react';

// AuthContext: decodifica el JWT del localStorage y, si el payload no incluye
// los campos de usuario (tokens emitidos antes de la actualización del backend),
// los obtiene llamando a GET /auth/me como fallback.

const AuthContext = createContext(null);
const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000';

function parseJwtPayload(token) {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );
    return JSON.parse(jsonPayload);
  } catch {
    return null;
  }
}

function buildUser(payload) {
  if (!payload) return null;
  return {
    id:         payload.sub  ?? '',
    roleId:     payload.role_id ?? null,
    isAdmin:    payload.role_id === 1,
    isProfesor: payload.role_id === 2,
    roleName:   payload.role_id === 1 ? 'Administrador' : payload.role_id === 2 ? 'Profesor' : null,
    firstName:  payload.first_name ?? null,
    lastName:   payload.last_name  ?? '',
    fullName:   payload.first_name
      ? `${payload.first_name} ${payload.last_name ?? ''}`.trim()
      : null,
  };
}

export function AuthProvider({ children }) {
  const [token, setToken]   = useState(() => localStorage.getItem('accessToken'));
  const [user, setUser]     = useState(null);
  const [ready, setReady]   = useState(false);

  useEffect(() => {
    if (!token) {
      setUser(null);
      setReady(true);
      return;
    }

    const payload = parseJwtPayload(token);

    // Si el payload ya contiene first_name y role_id, usarlo directamente
    if (payload?.first_name && payload?.role_id != null) {
      setUser(buildUser(payload));
      setReady(true);
      return;
    }

    // Fallback: solicitar datos al endpoint /auth/me
    fetch(`${API_BASE}/auth/me`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then(res => {
        if (!res.ok) throw new Error('Token inválido');
        return res.json();
      })
      .then(data => {
        setUser({
          id:         data.id,
          roleId:     data.role_id,
          isAdmin:    data.role_id === 1,
          isProfesor: data.role_id === 2,
          roleName:   data.role_id === 1 ? 'Administrador' : 'Profesor',
          firstName:  data.first_name,
          lastName:   data.last_name ?? '',
          fullName:   `${data.first_name} ${data.last_name ?? ''}`.trim(),
        });
      })
      .catch(() => {
        // Token inválido o expirado → limpiar sesión
        localStorage.removeItem('accessToken');
        setToken(null);
        setUser(null);
      })
      .finally(() => setReady(true));
  }, [token]);

  // Escuchar cambios en localStorage (login/logout desde otras pestañas o desde LoginPage)
  useEffect(() => {
    const onStorage = () => {
      const t = localStorage.getItem('accessToken');
      setToken(t);
      if (!t) setUser(null);
    };
    window.addEventListener('storage', onStorage);
    return () => window.removeEventListener('storage', onStorage);
  }, []);

  return (
    <AuthContext.Provider value={{ user, token, ready, setToken }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
