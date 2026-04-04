import { useState } from 'react';
import { Row, Col, Card, Form, Button, Alert } from 'react-bootstrap';
import { fetchApi } from '../api/apiFunctions';

export default function AdminDashboardPage() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState(null); // { type: 'success'|'danger', message: '' }
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      const selected = e.target.files[0];
      if (!selected.name.endsWith('.xlsx')) {
        setStatus({ type: 'danger', message: 'Fallo de integridad: Solo se admiten archivos .xlsx' });
        setFile(null);
      } else {
        setFile(selected);
        setStatus(null);
      }
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setStatus(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const result = await fetchApi('/uploads/attendance-excel', {
        method: 'POST',
        body: formData
      });
      // result expected: { received_month: 4, inserted: 200, skipped: 10, updated: 5, logs: [] }
      setStatus({ 
        type: 'success', 
        message: `El Archivo "${file.name}" ha sido encriptado en el sistema. Insertados: ${result.inserted}. Actualizados: ${result.updated}. Omitidos: ${result.skipped}.` 
      });
      setFile(null);
    } catch (err) {
      setStatus({ type: 'danger', message: err.message });
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadTemplate = async () => {
    try {
      const response = await fetchApi('/exports/template/group/GRP001?year=2026&month=4', { isDownload: true });
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `Plantilla_Asistencia.xlsm`;
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (err) {
      setStatus({ type: 'danger', message: 'No se pudo generar la plantilla.' });
    }
  };

  return (
    <>
      <div className="mb-4">
        <h2 className="headline fw-bold">Panel Central Administrativo</h2>
        <p className="text-secondary">Sincronización en la cadena de bloques institucional.</p>
      </div>

      {status && <Alert variant={status.type} className="shadow-sm">{status.message}</Alert>}

      <Row className="g-4">
        {/* Upload Card */}
        <Col md={8}>
          <Card className="bg-dark text-light border-0 shadow">
            <Card.Body className="p-5 text-center">
              <span className="material-symbols-outlined display-1 text-primary mb-3">upload_file</span>
              <h4 className="headline">Recepcionar Asistencias</h4>
              <p className="text-secondary mb-4">Anexe un documento .xlsx para realizar un UPSERT masivo sobre el ciclo actual.</p>
              
              <Form.Group className="mb-4 mx-auto" style={{ maxWidth: '400px' }}>
                <Form.Control 
                  type="file" 
                  accept=".xlsx"
                  className="bg-secondary text-dark border-0"
                  onChange={handleFileChange}
                />
              </Form.Group>

              <Button 
                variant="danger" 
                size="lg" 
                className="px-5 text-uppercase fw-bold"
                onClick={handleUpload}
                disabled={!file || loading}
              >
                {loading ? 'Procesando bloque...' : 'Validar & Subir archivo'}
              </Button>
            </Card.Body>
          </Card>
        </Col>

        {/* Info & Side actions */}
        <Col md={4}>
          <Card className="bg-dark text-light border-0 shadow h-100">
            <Card.Body className="p-4 d-flex flex-column">
              <h5 className="headline mb-4">Herramientas</h5>
              <div className="d-grid gap-3">
                <Button variant="outline-light" className="text-start d-flex align-items-center" onClick={handleDownloadTemplate}>
                  <span className="material-symbols-outlined me-2">download</span>
                  Plantilla de Grupo 1 (Test)
                </Button>
                <Button variant="outline-light" className="text-start d-flex align-items-center" onClick={() => alert("Este módulo de Gestión de Alumnos estará disponible en la próxima actualización de seguridad.")}>
                  <span className="material-symbols-outlined me-2">groups</span>
                  Gestión de Alumnos
                </Button>
              </div>
              
              <div className="mt-auto pt-4 border-top border-secondary opacity-50">
                <small className="d-block text-secondary">
                  <strong>Regla de Upsert:</strong> Si una asistencia ya está firmada digitalmente, se sobreescribirá ante un conflicto de fechas en la celda.
                </small>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </>
  );
}
