import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Button, Alert, Spinner } from 'react-bootstrap';
import { useAuth } from '../context/AuthContext';
import { API_BASE } from '../config';


export default function UploadAttendancePage() {
  const { token } = useAuth();
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    setResult(null);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch(`${API_BASE}/uploads/attendance-excel`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` },
        body: formData,
      });
      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail ?? `Error ${res.status}`);
      }
      const data = await res.json();
      setResult(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadTemplate = async (groupId) => {
    try {
      const res = await fetch(`${API_BASE}/exports/attendance-template/${groupId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error(`Error ${res.status}`);
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `Plantilla_Asistencia_${groupId}.xlsm`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (e) {
      alert(`Error al descargar plantilla: ${e.message}`);
    }
  };

  return (
    <>
      <div className="page-header">
        <div>
          <Link to="/dashboard" className="page-header-back">
            <span className="material-symbols-outlined" style={{ fontSize: '0.9rem' }}>arrow_back</span>
            Inicio
          </Link>
          <h1 className="headline mb-0" style={{ fontSize: '1.6rem', fontWeight: 700 }}>Subir Asistencias (Excel)</h1>
          <p style={{ color: 'var(--on-surface-dim)', fontSize: '0.85rem', marginBottom: 0 }}>
            Importa las horas de llegada desde la plantilla institucional. Las celdas de cada día deben contener la hora en formato HH:MM.
          </p>
        </div>
      </div>

      <div className="row g-4">
        {/* Panel de carga */}
        <div className="col-12 col-lg-7">
          <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 10, padding: '1.5rem' }}>
            <h5 className="headline mb-3" style={{ fontWeight: 700 }}>
              <span className="material-symbols-outlined me-2" style={{ fontSize: '1.2rem', color: 'var(--primary-light)' }}>upload_file</span>
              Importar Archivo
            </h5>
            <form onSubmit={handleSubmit}>
              <div className="mb-3">
                <label htmlFor="input-archivo-excel" className="form-label" style={{ fontSize: '0.85rem', color: 'var(--on-surface-dim)', fontWeight: 600 }}>
                  ARCHIVO .XLSM o .XLSX (Plantilla de Asistencia)
                </label>
                <input
                  id="input-archivo-excel"
                  type="file"
                  accept=".xlsm,.xlsx"
                  className="form-control bg-dark text-light border-secondary"
                  onChange={e => { setFile(e.target.files[0]); setResult(null); setError(null); }}
                  required
                />
              </div>
              <Button id="btn-subir-excel" type="submit" variant="danger" className="w-100" disabled={loading || !file}>
                {loading
                  ? <><Spinner size="sm" animation="border" className="me-2" />Procesando...</>
                  : <><span className="material-symbols-outlined me-2" style={{ fontSize: '1rem' }}>cloud_upload</span>Subir y Procesar</>
                }
              </Button>
            </form>

            {/* Resultado */}
            {result && (
              <Alert variant="success" className="mt-3 mb-0">
                <p className="mb-1 fw-bold">✓ Archivo procesado correctamente</p>
                <div className="d-flex gap-3" style={{ fontSize: '0.85rem' }}>
                  <span>Insertados: <strong>{result.inserted}</strong></span>
                  <span>Actualizados: <strong>{result.updated}</strong></span>
                  <span>Omitidos: <strong>{result.skipped}</strong></span>
                </div>
                <p className="mb-0 mt-1" style={{ fontSize: '0.8rem', opacity: 0.75 }}>
                  Periodo: {result.received_month}/{result.received_year}
                </p>
              </Alert>
            )}
            {error && <Alert variant="danger" className="mt-3 mb-0">{error}</Alert>}
          </div>
        </div>

        {/* Panel de descarga de plantilla */}
        <div className="col-12 col-lg-5">
          <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 10, padding: '1.5rem' }}>
            <h5 className="headline mb-1" style={{ fontWeight: 700 }}>
              <span className="material-symbols-outlined me-2" style={{ fontSize: '1.2rem', color: 'var(--primary-light)' }}>download</span>
              Descargar Plantilla
            </h5>
            <p style={{ fontSize: '0.82rem', color: 'var(--on-surface-dim)', marginBottom: '1rem' }}>
              Descarga la plantilla <strong>.xlsm</strong> con macros pre-instaladas. Escribe <code>1</code> en la celda del alumno para que la macro capture la hora automáticamente.
            </p>
            <div className="d-flex gap-2 flex-wrap">
              {['GRP001', 'GRP002', 'GRP003', 'GRP004', 'GRP005', 'GRP006', 'GRP007'].map(g => (
                <button
                  key={g}
                  id={`btn-plantilla-${g}`}
                  className="btn btn-sm btn-outline-secondary"
                  onClick={() => handleDownloadTemplate(g)}
                >
                  {g}
                </button>
              ))}
            </div>
            <p className="mt-2 mb-0" style={{ fontSize: '0.75rem', color: 'var(--on-surface-dim)' }}>
              Los IDs de grupo disponibles dependen de los registrados en el sistema.
            </p>
          </div>
        </div>
      </div>
    </>
  );
}
