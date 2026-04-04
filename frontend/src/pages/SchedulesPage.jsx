import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Modal, Button, Form, Spinner, Alert } from 'react-bootstrap';
import { useAuth } from '../context/AuthContext';
import { apiFetch } from '../api/apiClient';

const DAYS = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'];

export default function SchedulesPage() {
  const { user, token } = useAuth();
  const isAdmin = user?.isAdmin ?? false;

  const [schedules, setSchedules] = useState([]);
  const [loading, setLoading]     = useState(true);
  const [error, setError]         = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [editing, setEditing]     = useState(null);
  const [saving, setSaving]       = useState(false);
  const [formError, setFormError] = useState(null);

  const emptyForm = { id: '', day_of_week: 0, start_time: '', end_time: '', max_entry_minutes: 5, minutes_to_be_late: 15, group_id: '' };
  const [form, setForm] = useState(emptyForm);

  const loadSchedules = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiFetch('/schedules', { token });
      setSchedules(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadSchedules(); }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const openCreate = () => {
    setEditing(null);
    setForm(emptyForm);
    setFormError(null);
    setShowModal(true);
  };

  const openEdit = (s) => {
    setEditing(s);
    setForm({ id: s.id, day_of_week: s.day_of_week, start_time: s.start_time, end_time: s.end_time, max_entry_minutes: s.max_entry_minutes, minutes_to_be_late: s.minutes_to_be_late, group_id: s.group_id });
    setFormError(null);
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (!window.confirm(`¿Eliminar el horario "${id}"?`)) return;
    try {
      await apiFetch(`/schedules/${id}`, { method: 'DELETE', token });
      await loadSchedules();
    } catch (e) {
      alert(`Error: ${e.message}`);
    }
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    setFormError(null);
    const body = { ...form, day_of_week: parseInt(form.day_of_week), max_entry_minutes: parseInt(form.max_entry_minutes), minutes_to_be_late: parseInt(form.minutes_to_be_late) };
    try {
      if (editing) {
        const { id: _id, ...rest } = body;
        await apiFetch(`/schedules/${editing.id}`, { method: 'PUT', token, body: rest });
      } else {
        await apiFetch('/schedules', { method: 'POST', token, body });
      }
      setShowModal(false);
      await loadSchedules();
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
          <h1 className="headline mb-0" style={{ fontSize: '1.6rem', fontWeight: 700 }}>Horarios de Clase</h1>
          <p style={{ color: 'var(--on-surface-dim)', fontSize: '0.85rem', marginBottom: 0 }}>
            {isAdmin ? 'Configura los horarios y tolerancias de asistencia por grupo.' : 'Horarios asignados a los grupos. Solo lectura.'}
          </p>
        </div>
        {isAdmin && (
          <Button id="btn-nuevo-horario" variant="danger" className="vault-gradient border-0" onClick={openCreate}>
            <span className="material-symbols-outlined me-2" style={{ fontSize: '1rem' }}>add</span>
            Nuevo Horario
          </Button>
        )}
      </div>

      {loading && <div className="text-center py-5"><Spinner animation="border" variant="danger" /></div>}
      {error   && <Alert variant="danger">{error}</Alert>}

      {!loading && !error && (
        <div className="table-responsive" style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 10 }}>
          <table className="table table-dark table-hover mb-0 crud-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Grupo</th>
                <th>Día</th>
                <th>Hora Inicio</th>
                <th>Hora Fin</th>
                <th>Tolerancia (min)</th>
                {isAdmin && <th className="text-end">Acciones</th>}
              </tr>
            </thead>
            <tbody>
              {schedules.length === 0 ? (
                <tr><td colSpan={isAdmin ? 7 : 6} className="text-center py-5" style={{ color: 'var(--on-surface-dim)' }}>Sin horarios registrados</td></tr>
              ) : (
                schedules.map(s => (
                  <tr key={s.id}>
                    <td><code style={{ color: 'var(--primary-light)', fontSize: '0.8rem' }}>{s.id}</code></td>
                    <td><code style={{ color: 'var(--primary-light)' }}>{s.group_id}</code></td>
                    <td>{DAYS[s.day_of_week] ?? s.day_of_week}</td>
                    <td>{s.start_time}</td>
                    <td>{s.end_time}</td>
                    <td style={{ color: 'var(--on-surface-dim)' }}>{s.minutes_to_be_late} min</td>
                    {isAdmin && (
                      <td className="text-end">
                        <button id={`btn-editar-hor-${s.id}`} className="btn btn-sm btn-outline-secondary me-2" onClick={() => openEdit(s)}>
                          <span className="material-symbols-outlined" style={{ fontSize: '0.9rem' }}>edit</span>
                        </button>
                        <button id={`btn-eliminar-hor-${s.id}`} className="btn btn-sm btn-outline-danger" onClick={() => handleDelete(s.id)}>
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
              {editing ? 'Editar Horario' : 'Nuevo Horario'}
            </Modal.Title>
          </Modal.Header>
          <Form onSubmit={handleSave}>
            <Modal.Body style={{ background: 'var(--surface)' }}>
              {formError && <Alert variant="danger" className="py-2">{formError}</Alert>}
              {!editing && (
                <Form.Group className="mb-3">
                  <Form.Label>ID del Horario</Form.Label>
                  <Form.Control id="input-hor-id" type="text" placeholder="Ej: SCH001" value={form.id} onChange={e => setForm(f => ({ ...f, id: e.target.value }))} required className="bg-dark text-light border-secondary" />
                </Form.Group>
              )}
              <Form.Group className="mb-3">
                <Form.Label>Grupo</Form.Label>
                <Form.Control id="input-hor-grupo" type="text" placeholder="Ej: GRP001" value={form.group_id} onChange={e => setForm(f => ({ ...f, group_id: e.target.value }))} required className="bg-dark text-light border-secondary" />
              </Form.Group>
              <Form.Group className="mb-3">
                <Form.Label>Día de la Semana</Form.Label>
                <Form.Select id="select-hor-dia" value={form.day_of_week} onChange={e => setForm(f => ({ ...f, day_of_week: e.target.value }))} className="bg-dark text-light border-secondary">
                  {DAYS.map((d, i) => <option key={i} value={i}>{d}</option>)}
                </Form.Select>
              </Form.Group>
              <div className="row g-2 mb-3">
                <div className="col-6">
                  <Form.Label>Hora de Inicio</Form.Label>
                  <Form.Control id="input-hor-inicio" type="time" value={form.start_time} onChange={e => setForm(f => ({ ...f, start_time: e.target.value }))} required className="bg-dark text-light border-secondary" />
                </div>
                <div className="col-6">
                  <Form.Label>Hora de Fin</Form.Label>
                  <Form.Control id="input-hor-fin" type="time" value={form.end_time} onChange={e => setForm(f => ({ ...f, end_time: e.target.value }))} required className="bg-dark text-light border-secondary" />
                </div>
              </div>
              <div className="row g-2 mb-1">
                <div className="col-6">
                  <Form.Label>Entrada anticipada (min)</Form.Label>
                  <Form.Control id="input-hor-anticipada" type="number" min="0" value={form.max_entry_minutes} onChange={e => setForm(f => ({ ...f, max_entry_minutes: e.target.value }))} className="bg-dark text-light border-secondary" />
                </div>
                <div className="col-6">
                  <Form.Label>Tolerancia de retardo (min)</Form.Label>
                  <Form.Control id="input-hor-tolerancia" type="number" min="0" value={form.minutes_to_be_late} onChange={e => setForm(f => ({ ...f, minutes_to_be_late: e.target.value }))} className="bg-dark text-light border-secondary" />
                </div>
              </div>
            </Modal.Body>
            <Modal.Footer style={{ background: 'var(--surface)', borderColor: 'var(--border)' }}>
              <Button variant="outline-secondary" onClick={() => setShowModal(false)}>Cancelar</Button>
              <Button id="btn-guardar-horario" type="submit" variant="danger" className="vault-gradient border-0" disabled={saving}>
                {saving ? <Spinner size="sm" animation="border" /> : (editing ? 'Guardar Cambios' : 'Crear Horario')}
              </Button>
            </Modal.Footer>
          </Form>
        </Modal>
      )}
    </>
  );
}
