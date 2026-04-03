-- Script de prueba para operaciones CRUD de inscripciones (Enrollments)
-- Este archivo contiene plantillas para pruebas de inscripciones
-- NO incluye datos de seed, solo estructura para pruebas

-- ====================================
-- PRUEBAS DE CREACIÓN (CREATE)
-- ====================================
-- Insertar inscripciones de prueba
-- Nota: Los IDs de estudiantes, grupos deben existir previamente
-- INSERT INTO enrollments (enrollment_date, student_id, group_id)
-- VALUES 
--   ('2025-01-15', 'EST001', 'GRP001'),
--   ('2025-01-20', 'EST002', 'GRP001'),
--   ('2025-02-01', 'EST003', 'GRP002');


-- ====================================
-- PRUEBAS DE LECTURA (READ)
-- ====================================
-- Obtener todas las inscripciones
-- SELECT * FROM enrollments;

-- Obtener inscripción por ID
-- SELECT * FROM enrollments WHERE id = 1;

-- Obtener inscripciones de un estudiante
-- SELECT * FROM enrollments WHERE student_id = 'EST001';

-- Obtener inscripciones de un grupo
-- SELECT * FROM enrollments WHERE group_id = 'GRP001';

-- Obtener inscripciones entre fechas
-- SELECT * FROM enrollments WHERE enrollment_date BETWEEN '2025-01-01' AND '2025-02-28';

-- Obtener estudiantes inscritos en un grupo (JOIN)
-- SELECT s.id, s.first_name, s.last_name, e.group_id FROM students s
-- JOIN enrollments e ON s.id = e.student_id
-- WHERE e.group_id = 'GRP001';


-- ====================================
-- PRUEBAS DE ACTUALIZACIÓN (UPDATE)
-- ====================================
-- Actualizar fecha de inscripción
-- UPDATE enrollments SET enrollment_date = '2025-03-01' WHERE id = 1;

-- Cambiar estudiante de grupo (raramente se hace)
-- UPDATE enrollments SET group_id = 'GRP002' WHERE id = 1;


-- ====================================
-- PRUEBAS DE ELIMINACIÓN (DELETE)
-- ====================================
-- Eliminar inscripción (hard delete)
-- DELETE FROM enrollments WHERE id = 1;

-- Eliminar todas las inscripciones de un grupo
-- DELETE FROM enrollments WHERE group_id = 'GRP001';
