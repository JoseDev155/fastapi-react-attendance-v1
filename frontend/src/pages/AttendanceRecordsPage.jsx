import { useState, useEffect } from 'react';
import { Row, Col, Card, Table, Badge, Spinner, Alert } from 'react-bootstrap';
import { fetchApi } from '../api/apiFunctions';

export default function AttendanceRecordsPage() {
  const [report, setReport] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadReport = async () => {
      try {
        const data = await fetchApi('/reports/group/GRP001/monthly?year=2026&month=4');
        setReport(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    loadReport();
  }, []);

  const getBadgeVariant = (val) => {
    if(val >= 80) return 'success';
    if(val >= 60) return 'warning';
    return 'danger';
  };

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ minHeight: '60vh' }}>
        <Spinner animation="border" variant="danger" />
      </div>
    );
  }

  if (error) {
    return <Alert variant="danger">{error}</Alert>;
  }

  const students = report.students || [];

  return (
    <>
      <div className="mb-4">
        <h2 className="headline fw-bold">Registro de Asistencias - {report.group_name}</h2>
        <p className="text-secondary">Métricas operacionales del mes base.</p>
      </div>

      <Row className="mb-4">
        <Col md={3}>
          <Card className="bg-dark text-light border-0 shadow-sm">
            <Card.Body>
              <h6 className="text-secondary text-uppercase fw-bold" style={{ fontSize: '0.8rem' }}>Asistencias Globlales</h6>
              <h2 className="headline text-success">{report.global_stats?.PRESENT || 0}</h2>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="bg-dark text-light border-0 shadow-sm">
            <Card.Body>
              <h6 className="text-secondary text-uppercase fw-bold" style={{ fontSize: '0.8rem' }}>Faltas Absolutas</h6>
              <h2 className="headline text-danger">{report.global_stats?.ABSENT || 0}</h2>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="bg-dark text-light border-0 shadow-sm">
            <Card.Body>
              <h6 className="text-secondary text-uppercase fw-bold" style={{ fontSize: '0.8rem' }}>Retardos Tol.</h6>
              <h2 className="headline text-warning">{report.global_stats?.LATE || 0}</h2>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="bg-dark text-light border-0 shadow-sm">
            <Card.Body>
              <h6 className="text-secondary text-uppercase fw-bold" style={{ fontSize: '0.8rem' }}>Periodo</h6>
              <h2 className="headline">{report.month}/{report.year}</h2>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Card className="bg-dark text-light border-0 shadow-sm">
        <Card.Body className="p-0">
          <Table responsive variant="dark" hover className="mb-0">
            <thead>
              <tr>
                <th className="py-3 px-4 border-bottom border-secondary text-uppercase text-secondary" style={{ fontSize: '0.85rem' }}>Identificador</th>
                <th className="py-3 px-4 border-bottom border-secondary text-uppercase text-secondary" style={{ fontSize: '0.85rem' }}>Estudiante</th>
                <th className="py-3 px-4 border-bottom border-secondary text-uppercase text-secondary text-center" style={{ fontSize: '0.85rem' }}>Presente</th>
                <th className="py-3 px-4 border-bottom border-secondary text-uppercase text-secondary text-center" style={{ fontSize: '0.85rem' }}>Ausente</th>
                <th className="py-3 px-4 border-bottom border-secondary text-uppercase text-secondary text-center" style={{ fontSize: '0.85rem' }}>Tarde</th>
                <th className="py-3 px-4 border-bottom border-secondary text-uppercase text-secondary text-end" style={{ fontSize: '0.85rem' }}>Estado</th>
              </tr>
            </thead>
            <tbody>
              {students.map((st) => {
                const present = st.stats?.PRESENT || 0;
                const absent = st.stats?.ABSENT || 0;
                const total = present + absent + (st.stats?.LATE || 0);
                const perc = total > 0 ? Math.round((present / total) * 100) : 0;
                
                return (
                  <tr key={st.student_id}>
                    <td className="py-3 px-4 fw-bold font-monospace text-primary">{st.nickname}</td>
                    <td className="py-3 px-4">{st.full_name}</td>
                    <td className="py-3 px-4 text-center">{present}</td>
                    <td className="py-3 px-4 text-center">{absent}</td>
                    <td className="py-3 px-4 text-center">{st.stats?.LATE || 0}</td>
                    <td className="py-3 px-4 text-end">
                      <Badge bg={getBadgeVariant(perc)}>{perc}% Asistencia</Badge>
                    </td>
                  </tr>
                );
              })}
              {students.length === 0 && (
                <tr>
                  <td colSpan="6" className="text-center py-4 text-secondary">
                    Sin registros para este bloque.
                  </td>
                </tr>
              )}
            </tbody>
          </Table>
        </Card.Body>
      </Card>
    </>
  );
}
