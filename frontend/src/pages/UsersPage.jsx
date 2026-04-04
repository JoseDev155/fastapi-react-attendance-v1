import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Modal, Button, Form, Spinner, Alert, Badge } from 'react-bootstrap';
import { useAuth } from '../context/AuthContext';
import { apiFetch } from '../api/apiClient';

export default function UsersPage() {
  const { token } = useAuth();

  const [users, setUsers]         = useState([]);
  const [loading, setLoading]     = useState(true);
  const [error, setError]         = useState(null);
  const [search, setSearch]       = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editing, setEditing]     = useState(null);
  const [saving, setSaving]       = useState(false);
  const [formError, setFormError] = useState(null);

  const emptyForm = { id: '', first_name: '', last_name: '', email: '', password: '', role_id: 2 };
  const [form, setForm] = useState(emptyForm);

  const loadUsers = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiFetch('/users', { token });
      setUsers(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadUsers(); }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const openCreate = () => {
    setEditing(null);
    setForm(emptyForm);
    setFormError(null);
    setShowModal(true);
  };

  const openEdit = (u) => {
    setEditing(u);
    setForm({ id: u.id, first_name: u.first_name, last_name: u.last_name, email: u.email, password: '', role_id: u.role_id });
    setFormError(null);
    setShowModal(true);
  };

  const handleSoftDelete = async (id, name) => {
    if (!window.confirm(`¿Desactivar al usuario "${name}"? Podrá ser reactivado posteriormente.`)) return;
    try {
      await apiFetch(`/users/${id}`, { method: 'DELETE', token });
      await loadUsers();
    } catch (e) {
      alert(`Error: ${e.message}`);
    }
  };

  const handleReactivate = async (id) => {
    try {
      await apiFetch(`/users/${id}/reactivate`, { method: 'POST', token });
      await loadUsers();
    } catch (e) {
      alert(`Error: ${e.message}`);
    }
  };

  const handleDestroy = async (id, name) => {
    if (!window.confirm(`⚠️ ¿Eliminar DEFINITIVAMENTE al usuario "${name}"? Esta acción no se puede deshacer.`)) return;
    try {
      await apiFetch(`/users/${id}/destroy`, { method: 'DELETE', token });
      await loadUsers();
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
        const body = { first_name: form.first_name, last_name: form.last_name, email: form.email, role_id: parseInt(form.role_id) };
        if (form.password) body.password = form.password;
        await apiFetch(`/users/${editing.id}`, { method: 'PUT', token, body });
      } else {
        await apiFetch('/users', { method: 'POST', token, body: { ...form, role_id: parseInt(form.role_id) } });
      }
      setShowModal(false);
      await loadUsers();
    } catch (e) {
      setFormError(e.message);
    } finally {
      setSaving(false);
    }
  };

  const filtered = users.filter(u => {
    const q = search.toLowerCase();
    return u.id.toLowerCase().includes(q) || u.first_name.toLowerCase().includes(q) || u.last_name.toLowerCase().includes(q) || u.email.toLowerCase().includes(q);
  });

  return (
    <>
      <div className="page-header">
        <div>
          <Link to="/dashboard" className="page-header-back">
            <span className="material-symbols-outlined" style={{ fontSize: '0.9rem' }}>arrow_back</span>
            Inicio
          </Link>
          <h1 className="headline mb-0" style={{ fontSize: '1.6rem', fontWeight: 700 }}>Usuarios del Sistema</h1>
          <p style={{ color: 'var(--on-surface-dim)', fontSize: '0.85rem', marginBottom: 0 }}>
            Administradores y profesores con acceso al sistema.
          </p>
        </div>
        <Button id="btn-nuevo-usuario" variant="danger" className="vault-gradient border-0" onClick={openCreate}>
          <span className="material-symbols-outlined me-2" style={{ fontSize: '1rem' }}>person_add</span>
          Nuevo Usuario
        </Button>
      </div>

      <div className="mb-3" style={{ maxWidth: 360 }}>
        <div className="input-group">
          <span className="input-group-text bg-dark border-secondary text-secondary">
            <span className="material-symbols-outlined" style={{ fontSize: '1.1rem' }}>search</span>
          </span>
          <input id="input-buscar-usuario" type="text" className="form-control bg-dark text-light border-secondary" placeholder="Buscar por nombre, ID o correo..." value={search} onChange={e => setSearch(e.target.value)} />
        </div>
      </div>

      {loading && <div className="text-center py-5"><Spinner animation="border" variant="danger" /></div>}
      {error   && <Alert variant="danger">{error}</Alert>}

      {!loading && !error && (
        <div className="table-responsive" style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 10 }}>
          <table className="table table-dark table-hover mb-0 crud-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Nombre Completo</th>
                <th>Correo</th>
                <th>Rol</th>
                <th>Estado</th>
                <th className="text-end">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {filtered.length === 0 ? (
                <tr><td colSpan={6} className="text-center py-5" style={{ color: 'var(--on-surface-dim)' }}>Sin usuarios registrados</td></tr>
              ) : (
                filtered.map(u => (
                  <tr key={u.id}>
                    <td><code style={{ color: 'var(--primary-light)' }}>{u.id}</code></td>
                    <td style={{ fontWeight: 600 }}>{u.first_name} {u.last_name}</td>
                    <td style={{ fontSize: '0.85rem' }}>{u.email}</td>
                    <td>
                      <span className={`role-badge ${u.role_id === 1 ? 'role-badge-admin' : 'role-badge-profesor'}`}>
                        {u.role_id === 1 ? 'Administrador' : 'Profesor'}
                      </span>
                    </td>
                    <td>
                      <span className={`badge ${u.is_active ? 'bg-success' : 'bg-secondary'}`}>
                        {u.is_active ? 'Activo' : 'Inactivo'}
                      </span>
                    </td>
                    <td className="text-end">
                      <button id={`btn-editar-usr-${u.id}`} className="btn btn-sm btn-outline-secondary me-1" onClick={() => openEdit(u)} title="Editar">
                        <span className="material-symbols-outlined" style={{ fontSize: '0.9rem' }}>edit</span>
                      </button>
                      {u.is_active ? (
                        <button id={`btn-desactivar-${u.id}`} className="btn btn-sm btn-outline-warning me-1" onClick={() => handleSoftDelete(u.id, `${u.first_name} ${u.last_name}`)} title="Desactivar">
                          <span className="material-symbols-outlined" style={{ fontSize: '0.9rem' }}>person_off</span>
                        </button>
                      ) : (
                        <button id={`btn-reactivar-${u.id}`} className="btn btn-sm btn-outline-success me-1" onClick={() => handleReactivate(u.id)} title="Reactivar">
                          <span className="material-symbols-outlined" style={{ fontSize: '0.9rem' }}>person_check</span>
                        </button>
                      )}
                      <button id={`btn-eliminar-usr-${u.id}`} className="btn btn-sm btn-outline-danger" onClick={() => handleDestroy(u.id, `${u.first_name} ${u.last_name}`)} title="Eliminar definitivamente">
                        <span className="material-symbols-outlined" style={{ fontSize: '0.9rem' }}>delete_forever</span>
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
          <div className="px-3 py-2" style={{ color: 'var(--on-surface-dim)', fontSize: '0.8rem' }}>
            {filtered.length} de {users.length} usuarios
          </div>
        </div>
      )}

      <Modal show={showModal} onHide={() => setShowModal(false)} centered data-bs-theme="dark">
        <Modal.Header closeButton style={{ background: 'var(--surface)', borderColor: 'var(--border)' }}>
          <Modal.Title className="headline" style={{ fontSize: '1.1rem' }}>
            {editing ? 'Editar Usuario' : 'Nuevo Usuario del Sistema'}
          </Modal.Title>
        </Modal.Header>
        <Form onSubmit={handleSave}>
          <Modal.Body style={{ background: 'var(--surface)' }}>
            {formError && <Alert variant="danger" className="py-2">{formError}</Alert>}
            {!editing && (
              <Form.Group className="mb-3">
                <Form.Label>ID de Empleado</Form.Label>
                <Form.Control id="input-usr-id" type="text" placeholder="Ej: PROF002" value={form.id} onChange={e => setForm(f => ({ ...f, id: e.target.value }))} required className="bg-dark text-light border-secondary" />
              </Form.Group>
            )}
            <div className="row g-2 mb-3">
              <div className="col-6">
                <Form.Label>Nombre(s)</Form.Label>
                <Form.Control id="input-usr-nombre" type="text" placeholder="Nombre" value={form.first_name} onChange={e => setForm(f => ({ ...f, first_name: e.target.value }))} required className="bg-dark text-light border-secondary" />
              </div>
              <div className="col-6">
                <Form.Label>Apellidos</Form.Label>
                <Form.Control id="input-usr-apellido" type="text" placeholder="Apellidos" value={form.last_name} onChange={e => setForm(f => ({ ...f, last_name: e.target.value }))} required className="bg-dark text-light border-secondary" />
              </div>
            </div>
            <Form.Group className="mb-3">
              <Form.Label>Correo Electrónico</Form.Label>
              <Form.Control id="input-usr-email" type="email" placeholder="correo@ubbj.edu.mx" value={form.email} onChange={e => setForm(f => ({ ...f, email: e.target.value }))} required className="bg-dark text-light border-secondary" />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>
                Contraseña {editing && <span style={{ color: 'var(--on-surface-dim)', fontSize: '0.8rem' }}>(dejar vacío para no cambiar)</span>}
              </Form.Label>
              <Form.Control id="input-usr-password" type="password" placeholder="••••••••" value={form.password} onChange={e => setForm(f => ({ ...f, password: e.target.value }))} required={!editing} className="bg-dark text-light border-secondary" />
            </Form.Group>
            <Form.Group className="mb-1">
              <Form.Label>Rol</Form.Label>
              <Form.Select id="select-usr-rol" value={form.role_id} onChange={e => setForm(f => ({ ...f, role_id: e.target.value }))} className="bg-dark text-light border-secondary">
                <option value={2}>Profesor</option>
                <option value={1}>Administrador</option>
              </Form.Select>
            </Form.Group>
          </Modal.Body>
          <Modal.Footer style={{ background: 'var(--surface)', borderColor: 'var(--border)' }}>
            <Button variant="outline-secondary" onClick={() => setShowModal(false)}>Cancelar</Button>
            <Button id="btn-guardar-usuario" type="submit" variant="danger" className="vault-gradient border-0" disabled={saving}>
              {saving ? <Spinner size="sm" animation="border" /> : (editing ? 'Guardar Cambios' : 'Crear Usuario')}
            </Button>
          </Modal.Footer>
        </Form>
      </Modal>
    </>
  );
}
