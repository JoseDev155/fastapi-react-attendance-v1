import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Spinner, Alert } from 'react-bootstrap';
import { useAuth } from '../context/AuthContext';
import { apiFetch } from '../api/apiClient';

const STATUS_LABELS = { PRESENT: 'Presente', ABSENT: 'Ausente', LATE: 'Retardo', JUSTIFIED: 'Justificado', LEFT_EARLY: 'Salió Temprano' };
const STATUS_BADGE = { PRESENT: 'bg-success', ABSENT: 'bg-danger', LATE: 'bg-warning text-dark', JUSTIFIED: 'bg-info text-dark', LEFT_EARLY: 'bg-secondary' };

export default function AttendancePage() {
  const { token } = useAuth();
  const [attendances, setAttendances] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [groupId, setGroupId] = useState('GRP001');
  const [groupInput, setGroupInput] = useState('GRP001');

  const load = async (gid) => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiFetch(`/attendances/group/${gid}/calculated`, { token });
      setAttendances(Array.isArray(data) ? data : []);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(groupId); }, [groupId]); // eslint-disable-line react-hooks/exhaustive-deps

  const handleFilter = (e) => {
    e.preventDefault();
    const trimmed = groupInput.trim().toUpperCase();
    if (trimmed) setGroupId(trimmed);
  };

  return (
    <>
      <div className="page-header">
        <div>
          <Link to="/dashboard" className="page-header-back">
            <span className="material-symbols-outlined" style={{ fontSize: '0.9rem' }}>arrow_back</span>
            Inicio
          </Link>
          <h1 className="headline mb-0" style={{ fontSize: '1.6rem', fontWeight: 700 }}>Registros de Asistencia</h1>
          <p style={{ color: 'var(--on-surface-dim)', fontSize: '0.85rem', marginBottom: 0 }}>
            Consulta los registros de llegada por grupo.
          </p>
        </div>
      </div>

      {/* Filtro de grupo */}
      <form className="mb-3 d-flex gap-2 align-items-center" onSubmit={handleFilter} style={{ maxWidth: 360 }}>
        <div className="input-group">
          <span className="input-group-text bg-dark border-secondary text-secondary">
            <span className="material-symbols-outlined" style={{ fontSize: '1.1rem' }}>groups</span>
          </span>
          <input
            id="input-filtro-grupo"
            type="text"
            className="form-control bg-dark text-light border-secondary"
            placeholder="ID del grupo (Ej: GRP001)"
            value={groupInput}
            onChange={e => setGroupInput(e.target.value)}
          />
        </div>
        <button id="btn-filtrar-grupo" type="submit" className="btn btn-danger vault-gradient border-0 text-nowrap">
          Filtrar
        </button>
      </form>

      {loading && <div className="text-center py-5"><Spinner animation="border" variant="danger" /></div>}
      {error && <Alert variant="danger">{error}</Alert>}

      {!loading && !error && (
        <div className="table-responsive" style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 10 }}>
          <table className="table table-dark table-hover mb-0 crud-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Inscripción</th>
                <th>Fecha</th>
                <th>Hora de Llegada</th>
                <th>Estado Calculado</th>
                <th>Notas</th>
              </tr>
            </thead>
            <tbody>
              {attendances.length === 0 ? (
                <tr><td colSpan={6} className="text-center py-5" style={{ color: 'var(--on-surface-dim)' }}>Sin registros para el grupo <strong>{groupId}</strong></td></tr>
              ) : (
                attendances.map(a => (
                  <tr key={a.id}>
                    <td style={{ color: 'var(--on-surface-dim)' }}>{a.id}</td>
                    <td><code style={{ color: 'var(--primary-light)' }}>{a.enrollment_id}</code></td>
                    <td style={{ fontSize: '0.85rem' }}>{a.attendance_date}</td>
                    <td style={{ fontWeight: 600 }}>{a.arrival_time ?? <span style={{ color: 'var(--on-surface-dim)' }}>—</span>}</td>
                    <td>
                      {a.status ? (
                        <span className={`badge ${STATUS_BADGE[a.status] ?? 'bg-secondary'}`}>
                          {STATUS_LABELS[a.status] ?? a.status}
                        </span>
                      ) : (
                        <span className="badge bg-secondary">Sin horario</span>
                      )}
                    </td>
                    <td style={{ fontSize: '0.8rem', color: 'var(--on-surface-dim)' }}>{a.notes ?? '—'}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
          <div className="px-3 py-2" style={{ color: 'var(--on-surface-dim)', fontSize: '0.8rem' }}>
            {attendances.length} registros · Grupo <strong>{groupId}</strong>
          </div>
        </div>
      )}
    </>
  );
}
