import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Modal, Button, Form, Spinner, Alert } from 'react-bootstrap';
import { useAuth } from '../context/AuthContext';
import { apiFetch } from '../api/apiClient';

export default function EnrollmentsPage() {
  const { user, token } = useAuth();
  const isAdmin = user?.isAdmin ?? false;

  const [enrollments, setEnrollments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [editing, setEditing] = useState(null);
  const [saving, setSaving] = useState(false);
  const [formError, setFormError] = useState(null);

  const emptyForm = { enrollment_date: '', student_id: '', group_id: '' };
  const [form, setForm] = useState(emptyForm);

  const loadEnrollments = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiFetch('/enrollments', { token });
      setEnrollments(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadEnrollments(); }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const openCreate = () => {
    setEditing(null);
    setForm(emptyForm);
    setFormError(null);
    setShowModal(true);
  };

  const openEdit = (en) => {
    setEditing(en);
    setForm({ enrollment_date: en.enrollment_date, student_id: en.student_id, group_id: en.group_id });
    setFormError(null);
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (!window.confirm(`¿Eliminar la inscripción #${id}?`)) return;
    try {
      await apiFetch(`/enrollments/${id}`, { method: 'DELETE', token });
      await loadEnrollments();
    } catch (e) {
      alert(`Error: ${e.message}`);
    }
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    setFormError(null);
    try {
      if (editing) {
        await apiFetch(`/enrollments/${editing.id}`, { method: 'PUT', token, body: form });
      } else {
        await apiFetch('/enrollments', { method: 'POST', token, body: form });
      }
      setShowModal(false);
      await loadEnrollments();
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
          <h1 className="headline mb-0" style={{ fontSize: '1.6rem', fontWeight: 700 }}>Inscripciones</h1>
          <p style={{ color: 'var(--on-surface-dim)', fontSize: '0.85rem', marginBottom: 0 }}>
            {isAdmin ? 'Administra las inscripciones de alumnos a grupos.' : 'Inscripciones de alumnos. Solo lectura.'}
          </p>
        </div>
        {isAdmin && (
          <Button id="btn-nueva-inscripcion" variant="danger"  onClick={openCreate}>
            <span className="material-symbols-outlined me-2" style={{ fontSize: '1rem' }}>add</span>
            Nueva Inscripción
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
                <th>Estudiante (ID)</th>
                <th>Grupo (ID)</th>
                <th>Fecha de Inscripción</th>
                {isAdmin && <th className="text-end">Acciones</th>}
              </tr>
            </thead>
            <tbody>
              {enrollments.length === 0 ? (
                <tr><td colSpan={isAdmin ? 5 : 4} className="text-center py-5" style={{ color: 'var(--on-surface-dim)' }}>Sin inscripciones registradas</td></tr>
              ) : (
                enrollments.map(en => (
                  <tr key={en.id}>
                    <td style={{ color: 'var(--on-surface-dim)' }}>{en.id}</td>
                    <td><code style={{ color: 'var(--primary-light)' }}>{en.student_id}</code></td>
                    <td><code style={{ color: 'var(--primary-light)' }}>{en.group_id}</code></td>
                    <td style={{ fontSize: '0.85rem', color: 'var(--on-surface-dim)' }}>{en.enrollment_date}</td>
                    {isAdmin && (
                      <td className="text-end">
                        <button id={`btn-editar-insc-${en.id}`} className="btn btn-sm btn-outline-secondary me-2" onClick={() => openEdit(en)}>
                          <span className="material-symbols-outlined" style={{ fontSize: '0.9rem' }}>edit</span>
                        </button>
                        <button id={`btn-eliminar-insc-${en.id}`} className="btn btn-sm btn-outline-danger" onClick={() => handleDelete(en.id)}>
                          <span className="material-symbols-outlined" style={{ fontSize: '0.9rem' }}>delete</span>
                        </button>
                      </td>
                    )}
                  </tr>
                ))
              )}
            </tbody>
          </table>
          <div className="px-3 py-2" style={{ color: 'var(--on-surface-dim)', fontSize: '0.8rem' }}>
            {enrollments.length} inscripciones
          </div>
        </div>
      )}

      {isAdmin && (
        <Modal show={showModal} onHide={() => setShowModal(false)} centered data-bs-theme="dark">
          <Modal.Header closeButton style={{ background: 'var(--surface)', borderColor: 'var(--border)' }}>
            <Modal.Title className="headline" style={{ fontSize: '1.1rem' }}>
              {editing ? 'Editar Inscripción' : 'Nueva Inscripción'}
            </Modal.Title>
          </Modal.Header>
          <Form onSubmit={handleSave}>
            <Modal.Body style={{ background: 'var(--surface)' }}>
              {formError && <Alert variant="danger" className="py-2">{formError}</Alert>}
              <Form.Group className="mb-3">
                <Form.Label>ID del Estudiante</Form.Label>
                <Form.Control id="input-insc-estudiante" type="text" placeholder="Ej: EST001" value={form.student_id} onChange={e => setForm(f => ({ ...f, student_id: e.target.value }))} required className="bg-dark text-light border-secondary" />
              </Form.Group>
              <Form.Group className="mb-3">
                <Form.Label>ID del Grupo</Form.Label>
                <Form.Control id="input-insc-grupo" type="text" placeholder="Ej: GRP001" value={form.group_id} onChange={e => setForm(f => ({ ...f, group_id: e.target.value }))} required className="bg-dark text-light border-secondary" />
              </Form.Group>
              <Form.Group className="mb-1">
                <Form.Label>Fecha de Inscripción</Form.Label>
                <Form.Control id="input-insc-fecha" type="date" value={form.enrollment_date} onChange={e => setForm(f => ({ ...f, enrollment_date: e.target.value }))} required className="bg-dark text-light border-secondary" />
              </Form.Group>
            </Modal.Body>
            <Modal.Footer style={{ background: 'var(--surface)', borderColor: 'var(--border)' }}>
              <Button variant="outline-secondary" onClick={() => setShowModal(false)}>Cancelar</Button>
              <Button id="btn-guardar-insc" type="submit" variant="danger"  disabled={saving}>
                {saving ? <Spinner size="sm" animation="border" /> : (editing ? 'Guardar Cambios' : 'Inscribir')}
              </Button>
            </Modal.Footer>
          </Form>
        </Modal>
      )}
    </>
  );
}
