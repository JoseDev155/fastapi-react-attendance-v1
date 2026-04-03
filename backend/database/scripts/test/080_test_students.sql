-- Script de prueba para operaciones CRUD de ESTUDIANTES
-- ⚠️ EJECUTAR OCTAVO - SIN DEPENDENCIAS DIRECTAS
-- Pero será referenciado por enrollments

-- ====================================
-- PRUEBAS DE CREACIÓN (CREATE)
-- ====================================
-- Insertar estudiantes de prueba
-- INSERT INTO students (id, first_name, last_name, email, enrollment_date, is_active)
-- VALUES 
--   ('EST001', 'Pedro', 'Martínez', 'pedro.martinez@student.ubbj.edu', '2025-01-15'::date, TRUE),
--   ('EST002', 'Ana', 'García', 'ana.garcia@student.ubbj.edu', '2025-01-20'::date, TRUE),
--   ('EST003', 'Luis', 'Rodríguez', 'luis.rodriguez@student.ubbj.edu', '2025-02-01'::date, TRUE),
--   ('EST004', 'Carmen', 'López', 'carmen.lopez@student.ubbj.edu', '2025-01-15'::date, TRUE),
--   ('EST005', 'Juan', 'Fernández', 'juan.fernandez@student.ubbj.edu', '2025-01-20'::date, TRUE),
--   ('EST006', 'Rosa', 'Torres', 'rosa.torres@student.ubbj.edu', '2025-02-05'::date, TRUE),
--   ('EST007', 'Miguel', 'Sánchez', 'miguel.sanchez@student.ubbj.edu', '2025-01-18'::date, TRUE),
--   ('EST008', 'Laura', 'Pérez', 'laura.perez@student.ubbj.edu', '2025-01-22'::date, TRUE);


-- ====================================
-- PRUEBAS DE LECTURA (READ)
-- ====================================
-- Obtener todos los estudiantes
-- SELECT id, first_name, last_name, email, enrollment_date FROM students;

-- Obtener estudiante por ID
-- SELECT * FROM students WHERE id = 'EST001';

-- Obtener estudiantes activos
-- SELECT id, first_name, last_name, email FROM students WHERE is_active = TRUE;

-- Obtener estudiantes por nombre
-- SELECT * FROM students WHERE first_name LIKE '%Pedro%';

-- Obtener estudiantes por email
-- SELECT * FROM students WHERE email = 'pedro.martinez@student.ubbj.edu';

-- Obtener grupos en los que está inscrito un estudiante (JOIN)
-- SELECT s.first_name, s.last_name, g.id, g.name, sig.name as materia FROM students s
-- JOIN enrollments e ON s.id = e.student_id
-- JOIN groups g ON e.group_id = g.id
-- JOIN career_signatures cs ON g.career_signature_id = cs.id
-- JOIN signatures sig ON cs.signature_id = sig.id
-- WHERE s.id = 'EST001';


-- ====================================
-- PRUEBAS DE ACTUALIZACIÓN (UPDATE)
-- ====================================
-- Actualizar nombre de estudiante
-- UPDATE students SET first_name = 'Pedro Luis' WHERE id = 'EST001';

-- Actualizar email de estudiante
-- UPDATE students SET email = 'pedroluis.martinez@student.ubbj.edu' WHERE id = 'EST001';

-- Actualizar fecha de inscripción
-- UPDATE students SET enrollment_date = '2025-03-01'::date WHERE id = 'EST003';

-- Desactivar estudiante (soft delete)
-- UPDATE students SET is_active = FALSE WHERE id = 'EST007';

-- Reactivar estudiante
-- UPDATE students SET is_active = TRUE WHERE id = 'EST007';


-- ====================================
-- PRUEBAS DE ELIMINACIÓN (DELETE)
-- ====================================
-- ⚠️ NO ELIMINAR si hay enrollments asociados
-- Verificar relaciones:
-- SELECT COUNT(*) FROM enrollments WHERE student_id = 'EST001';

-- Eliminar estudiante (solo si no hay enrollments referenced)
-- DELETE FROM students WHERE id = 'EST008';
