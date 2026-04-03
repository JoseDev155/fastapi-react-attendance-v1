-- Script de prueba para operaciones CRUD de roles, materias y carreras
-- Este archivo contiene plantillas para pruebas de datos base
-- NO incluye datos de seed, solo estructura para pruebas

-- ====================================
-- PRUEBAS ROLES
-- ====================================

-- Insertar roles de prueba
-- INSERT INTO roles (name, description, is_active)
-- VALUES 
--   ('Estudiante', 'Rol para estudiantes', TRUE),
--   ('Profesor', 'Rol para profesores', TRUE),
--   ('Coordinador', 'Rol para coordinadores', TRUE);

-- Obtener todos los roles
-- SELECT * FROM roles;

-- Actualizar descripción de rol
-- UPDATE roles SET description = 'Profesor universitario' WHERE name = 'Profesor';

-- Desactivar rol
-- UPDATE roles SET is_active = FALSE WHERE name = 'Coordinador';


-- ====================================
-- PRUEBAS MATERIAS (SIGNATURES)
-- ====================================

-- Insertar materias de prueba
-- INSERT INTO signatures (id, name, description, is_active)
-- VALUES 
--   ('MAT001', 'Matemáticas I', 'Cálculo diferencial e integral', TRUE),
--   ('FIS001', 'Física I', 'Mecánica clásica', TRUE),
--   ('PRO001', 'Programación I', 'Fundamentos de programación', TRUE);

-- Obtener todas las materias activas
-- SELECT * FROM signatures WHERE is_active = TRUE;

-- Buscar materia por nombre
-- SELECT * FROM signatures WHERE name LIKE '%Matemáticas%';

-- Actualizar materia
-- UPDATE signatures SET description = 'Cálculo y álgebra lineal avanzados' WHERE id = 'MAT001';

-- Desactivar materia
-- UPDATE signatures SET is_active = FALSE WHERE id = 'MAT001';


-- ====================================
-- PRUEBAS CARRERAS (CAREERS)
-- ====================================

-- Insertar carreras de prueba
-- INSERT INTO careers (id, name, description, is_active)
-- VALUES 
--   (1, 'Ingeniería en Sistemas', 'Carrera de 5 años en sistemas computacionales', TRUE),
--   (2, 'Ingeniería en Electrónica', 'Carrera de 5 años en electrónica', TRUE),
--   (3, 'Administración', 'Carrera de 4 años en administración de empresas', TRUE);

-- Obtener todas las carreras
-- SELECT * FROM careers;

-- Obtener materias de una carrera (JOIN)
-- SELECT c.name as carrera, s.name as materia FROM careers c
-- JOIN career_signatures cs ON c.id = cs.career_id
-- JOIN signatures s ON cs.signature_id = s.id
-- WHERE c.id = 1;

-- Actualizar carrera
-- UPDATE careers SET description = 'Carrera de 4 años con énfasis en ciberseguridad' WHERE id = 1;

-- Desactivar carrera
-- UPDATE careers SET is_active = FALSE WHERE id = 3;


-- ====================================
-- PRUEBAS CICLOS ACADÉMICOS (ACADEMIC_CYCLES)
-- ====================================

-- Insertar ciclos académicos de prueba
-- INSERT INTO academic_cycles (cycle_name, cycle_year, is_active)
-- VALUES 
--   ('Primer semestre 2025', '2025-01-01', TRUE),
--   ('Segundo semestre 2025', '2025-06-01', TRUE),
--   ('Primer semestre 2026', '2026-01-01', FALSE);

-- Obtener todos los ciclos académicos
-- SELECT * FROM academic_cycles;

-- Obtener ciclo académico activo
-- SELECT * FROM academic_cycles WHERE is_active = TRUE;

-- Obtener grupos en un ciclo académico
-- SELECT g.id, g.name, g.career_signature_id FROM groups g
-- WHERE g.academic_cycle_id = 1;
