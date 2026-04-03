-- Script de prueba para operaciones CRUD de INSCRIPCIONES (ENROLLMENTS)
-- ⚠️ EJECUTAR DÉCIMO - DEPENDE DE: students (080), groups (070)
-- Registra qué estudiantes están inscritos en cada grupo/materia

-- ====================================
-- PRUEBAS DE CREACIÓN (CREATE)
-- ====================================
-- Insertar inscripciones de prueba
-- Nota: student_id y group_id deben existir
-- INSERT INTO enrollments (enrollment_date, student_id, group_id)
-- VALUES 
--   ('2025-01-15'::date, 'EST001', 'GRP001'),  -- Pedro en Matemáticas I Grupo A
--   ('2025-01-15'::date, 'EST002', 'GRP001'),  -- Ana en Matemáticas I Grupo A
--   ('2025-01-16'::date, 'EST004', 'GRP001'),  -- Carmen en Matemáticas I Grupo A
--   ('2025-01-20'::date, 'EST003', 'GRP002'),  -- Luis en Matemáticas I Grupo B
--   ('2025-01-20'::date, 'EST005', 'GRP002'),  -- Juan en Matemáticas I Grupo B
--   ('2025-02-01'::date, 'EST006', 'GRP002'),  -- Rosa en Matemáticas I Grupo B
--   ('2025-01-15'::date, 'EST001', 'GRP003'),  -- Pedro en Programación I Grupo A
--   ('2025-01-15'::date, 'EST002', 'GRP003'),  -- Ana en Programación I Grupo A
--   ('2025-01-15'::date, 'EST004', 'GRP003'),  -- Carmen en Programación I Grupo A
--   ('2025-01-20'::date, 'EST003', 'GRP004'),  -- Luis en Programación I Grupo B
--   ('2025-01-20'::date, 'EST005', 'GRP004'),  -- Juan en Programación I Grupo B
--   ('2025-01-15'::date, 'EST001', 'GRP005'),  -- Pedro en Bases de Datos I Grupo A
--   ('2025-01-15'::date, 'EST004', 'GRP005');  -- Carmen en Bases de Datos I Grupo A


-- ====================================
-- PRUEBAS DE LECTURA (READ)
-- ====================================
-- Obtener todas las inscripciones
-- SELECT * FROM enrollments;

-- Obtener inscripción por ID
-- SELECT * FROM enrollments WHERE id = 1;

-- Obtener inscripciones de un estudiante
-- SELECT e.id, e.enrollment_date, g.id as grupo, sig.name as materia FROM enrollments e
-- JOIN groups g ON e.group_id = g.id
-- JOIN career_signatures cs ON g.career_signature_id = cs.id
-- JOIN signatures sig ON cs.signature_id = sig.id
-- WHERE e.student_id = 'EST001'
-- ORDER BY sig.name;

-- Obtener estudiantes inscritos en un grupo
-- SELECT s.id, s.first_name, s.last_name, e.enrollment_date FROM enrollments e
-- JOIN students s ON e.student_id = s.id
-- WHERE e.group_id = 'GRP001'
-- ORDER BY s.last_name;

-- Contar estudiantes por grupo
-- SELECT g.id, g.name, COUNT(e.id) as cantidad_estudiantes FROM groups g
-- LEFT JOIN enrollments e ON g.id = e.group_id
-- GROUP BY g.id, g.name
-- ORDER BY g.id;

-- Obtener inscripciones en un rango de fechas
-- SELECT s.first_name, s.last_name, g.id as grupo, e.enrollment_date FROM enrollments e
-- JOIN students s ON e.student_id = s.id
-- JOIN groups g ON e.group_id = g.id
-- WHERE e.enrollment_date BETWEEN '2025-01-01'::date AND '2025-02-28'::date
-- ORDER BY e.enrollment_date, s.last_name;

-- Obtener listado de estudiantes de un grupo para pasar asistencia
-- SELECT s.id, s.first_name, s.last_name FROM enrollments e
-- JOIN students s ON e.student_id = s.id
-- WHERE e.group_id = 'GRP001'
-- ORDER BY s.last_name, s.first_name;


-- ====================================
-- PRUEBAS DE ACTUALIZACIÓN (UPDATE)
-- ====================================
-- Actualizar fecha de inscripción
-- UPDATE enrollments SET enrollment_date = '2025-03-01'::date WHERE id = 1;

-- Cambiar estudiante de grupo (raramente se hace)
-- UPDATE enrollments SET group_id = 'GRP002' WHERE id = 4;


-- ====================================
-- PRUEBAS DE ELIMINACIÓN (DELETE)
-- ====================================
-- ⚠️ NO ELIMINAR si hay attendances asociados
-- Verificar relaciones:
-- SELECT COUNT(*) FROM attendances WHERE enrollment_id = 1;

-- Eliminar una inscripción específica
-- DELETE FROM enrollments WHERE id = 1;

-- Desmatricular un estudiante de un grupo
-- DELETE FROM enrollments WHERE student_id = 'EST007' AND group_id = 'GRP001';

-- Desmatricular todos los estudiantes de un grupo (CUIDADO)
-- DELETE FROM enrollments WHERE group_id = 'GRP001';
