import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Button, Spinner, Alert } from 'react-bootstrap';
import { useAuth } from '../context/AuthContext';

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000';

export default function ReportsPage() {
  const { token } = useAuth();

  const [groupId, setGroupId]   = useState('GRP001');
  const [year, setYear]         = useState(new Date().getFullYear());
  const [month, setMonth]       = useState(new Date().getMonth() + 1);
  const [loading, setLoading]   = useState(false);
  const [error, setError]       = useState(null);
  const [report, setReport]     = useState(null);

  const MONTHS = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'];

  const fetchReport = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setReport(null);
    try {
      const res = await fetch(`${API_BASE}/reports/group/${groupId}/monthly?year=${year}&month=${month}`, {
        headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail ?? `Error ${res.status}`);
      }
      setReport(await res.json());
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const statCard = (label, value, icon, color = 'var(--on-surface)') => (
    <div style={{ background: 'var(--surface-raised)', border: '1px solid var(--border)', borderRadius: 8, padding: '1rem' }}>
      <div className="d-flex align-items-center gap-2 mb-1">
        <span className="material-symbols-outlined" style={{ fontSize: '1.1rem', color }}>{icon}</span>
        <span style={{ fontSize: '0.72rem', fontWeight: 700, letterSpacing: '1px', textTransform: 'uppercase', color: 'var(--on-surface-dim)' }}>{label}</span>
      </div>
      <div style={{ fontSize: '2rem', fontWeight: 700, fontFamily: 'Instrument Sans, sans-serif', color }}>{value}</div>
    </div>
  );

  return (
    <>
      <div className="page-header">
        <div>
          <Link to="/dashboard" className="page-header-back">
            <span className="material-symbols-outlined" style={{ fontSize: '0.9rem' }}>arrow_back</span>
            Inicio
          </Link>
          <h1 className="headline mb-0" style={{ fontSize: '1.6rem', fontWeight: 700 }}>Reportes y Métricas</h1>
          <p style={{ color: 'var(--on-surface-dim)', fontSize: '0.85rem', marginBottom: 0 }}>
            Genera reportes mensuales de asistencia por grupo y descarga la plantilla Excel institucional.
          </p>
        </div>
      </div>

      <div className="row g-4">
        {/* Parámetros */}
        <div className="col-12 col-lg-4">
          <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 10, padding: '1.5rem' }}>
            <h5 className="headline mb-3" style={{ fontWeight: 700, fontSize: '1rem' }}>
              <span className="material-symbols-outlined me-2" style={{ fontSize: '1.1rem', color: 'var(--primary-light)' }}>tune</span>
              Parámetros del Reporte
            </h5>
            <form onSubmit={fetchReport}>
              <div className="mb-3">
                <label className="form-label" style={{ fontSize: '0.78rem', fontWeight: 700, letterSpacing: '1px', textTransform: 'uppercase', color: 'var(--on-surface-dim)' }}>Grupo</label>
                <input id="input-rep-grupo" type="text" className="form-control bg-dark text-light border-secondary" value={groupId} onChange={e => setGroupId(e.target.value.toUpperCase())} placeholder="Ej: GRP001" required />
              </div>
              <div className="mb-3">
                <label className="form-label" style={{ fontSize: '0.78rem', fontWeight: 700, letterSpacing: '1px', textTransform: 'uppercase', color: 'var(--on-surface-dim)' }}>Mes</label>
                <select id="select-rep-mes" className="form-select bg-dark text-light border-secondary" value={month} onChange={e => setMonth(parseInt(e.target.value))}>
                  {MONTHS.map((m, i) => <option key={i} value={i+1}>{m}</option>)}
                </select>
              </div>
              <div className="mb-3">
                <label className="form-label" style={{ fontSize: '0.78rem', fontWeight: 700, letterSpacing: '1px', textTransform: 'uppercase', color: 'var(--on-surface-dim)' }}>Año</label>
                <input id="input-rep-anio" type="number" min="2020" max="2099" className="form-control bg-dark text-light border-secondary" value={year} onChange={e => setYear(parseInt(e.target.value))} required />
              </div>
              <Button id="btn-generar-reporte" type="submit" variant="danger" className="vault-gradient border-0 w-100" disabled={loading}>
                {loading ? <><Spinner size="sm" animation="border" className="me-2" />Generando...</> : 'Generar Reporte'}
              </Button>
            </form>
          </div>
        </div>

        {/* Resultados */}
        <div className="col-12 col-lg-8">
          {!report && !loading && !error && (
            <div className="d-flex align-items-center justify-content-center h-100" style={{ minHeight: 240, background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 10, color: 'var(--on-surface-dim)' }}>
              <div className="text-center">
                <span className="material-symbols-outlined d-block mb-2" style={{ fontSize: '2.5rem' }}>bar_chart</span>
                <p className="mb-0" style={{ fontSize: '0.9rem' }}>Configura los parámetros y genera el reporte.</p>
              </div>
            </div>
          )}
          {loading && <div className="text-center py-5"><Spinner animation="border" variant="danger" /></div>}
          {error   && <Alert variant="danger">{error}</Alert>}

          {report && !loading && (
            <>
              <div className="mb-3">
                <p style={{ color: 'var(--on-surface-dim)', fontSize: '0.82rem', marginBottom: '0.25rem' }}>
                  Grupo: <strong>{report.group_name ?? groupId}</strong> · {MONTHS[month-1]} {year}
                </p>
              </div>

              {/* Métricas globales */}
              <div className="row g-3 mb-4">
                <div className="col-6 col-sm-4">{statCard('Presentes', report.global_stats?.PRESENT ?? 0, 'check_circle', '#86efac')}</div>
                <div className="col-6 col-sm-4">{statCard('Ausentes',  report.global_stats?.ABSENT  ?? 0, 'cancel', '#fca5a5')}</div>
                <div className="col-6 col-sm-4">{statCard('Retardos',  report.global_stats?.LATE    ?? 0, 'schedule', '#fde68a')}</div>
                <div className="col-6 col-sm-4">{statCard('Justificados', report.global_stats?.JUSTIFIED ?? 0, 'verified', '#93c5fd')}</div>
                <div className="col-6 col-sm-4">{statCard('Puntualidad', `${report.global_stats?.PUNCTUALITY_PERCENTAGE ?? 0}%`, 'trending_up', 'var(--primary-light)')}</div>
                <div className="col-6 col-sm-4">{statCard('Ausentismo', `${report.global_stats?.ABSENT_PERCENTAGE ?? 0}%`, 'trending_down', '#fca5a5')}</div>
              </div>

              {/* Detalle por estudiante */}
              {report.students && report.students.length > 0 && (
                <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 10 }}>
                  <div className="px-3 pt-3 pb-2">
                    <h6 className="headline mb-0" style={{ fontWeight: 700 }}>Desglose por Estudiante</h6>
                  </div>
                  <div className="table-responsive">
                    <table className="table table-dark table-hover mb-0 crud-table">
                      <thead>
                        <tr>
                          <th>Estudiante</th>
                          <th>Presentes</th>
                          <th>Ausentes</th>
                          <th>Retardos</th>
                          <th>Total</th>
                        </tr>
                      </thead>
                      <tbody>
                        {report.students.map(s => (
                          <tr key={s.student_id}>
                            <td style={{ fontWeight: 600 }}>{s.full_name} <span style={{ fontSize: '0.75rem', color: 'var(--on-surface-dim)' }}>({s.nickname ?? s.student_id})</span></td>
                            <td><span className="badge bg-success">{s.stats?.PRESENT ?? 0}</span></td>
                            <td><span className="badge bg-danger">{s.stats?.ABSENT ?? 0}</span></td>
                            <td><span className="badge bg-warning text-dark">{s.stats?.LATE ?? 0}</span></td>
                            <td style={{ color: 'var(--on-surface-dim)' }}>{s.stats?.TOTAL ?? 0}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </>
  );
}
