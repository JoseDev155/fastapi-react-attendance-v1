import { useState } from 'react';
import { Outlet, useNavigate, useLocation, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

// Definición de módulos por rol.
// Cada módulo incluye: ruta, etiqueta, ícono Material Symbols y roles permitidos.
// roles: [1] = solo Admin | [1,2] = Admin y Profesor
const ALL_MODULES = [
  // ── Comunes Admin y Profesor ──────────────────────────────
  {
    path: '/dashboard/asistencias',
    label: 'Asistencias',
    icon: 'assignment_turned_in',
    roles: [1, 2],
    section: 'Académico',
  },
  {
    path: '/dashboard/grupos',
    label: 'Grupos',
    icon: 'groups',
    roles: [1, 2],
    section: 'Académico',
  },
  {
    path: '/dashboard/estudiantes',
    label: 'Estudiantes',
    icon: 'school',
    roles: [1, 2],
    section: 'Académico',
  },
  {
    path: '/dashboard/ciclos',
    label: 'Ciclos Académicos',
    icon: 'event_repeat',
    roles: [1, 2],
    section: 'Académico',
  },
  {
    path: '/dashboard/inscripciones',
    label: 'Inscripciones',
    icon: 'how_to_reg',
    roles: [1, 2],
    section: 'Académico',
  },
  {
    path: '/dashboard/horarios',
    label: 'Horarios',
    icon: 'schedule',
    roles: [1, 2],
    section: 'Académico',
  },
  // ── Solo Administrador ────────────────────────────────────
  {
    path: '/dashboard/subir-asistencias',
    label: 'Subir Asistencias',
    icon: 'upload_file',
    roles: [1],
    section: 'Administración',
  },
  {
    path: '/dashboard/reportes',
    label: 'Reportes',
    icon: 'bar_chart',
    roles: [1],
    section: 'Administración',
  },
  {
    path: '/dashboard/usuarios',
    label: 'Usuarios del Sistema',
    icon: 'manage_accounts',
    roles: [1],
    section: 'Administración',
  },
];

export default function MainLayout() {
  const navigate = useNavigate();
  const location = useLocation();
  const { user } = useAuth();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    navigate('/login');
  };

  // Filtrar módulos según el rol del usuario autenticado
  const roleId = user?.roleId ?? 0;
  const visibleModules = ALL_MODULES.filter(m => m.roles.includes(roleId));

  // Agrupar por sección para el sidebar
  const sections = [...new Set(visibleModules.map(m => m.section))];

  // Iniciales para el avatar
  const initials = user
    ? `${user.firstName.charAt(0)}${user.lastName?.charAt(0) ?? ''}`.toUpperCase()
    : '?';

  return (
    <div className="app-shell">

      {/* ── Topbar ─────────────────────────────────────────── */}
      <header className="topbar">
        {/* Burger (solo móvil) */}
        <button
          className="btn btn-link p-0 d-lg-none text-secondary me-2"
          onClick={() => setSidebarOpen(prev => !prev)}
          aria-label="Menú"
          style={{ lineHeight: 1 }}
        >
          <span className="material-symbols-outlined" style={{ fontSize: '1.4rem' }}>menu</span>
        </button>

        <Link to="/dashboard" className="topbar-brand">
          <span className="material-symbols-outlined me-2" style={{ fontSize: '1.2rem' }}>
            account_balance
          </span>
          Sistema de Asistencias - UBBJ
        </Link>

        <div className="topbar-spacer" />

        {/* Usuario — solo muestra nombre y rol, sin acción de logout */}
        <div className="topbar-user" style={{ cursor: 'default' }}>
          <div className="topbar-avatar">{initials}</div>
          <div className="topbar-user-info d-none d-sm-flex">
            <span className="topbar-user-name">{user?.fullName ?? 'Usuario'}</span>
            <span className="topbar-user-role">{user?.roleName ?? '—'}</span>
          </div>
        </div>
      </header>

      {/* ── Overlay (móvil) ────────────────────────────────── */}
      {sidebarOpen && (
        <div
          className="d-lg-none"
          onClick={() => setSidebarOpen(false)}
          style={{
            position: 'fixed', inset: 0, zIndex: 1025,
            background: 'rgba(0,0,0,0.5)',
          }}
        />
      )}

      {/* ── Sidebar ────────────────────────────────────────── */}
      <nav className={`sidebar${sidebarOpen ? ' open' : ''}`}>

        {/* Badge de estado del usuario */}
        <div className="px-3 pb-2">
          <span className={`role-badge role-badge-${user?.isAdmin ? 'admin' : 'profesor'}`}>
            {user?.roleName ?? 'Sin rol'}
          </span>
        </div>

        {sections.map(section => (
          <div key={section}>
            <p className="sidebar-section-label">{section}</p>
            {visibleModules
              .filter(m => m.section === section)
              .map(m => (
                <Link
                  key={m.path}
                  to={m.path}
                  className={`sidebar-link${location.pathname === m.path ? ' active' : ''}`}
                  onClick={() => setSidebarOpen(false)}
                >
                  <span className="material-symbols-outlined">{m.icon}</span>
                  {m.label}
                </Link>
              ))}
          </div>
        ))}

        <div className="sidebar-bottom">
          <div className="sidebar-divider" />
          <button className="sidebar-link" onClick={handleLogout}>
            <span className="material-symbols-outlined">logout</span>
            Cerrar Sesión
          </button>
        </div>
      </nav>

      {/* ── Contenido principal ─────────────────────────────── */}
      <main className="main-content">
        <Outlet />
      </main>

    </div>
  );
}
