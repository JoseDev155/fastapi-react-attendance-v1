-- Script de prueba para operaciones CRUD de estudiantes
-- Este archivo contiene plantillas para pruebas de estudiantes
-- NO incluye datos de seed, solo estructura para pruebas

-- ====================================
-- PRUEBAS DE CREACIÓN (CREATE)
-- ====================================
-- Insertar estudiantes de prueba
-- INSERT INTO students (id, nickname, first_name, last_name, email, enrollment_date, is_active)
-- VALUES 
--   ('EST001', 'Toño', 'Antonio', 'Martínez', 'antony@example.com', '2025-01-15', TRUE),
--   ('EST002', 'Nita', 'Ana', 'García', 'ana@example.com', '2025-01-20', TRUE),
--   ('EST003', 'Chepe', 'José', 'Rodríguez', 'jose@example.com', '2025-02-01', TRUE);


-- ====================================
-- PRUEBAS DE LECTURA (READ)
-- ====================================
-- Obtener todos los estudiantes
-- SELECT * FROM students;

-- Obtener estudiante por ID
-- SELECT * FROM students WHERE id = 'EST001';

-- Obtener estudiantes activos
-- SELECT * FROM students WHERE is_active = TRUE;

-- Obtener estudiantes por nombre
-- SELECT * FROM students WHERE first_name = 'Antonio';

-- Obtener estudiantes por email
-- SELECT * FROM students WHERE email = 'antony@example.com';


-- ====================================
-- PRUEBAS DE ACTUALIZACIÓN (UPDATE)
-- ====================================
-- Actualizar nombre de estudiante
-- UPDATE students SET first_name = 'Pedro Juan' WHERE id = 'EST001';

-- Actualizar email de estudiante
-- UPDATE students SET email = 'pedroj@example.com' WHERE id = 'EST001';

-- Actualizar fecha de inscripción
-- UPDATE students SET enrollment_date = '2025-03-01' WHERE id = 'EST001';

-- Desactivar estudiante (soft delete)
-- UPDATE students SET is_active = FALSE WHERE id = 'EST003';

-- Reactivar estudiante
-- UPDATE students SET is_active = TRUE WHERE id = 'EST003';


-- ====================================
-- PRUEBAS DE ELIMINACIÓN (DELETE)
-- ====================================
-- Eliminar estudiante (hard delete - solo si no tiene referencias en enrollments)
-- DELETE FROM students WHERE id = 'EST001';
