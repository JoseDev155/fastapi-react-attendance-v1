-- Script de prueba para operaciones CRUD de asistencias (Attendance)
-- Este archivo contiene plantillas para pruebas de asistencias
-- NO incluye datos de seed, solo estructura para pruebas

-- ====================================
-- PRUEBAS DE CREACIÓN (CREATE)
-- ====================================
-- Insertar registros de asistencia de prueba
-- Nota: El enrollment_id debe existir previamente en enrollments
-- INSERT INTO attendances (attendance_date, arrival_time, status, notes, enrollment_id)
-- VALUES 
--   ('2025-01-15', '08:30:00', 'present', 'Asistió puntualmente', 1),
--   ('2025-01-15', '08:45:00', 'late', 'Llegó 15 minutos tarde', 2),
--   ('2025-01-15', '08:00:00', 'absent', 'Falta injustificada', 3),
--   ('2025-01-16', '08:25:00', 'justified', 'Falta justificada - médico', 1);


-- ====================================
-- PRUEBAS DE LECTURA (READ)
-- ====================================
-- Obtener todas las asistencias
-- SELECT * FROM attendances;

-- Obtener asistencia por ID
-- SELECT * FROM attendances WHERE id = 1;

-- Obtener asistencias de una inscripción
-- SELECT * FROM attendances WHERE enrollment_id = 1;

-- Obtener asistencias de una fecha específica
-- SELECT * FROM attendances WHERE DATE(arrival_time) = '2025-01-15';

-- Obtener asistencias por estado
-- SELECT * FROM attendances WHERE status = 'present';

-- Contar presentes en una clase
-- SELECT COUNT(*) as presentes FROM attendances 
-- WHERE enrollment_id IN (SELECT id FROM enrollments WHERE group_id = 'GRP001')
-- AND DATE(arrival_time) = '2025-01-15'
-- AND status = 'present';

-- Obtener estudiante y su asistencia (JOIN)
-- SELECT s.first_name, s.last_name, a.arrival_time, a.status FROM students s
-- JOIN enrollments e ON s.id = e.student_id
-- JOIN attendances a ON e.id = a.enrollment_id
-- WHERE DATE(a.arrival_time) = '2025-01-15';


-- ====================================
-- PRUEBAS DE ACTUALIZACIÓN (UPDATE)
-- ====================================
-- Actualizar estado de asistencia (ej: cambiar de ausente a justificada)
-- UPDATE attendances SET status = 'justified' WHERE id = 3;

-- Actualizar notas de asistencia
-- UPDATE attendances SET notes = 'Asistencia confirmada por coordinación' WHERE id = 1;

-- Cambiar hora de llegada
-- UPDATE attendances SET arrival_time = '2025-01-15 08:40:00' WHERE id = 2;


-- ====================================
-- PRUEBAS DE ELIMINACIÓN (DELETE)
-- ====================================
-- Eliminar un registro de asistencia (hard delete)
-- DELETE FROM attendances WHERE id = 1;

-- Eliminar asistencias de una fecha
-- DELETE FROM attendances WHERE DATE(arrival_time) = '2025-01-15';

-- Eliminar asistencias de una inscripción
-- DELETE FROM attendances WHERE enrollment_id = 1;
