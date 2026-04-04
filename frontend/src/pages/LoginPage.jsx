import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Row, Col, Form, Button, Alert } from 'react-bootstrap';
import { fetchApi } from '../api/apiFunctions';
import { useAuth } from '../context/AuthContext';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { setToken } = useAuth();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const data = await fetchApi('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ username: email, password: password }),
      });

      localStorage.setItem('accessToken', data.access_token);
      setToken(data.access_token);  // actualiza el contexto sin recarga
      navigate('/dashboard');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container fluid className="vh-100 d-flex align-items-center justify-content-center" style={{ backgroundColor: 'var(--background)' }}>
      <Row className="w-100 shadow-lg rounded overflow-hidden" style={{ maxWidth: '1000px', backgroundColor: 'var(--surface)' }}>

        {/* Banner Institucional */}
        <Col lg={6} className="d-none d-lg-flex flex-column justify-content-between p-5 text-light" style={{ borderRight: '1px solid #3e4042' }}>
          <div>
            <div className="d-flex align-items-center mb-4">
              <span className="material-symbols-outlined fs-2 text-primary me-2">account_balance</span>
              <h4 className="headline fw-bold mb-0 text-primary">Sistema de Asistencias</h4>
            </div>
            <h1 className="headline display-5 fw-bold mt-5">Universidades para el Bienestar Benito Juárez García <br /> <span className="text-primary">(UBBJ)</span></h1>
            <p className="mt-4 text-secondary fs-5" style={{ fontWeight: 300 }}>
              Integridad académica, archivada digitalmente. Seguro, inmutable y permanente.
            </p>
          </div>
          <div className="d-flex gap-5 mt-5 pt-5">
            <div>
              <p className="text-primary fw-bold text-uppercase mb-1" style={{ fontSize: '0.8rem', letterSpacing: '2px' }}>Establecido</p>
              <h5 className="headline text-light">1894</h5>
            </div>
            <div>
              <p className="text-primary fw-bold text-uppercase mb-1" style={{ fontSize: '0.8rem', letterSpacing: '2px' }}>Versión</p>
              <h5 className="headline text-light">v1.0.4 - ESTABLE</h5>
            </div>
          </div>
        </Col>

        {/* Formulario de Login */}
        <Col lg={6} xs={12} className="p-sm-5 p-4 d-flex align-items-center">
          <div className="w-100">
            <div className="mb-4 d-flex align-items-center d-lg-none">
              <span className="material-symbols-outlined fs-4 text-primary me-2">account_balance</span>
              <h5 className="headline fw-bold mb-0 text-primary">Sistema de Asistencias</h5>
            </div>
            <h2 className="headline fw-bold mb-1">Formulario de Acceso</h2>
            <p className="text-secondary mb-4">Autenticación Institucional Requerida</p>

            {error && <Alert variant="danger">{error}</Alert>}

            <Form onSubmit={handleLogin}>
              <Form.Group className="mb-4">
                <Form.Label className="text-secondary text-uppercase fw-bold" style={{ fontSize: '0.8rem', letterSpacing: '1px' }}>ID o Correo Electrónico</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="correo@ejemplo.edu.mx"
                  className="bg-dark text-light border-secondary p-3"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </Form.Group>

              <Form.Group className="mb-4">
                <Form.Label className="text-secondary text-uppercase fw-bold" style={{ fontSize: '0.8rem', letterSpacing: '1px' }}>Clave de Acceso</Form.Label>
                <div className="position-relative">
                  <Form.Control
                    type={showPassword ? 'text' : 'password'}
                    placeholder="••••••••••••"
                    className="bg-dark text-light border-secondary p-3 pe-5"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    style={{ paddingRight: '3rem' }}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(prev => !prev)}
                    style={{
                      position: 'absolute', top: '50%', right: '0.9rem',
                      transform: 'translateY(-50%)',
                      background: 'none', border: 'none', cursor: 'pointer',
                      color: 'var(--secondary)', opacity: 0.75, lineHeight: 1, padding: 0
                    }}
                    tabIndex={-1}
                    aria-label={showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'}
                  >
                    <span className="material-symbols-outlined" style={{ fontSize: '1.3rem', userSelect: 'none' }}>
                      {showPassword ? 'visibility_off' : 'visibility'}
                    </span>
                  </button>
                </div>
              </Form.Group>

              <div className="d-grid mt-5">
                <Button variant="danger" size="lg" type="submit" className="vault-gradient text-uppercase fw-bold border-0 p-3" disabled={loading}>
                  {loading ? 'Autenticando...' : 'Autenticar Entrada'}
                </Button>
              </div>
            </Form>
            <div className="mt-5 text-center">
              <small className="text-secondary opacity-75">
                Solo Personal Autorizado. Todos los intentos de acceso son registrados.
              </small>
            </div>
          </div>
        </Col>
      </Row>
    </Container>
  );
}
