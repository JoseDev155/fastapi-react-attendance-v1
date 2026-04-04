import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

// Definición de módulos del hub: se muestran según el rol
const ADMIN_MODULES = [
  {
    path: '/dashboard/asistencias',
    icon: 'assignment_turned_in',
    title: 'Asistencias',
    desc: 'Consulta y administra los registros de asistencia de todos los grupos.',
  },
  {
    path: '/dashboard/estudiantes',
    icon: 'school',
    title: 'Estudiantes',
    desc: 'Expedientes académicos: alta, edición y baja de alumnos.',
  },
  {
    path: '/dashboard/grupos',
    icon: 'groups',
    title: 'Grupos',
    desc: 'Crea y administra los grupos asignados a cada profesor.',
  },
  {
    path: '/dashboard/ciclos',
    icon: 'event_repeat',
    title: 'Ciclos Académicos',
    desc: 'Gestiona los periodos escolares: apertura, cierre y planificación.',
  },
  {
    path: '/dashboard/inscripciones',
    icon: 'how_to_reg',
    title: 'Inscripciones',
    desc: 'Registra y actualiza las inscripciones de alumnos a grupos.',
  },
  {
    path: '/dashboard/horarios',
    icon: 'schedule',
    title: 'Horarios',
    desc: 'Configura los horarios de clase y tolerancias de llegada.',
  },
  {
    path: '/dashboard/subir-asistencias',
    icon: 'upload_file',
    title: 'Subir Asistencias (Excel)',
    desc: 'Importa listas de asistencia desde la plantilla institucional.',
  },
  {
    path: '/dashboard/reportes',
    icon: 'bar_chart',
    title: 'Reportes y Métricas',
    desc: 'Genera reportes mensuales por grupo y descarga la plantilla Excel.',
  },
  {
    path: '/dashboard/usuarios',
    icon: 'manage_accounts',
    title: 'Usuarios del Sistema',
    desc: 'Administra cuentas de profesores y administradores.',
  },
];

const PROFESOR_MODULES = [
  {
    path: '/dashboard/asistencias',
    icon: 'assignment_turned_in',
    title: 'Asistencias',
    desc: 'Consulta los registros de asistencia de tus grupos.',
  },
  {
    path: '/dashboard/grupos',
    icon: 'groups',
    title: 'Mis Grupos',
    desc: 'Visualiza los grupos que tienes asignados.',
  },
  {
    path: '/dashboard/estudiantes',
    icon: 'school',
    title: 'Estudiantes',
    desc: 'Consulta la información de los alumnos inscritos en tus grupos.',
  },
  {
    path: '/dashboard/ciclos',
    icon: 'event_repeat',
    title: 'Ciclos Académicos',
    desc: 'Consulta los periodos escolares activos.',
  },
  {
    path: '/dashboard/inscripciones',
    icon: 'how_to_reg',
    title: 'Inscripciones',
    desc: 'Consulta las inscripciones de alumnos en tus grupos.',
  },
  {
    path: '/dashboard/horarios',
    icon: 'schedule',
    title: 'Horarios',
    desc: 'Revisa los horarios configurados para tus grupos.',
  },
];

export default function HomeDashboardPage() {
  const { user } = useAuth();
  const modules = user?.isAdmin ? ADMIN_MODULES : PROFESOR_MODULES;

  const greeting = () => {
    const h = new Date().getHours();
    if (h < 12) return 'Buenos días';
    if (h < 19) return 'Buenas tardes';
    return 'Buenas noches';
  };

  return (
    <>
      {/* Cabecera de bienvenida */}
      <div className="mb-4">
        <p className="mb-1" style={{ fontSize: '0.8rem', fontWeight: 700, letterSpacing: '1px', textTransform: 'uppercase', color: 'var(--on-surface-dim)' }}>
          <span className="material-symbols-outlined me-1" style={{ fontSize: '0.9rem' }}>circle</span>
          {user?.roleName ?? 'Usuario'} · Sistema activo
        </p>
        <h1 className="headline mb-1" style={{ fontSize: '1.9rem', fontWeight: 700 }}>
          {greeting()}, {user?.firstName ?? 'usuario'}
        </h1>
        <p style={{ color: 'var(--on-surface-dim)', fontSize: '0.9rem' }}>
          Universidades para el Bienestar Benito Juárez García — Panel de Control
        </p>
      </div>

      {/* Grid de módulos */}
      <div className="row g-3">
        {modules.map(m => (
          <div key={m.path} className="col-12 col-sm-6 col-xl-4">
            <Link to={m.path} className="module-card">
              <div className="module-card-icon">
                <span className="material-symbols-outlined">{m.icon}</span>
              </div>
              <div className="module-card-title">{m.title}</div>
              <div className="module-card-desc">{m.desc}</div>
            </Link>
          </div>
        ))}
      </div>
    </>
  );
}
