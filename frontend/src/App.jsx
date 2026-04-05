import { Routes, Route, Navigate } from 'react-router-dom';
import { Spinner } from 'react-bootstrap';
import { AuthProvider, useAuth } from './context/AuthContext';
import MainLayout from './layouts/MainLayout';

// Páginas públicas
import LoginPage from './pages/LoginPage';

// Páginas protegidas
import HomeDashboardPage from './pages/HomeDashboardPage';
import AttendancePage from './pages/AttendancePage';
import UploadAttendancePage from './pages/UploadAttendancePage';
import StudentsPage from './pages/StudentsPage';
import GroupsPage from './pages/GroupsPage';
import AcademicCyclesPage from './pages/AcademicCyclesPage';
import UsersPage from './pages/UsersPage';
import EnrollmentsPage from './pages/EnrollmentsPage';
import SchedulesPage from './pages/SchedulesPage';
import ReportsPage from './pages/ReportsPage';

// Guarda de ruta: redirige al login si no hay token válido.
// Mientras el contexto resuelve los datos del usuario muestra un spinner.
function ProtectedRoute({ children }) {
  const { token, ready } = useAuth();

  if (!ready) {
    return (
      <div
        className="d-flex align-items-center justify-content-center min-vh-100"
        style={{ background: 'var(--background)' }}
      >
        <Spinner animation="border" variant="danger" />
      </div>
    );
  }

  if (!token) return <Navigate to="/login" replace />;
  return children;
}

function App() {
  return (
    <AuthProvider>
      <Routes>
        {/* Ruta pública */}
        <Route path="/login" element={<LoginPage />} />

        {/* Rutas protegidas bajo el layout compartido */}
        <Route
          element={
            <ProtectedRoute>
              <MainLayout />
            </ProtectedRoute>
          }
        >
          <Route path="/dashboard" element={<HomeDashboardPage />} />
          <Route path="/dashboard/asistencias" element={<AttendancePage />} />
          <Route path="/dashboard/subir-asistencias" element={<UploadAttendancePage />} />
          <Route path="/dashboard/estudiantes" element={<StudentsPage />} />
          <Route path="/dashboard/grupos" element={<GroupsPage />} />
          <Route path="/dashboard/ciclos" element={<AcademicCyclesPage />} />
          <Route path="/dashboard/inscripciones" element={<EnrollmentsPage />} />
          <Route path="/dashboard/horarios" element={<SchedulesPage />} />
          <Route path="/dashboard/usuarios" element={<UsersPage />} />
          <Route path="/dashboard/reportes" element={<ReportsPage />} />
        </Route>

        {/* Ruta comodín → Login */}
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </AuthProvider>
  );
}

export default App;
