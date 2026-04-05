import { useState, useEffect, useMemo } from 'react';
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

  // Estados para grupos dinámicos
  const [groups, setGroups] = useState([]);
  const [groupSearch, setGroupSearch] = useState('');
  const [selectedGroupId, setSelectedGroupId] = useState('');
  const [loadingGroups, setLoadingGroups] = useState(false);

  // Cargar grupos al montar
  useEffect(() => {
    const fetchGroups = async () => {
      setLoadingGroups(true);
      try {
        const res = await fetch(`${API_BASE}/groups`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!res.ok) throw new Error('Error al cargar grupos');
        const data = await res.json();
        setGroups(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoadingGroups(false);
      }
    };
    fetchGroups();
  }, [token]);

  // Filtrar grupos por búsqueda (usado solo para poblar el dropdown)
  const filteredGroups = useMemo(() => {
    const s = groupSearch.toLowerCase().trim();
    if (!s) return groups;
    return groups.filter(g => 
      g.id.toLowerCase().includes(s) || 
      g.name.toLowerCase().includes(s)
    );
  }, [groups, groupSearch]);

  const handleSearchChange = (val) => {
    setGroupSearch(val);
    const s = val.toLowerCase().trim();
    if (s) {
      // Intentamos encontrar el mejor match (priorizando empezar con el ID)
      const match = groups.find(g => g.id.toLowerCase().startsWith(s)) ||
                    groups.find(g => g.id.toLowerCase().includes(s) || g.name.toLowerCase().includes(s));
      
      if (match) {
        setSelectedGroupId(match.id);
      }
    }
  };

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
            <p style={{ fontSize: '0.82rem', color: 'var(--on-surface-dim)', marginBottom: '1.2rem' }}>
              Selecciona un grupo para descargar su plantilla <strong>.xlsm</strong>. La macro capturará la hora al escribir <code>1</code>.
            </p>

            <div className="mb-3">
              <label className="form-label small fw-bold text-uppercase opacity-75">1. Buscar Grupo</label>
              <div className="input-group input-group-sm mb-2">
                <span className="input-group-text bg-dark border-secondary text-secondary">
                  <span className="material-symbols-outlined" style={{ fontSize: '1.1rem' }}>search</span>
                </span>
                <input
                  type="text"
                  className="form-control bg-dark text-light border-secondary"
                  placeholder="ID o nombre del grupo..."
                  value={groupSearch}
                  onChange={e => handleSearchChange(e.target.value)}
                />
              </div>

              <label className="form-label small fw-bold text-uppercase opacity-75">2. Seleccionar de la lista</label>
              <select
                className="form-select form-select-sm bg-dark text-light border-secondary mb-3"
                value={selectedGroupId}
                onChange={e => setSelectedGroupId(e.target.value)}
                disabled={loadingGroups}
              >
                <option value="">{loadingGroups ? 'Cargando grupos...' : '-- Selecciona un grupo --'}</option>
                {filteredGroups.map(g => (
                  <option key={g.id} value={g.id}>
                    {g.id} - {g.name}
                  </option>
                ))}
                {!loadingGroups && groupSearch.trim() && filteredGroups.length === 0 && (
                  <option disabled>No se encontraron resultados</option>
                )}
              </select>

              <Button
                variant="outline-danger"
                className="w-100 btn-sm d-flex align-items-center justify-content-center"
                disabled={!selectedGroupId}
                onClick={() => handleDownloadTemplate(selectedGroupId)}
              >
                <span className="material-symbols-outlined me-2" style={{ fontSize: '1.1rem' }}>download</span>
                Descargar Plantilla (.xlsm)
              </Button>
            </div>

            <p className="mt-2 mb-0" style={{ fontSize: '0.75rem', color: 'var(--on-surface-dim)' }}>
              Solo se muestran los grupos registrados en el sistema.
            </p>
          </div>
        </div>
      </div>
    </>
  );
}
