import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Modal, Button, Form, Spinner, Alert } from 'react-bootstrap';
import { useAuth } from '../context/AuthContext';
import { apiFetch } from '../api/apiClient';

export default function AcademicCyclesPage() {
  const { user, token } = useAuth();
  const isAdmin = user?.isAdmin ?? false;

  const [cycles, setCycles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [editing, setEditing] = useState(null);
  const [saving, setSaving] = useState(false);
  const [formError, setFormError] = useState(null);

  const emptyForm = { cycle_name: '', cycle_year: new Date().getFullYear() };
  const [form, setForm] = useState(emptyForm);

  const loadCycles = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiFetch('/academic-cycles', { token });
      setCycles(Array.isArray(data) ? data : []);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadCycles(); }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const openCreate = () => {
    setEditing(null);
    setForm(emptyForm);
    setFormError(null);
    setShowModal(true);
  };

  const openEdit = (c) => {
    setEditing(c);
    // Extract year from date string (e.g. "2025-01-01" -> 2025)
    let year = new Date().getFullYear();
    if (c.cycle_year) {
      const parsedYear = parseInt(c.cycle_year.split('-')[0], 10);
      if (!isNaN(parsedYear)) year = parsedYear;
    }
    setForm({ cycle_name: c.cycle_name, cycle_year: year });
    setFormError(null);
    setShowModal(true);
  };

  const handleDelete = async (id, name) => {
    if (!window.confirm(`¿Eliminar el ciclo "${name}"?`)) return;
    try {
      await apiFetch(`/academic-cycles/${id}`, { method: 'DELETE', token });
      await loadCycles();
    } catch (e) {
      alert(`Error: ${e.message}`);
    }
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    setFormError(null);

    // Backend expects 'cycle_year' as a date string. We convert the year integer to 'YYYY-01-01'.
    const payload = {
      cycle_name: form.cycle_name,
      cycle_year: `${form.cycle_year}-01-01`
    };

    try {
      if (editing) {
        await apiFetch(`/academic-cycles/${editing.id}`, { method: 'PUT', token, body: payload });
      } else {
        await apiFetch('/academic-cycles', { method: 'POST', token, body: payload });
      }
      setShowModal(false);
      await loadCycles();
    } catch (e) {
      setFormError(e.message);
    } finally {
      setSaving(false);
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
          <h1 className="headline mb-0" style={{ fontSize: '1.6rem', fontWeight: 700 }}>Ciclos Académicos</h1>
          <p style={{ color: 'var(--on-surface-dim)', fontSize: '0.85rem', marginBottom: 0 }}>
            {isAdmin ? 'Administra los periodos escolares institucionales.' : 'Periodos escolares disponibles. Solo lectura.'}
          </p>
        </div>
        {isAdmin && (
          <Button id="btn-nuevo-ciclo" variant="danger"  onClick={openCreate}>
            <span className="material-symbols-outlined me-2" style={{ fontSize: '1rem' }}>add</span>
            Nuevo Ciclo
          </Button>
        )}
      </div>

      {loading && <div className="text-center py-5"><Spinner animation="border" variant="danger" /></div>}
      {error && <Alert variant="danger">{error}</Alert>}

      {!loading && !error && (
        <div className="table-responsive" style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 10 }}>
          <table className="table table-dark table-hover mb-0 crud-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Nombre del Ciclo</th>
                <th>Año</th>
                {isAdmin && <th className="text-end">Acciones</th>}
              </tr>
            </thead>
            <tbody>
              {cycles.length === 0 ? (
                <tr><td colSpan={isAdmin ? 4 : 3} className="text-center py-5" style={{ color: 'var(--on-surface-dim)' }}>Sin ciclos registrados</td></tr>
              ) : (
                cycles.map(c => (
                  <tr key={c.id}>
                    <td style={{ color: 'var(--on-surface-dim)' }}>{c.id}</td>
                    <td style={{ fontWeight: 600 }}>{c.cycle_name}</td>
                    <td>{c.cycle_year ? c.cycle_year.split('-')[0] : '—'}</td>
                    {isAdmin && (
                      <td className="text-end">
                        <button id={`btn-editar-ciclo-${c.id}`} className="btn btn-sm btn-outline-secondary me-2" onClick={() => openEdit(c)}>
                          <span className="material-symbols-outlined" style={{ fontSize: '0.9rem' }}>edit</span>
                        </button>
                        <button id={`btn-eliminar-ciclo-${c.id}`} className="btn btn-sm btn-outline-danger" onClick={() => handleDelete(c.id, c.cycle_name)}>
                          <span className="material-symbols-outlined" style={{ fontSize: '0.9rem' }}>delete</span>
                        </button>
                      </td>
                    )}
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}

      {isAdmin && (
        <Modal show={showModal} onHide={() => setShowModal(false)} centered data-bs-theme="dark">
          <Modal.Header closeButton style={{ background: 'var(--surface)', borderColor: 'var(--border)' }}>
            <Modal.Title className="headline" style={{ fontSize: '1.1rem' }}>
              {editing ? 'Editar Ciclo' : 'Nuevo Ciclo Académico'}
            </Modal.Title>
          </Modal.Header>
          <Form onSubmit={handleSave}>
            <Modal.Body style={{ background: 'var(--surface)' }}>
              {formError && <Alert variant="danger" className="py-2">{formError}</Alert>}
              <Form.Group className="mb-3">
                <Form.Label>Nombre del Ciclo</Form.Label>
                <Form.Control id="input-ciclo-nombre" type="text" placeholder="Ej: Primavera 2025" value={form.cycle_name} onChange={e => setForm(f => ({ ...f, cycle_name: e.target.value }))} required className="bg-dark text-light border-secondary" />
              </Form.Group>
              <Form.Group className="mb-3">
                <Form.Label>Año Académico</Form.Label>
                <Form.Control id="input-ciclo-anio" type="number" min="2020" max="2099" value={form.cycle_year} onChange={e => setForm(f => ({ ...f, cycle_year: parseInt(e.target.value) || new Date().getFullYear() }))} required className="bg-dark text-light border-secondary" />
              </Form.Group>
            </Modal.Body>
            <Modal.Footer style={{ background: 'var(--surface)', borderColor: 'var(--border)' }}>
              <Button variant="outline-secondary" onClick={() => setShowModal(false)}>Cancelar</Button>
              <Button id="btn-guardar-ciclo" type="submit" variant="danger"  disabled={saving}>
                {saving ? <Spinner size="sm" animation="border" /> : (editing ? 'Guardar Cambios' : 'Crear Ciclo')}
              </Button>
            </Modal.Footer>
          </Form>
        </Modal>
      )}
    </>
  );
}
