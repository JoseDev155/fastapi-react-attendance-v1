-- Script de prueba para operaciones CRUD de ASISTENCIAS (ATTENDANCES)
-- ⚠️ EJECUTAR ÚLTIMO - DEPENDE DE: enrollments (100)
-- Registra la asistencia de estudiantes en cada clase

-- ====================================
-- PRUEBAS DE CREACIÓN (CREATE)
-- ====================================
-- Insertar registros de asistencia de prueba
-- Nota: enrollment_id debe existir en enrollments
-- status puede ser: 'present', 'absent', 'late', 'justified', 'left_early'
-- INSERT INTO attendances (arrival_time, status, notes, enrollment_id)
-- VALUES 
--   ('2025-01-15 08:05:00'::timestamp, 'present', 'Asistió puntualmente', 1),
--   ('2025-01-15 08:12:00'::timestamp, 'late', 'Llegó 12 minutos tarde', 2),
--   ('2025-01-15 08:00:00'::timestamp, 'absent', NULL, 3),
--   ('2025-01-15 08:03:00'::timestamp, 'present', NULL, 4),
--   ('2025-01-17 10:05:00'::timestamp, 'present', NULL, 5),
--   ('2025-01-17 10:20:00'::timestamp, 'late', 'Llegó tarde por tráfico', 6),
--   ('2025-01-17 10:00:00'::timestamp, 'justified', 'Certificado médico', 7),
--   ('2025-01-17 10:02:00'::timestamp, 'present', NULL, 8),
--   ('2025-01-22 14:05:00'::timestamp, 'present', NULL, 9),
--   ('2025-01-22 14:30:00'::timestamp, 'left_early', 'Se retiró anticipadamente', 10),
--   ('2025-01-22 14:00:00'::timestamp, 'absent', NULL, 11),
--   ('2025-01-22 14:03:00'::timestamp, 'present', NULL, 12),
--   ('2025-01-22 14:08:00'::timestamp, 'present', NULL, 13);


-- ====================================
-- PRUEBAS DE LECTURA (READ)
-- ====================================
-- Obtener todas las asistencias
-- SELECT * FROM attendances;

-- Obtener asistencia por ID
-- SELECT * FROM attendances WHERE id = 1;

-- Obtener asistencias de una inscripción (estudiante en grupo)
-- SELECT a.id, a.arrival_time, a.status, a.notes FROM attendances a
-- WHERE a.enrollment_id = 1
-- ORDER BY a.arrival_time DESC;

-- Obtener asistencias de un estudiante en todas sus materias
-- SELECT s.first_name, s.last_name, sig.name as materia, a.arrival_time, a.status FROM attendances a
-- JOIN enrollments e ON a.enrollment_id = e.id
-- JOIN students s ON e.student_id = s.id
-- JOIN groups g ON e.group_id = g.id
-- JOIN career_signatures cs ON g.career_signature_id = cs.id
-- JOIN signatures sig ON cs.signature_id = sig.id
-- WHERE s.id = 'EST001'
-- ORDER BY a.arrival_time DESC;

-- Obtener asistencias de una fecha específica
-- SELECT a.id, s.first_name, s.last_name, a.arrival_time, a.status FROM attendances a
-- JOIN enrollments e ON a.enrollment_id = e.id
-- JOIN students s ON e.student_id = s.id
-- WHERE DATE(a.arrival_time) = '2025-01-17'::date
-- ORDER BY a.arrival_time;

-- Obtener asistencias por estado (PRESENTES)
-- SELECT s.first_name, s.last_name, a.arrival_time FROM attendances a
-- JOIN enrollments e ON a.enrollment_id = e.id
-- JOIN students s ON e.student_id = s.id
-- WHERE a.status = 'present'
-- ORDER BY a.arrival_time DESC
-- LIMIT 20;

-- Contar asistencias de un grupo en una clase
-- SELECT a.status, COUNT(*) as cantidad FROM attendances a
-- JOIN enrollments e ON a.enrollment_id = e.id
-- WHERE e.group_id = 'GRP001' AND DATE(a.arrival_time) = '2025-01-15'::date
-- GROUP BY a.status;

-- Generar reporte de presentes en un grupo para una fecha
-- SELECT s.id, s.first_name, s.last_name, 
--        COALESCE(a.status, 'absent') as estado,
--        CASE WHEN a.status IS NULL THEN 'No registrado'
--             WHEN a.status = 'present' THEN 'Presente'
--             WHEN a.status = 'late' THEN 'Tarde'
--             WHEN a.status = 'absent' THEN 'Ausente'
--             WHEN a.status = 'justified' THEN 'Falta justificada'
--             WHEN a.status = 'left_early' THEN 'Salida anticipada'
--        END as descripción
-- FROM enrollments e
-- JOIN students s ON e.student_id = s.id
-- LEFT JOIN attendances a ON e.id = a.enrollment_id AND DATE(a.arrival_time) = '2025-01-15'::date
-- WHERE e.group_id = 'GRP001'
-- ORDER BY s.last_name, s.first_name;

-- Porcentaje de asistencia por estudiante
-- SELECT s.first_name, s.last_name, 
--        COUNT(CASE WHEN a.status IN ('present', 'late', 'left_early') THEN 1 END) as clases_presentes,
--        COUNT(a.id) as total_registros,
--        ROUND(100.0 * COUNT(CASE WHEN a.status IN ('present', 'late', 'left_early') THEN 1 END) / NULLIF(COUNT(a.id), 0), 2) as porcentaje
-- FROM enrollments e
-- JOIN students s ON e.student_id = s.id
-- LEFT JOIN attendances a ON e.id = a.enrollment_id
-- WHERE e.group_id = 'GRP001'
-- GROUP BY s.id, s.first_name, s.last_name
-- ORDER BY porcentaje DESC;


-- ====================================
-- PRUEBAS DE ACTUALIZACIÓN (UPDATE)
-- ====================================
-- Actualizar estado de asistencia (ej: cambiar de ausente a justificada)
-- UPDATE attendances SET status = 'justified' WHERE id = 3;

-- Actualizar notas de asistencia
-- UPDATE attendances SET notes = 'Asistencia confirmada por coordinación' WHERE id = 1;

-- Cambiar hora de llegada (solo en caso de error)
-- UPDATE attendances SET arrival_time = '2025-01-15 08:10:00'::timestamp WHERE id = 2;


-- ====================================
-- PRUEBAS DE ELIMINACIÓN (DELETE)
-- ====================================
-- Eliminar un registro de asistencia específico
-- DELETE FROM attendances WHERE id = 1;

-- Eliminar asistencias de una fecha específica (CUIDADO)
-- DELETE FROM attendances WHERE DATE(arrival_time) = '2025-01-15'::date;

-- Eliminar asistencias de un estudiante en un grupo
-- DELETE FROM attendances WHERE enrollment_id = 1;

-- Eliminar asistencias de un grupo en una fecha
-- DELETE FROM attendances WHERE enrollment_id IN (
--   SELECT id FROM enrollments WHERE group_id = 'GRP001'
-- ) AND DATE(arrival_time) = '2025-01-15'::date;
