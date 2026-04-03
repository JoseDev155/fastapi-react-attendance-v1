-- Script de prueba para operaciones CRUD de MATERIAS (SIGNATURES)
-- ⚠️ EJECUTAR SEGUNDO - SIN DEPENDENCIAS (pero necesaria para career_signatures)
-- Este es un dato base: necesario para career_signatures

-- ====================================
-- PRUEBAS DE CREACIÓN (CREATE)
-- ====================================
-- Insertar materias de prueba
-- INSERT INTO signatures (id, name, description, is_active)
-- VALUES 
--   ('MAT001', 'Matemáticas I', 'Cálculo diferencial e integral', TRUE),
--   ('MAT002', 'Matemáticas II', 'Cálculo avanzado y ecuaciones diferenciales', TRUE),
--   ('FIS001', 'Física I', 'Mecánica clásica y cinemática', TRUE),
--   ('FIS002', 'Física II', 'Termodinámica y fluidos', TRUE),
--   ('PRO001', 'Programación I', 'Fundamentos de programación en Python', TRUE),
--   ('PRO002', 'Programación II', 'Programación orientada a objetos', TRUE),
--   ('BDD001', 'Bases de Datos I', 'Fundamentos de BD relacionales', TRUE),
--   ('BDD002', 'Bases de Datos II', 'SQL avanzado y administración', TRUE);


-- ====================================
-- PRUEBAS DE LECTURA (READ)
-- ====================================
-- Obtener todas las materias activas
-- SELECT * FROM signatures WHERE is_active = TRUE;

-- Buscar materia por ID
-- SELECT * FROM signatures WHERE id = 'MAT001';

-- Buscar materia por nombre
-- SELECT * FROM signatures WHERE name LIKE '%Programación%';

-- Obtener carreras que ofrecen una materia (JOIN)
-- SELECT DISTINCT c.name as carrera FROM careers c
-- JOIN career_signatures cs ON c.id = cs.career_id
-- WHERE cs.signature_id = 'MAT001';


-- ====================================
-- PRUEBAS DE ACTUALIZACIÓN (UPDATE)
-- ====================================
-- Actualizar descripción de materia
-- UPDATE signatures SET description = 'Cálculo diferencial, integral y álgebra lineal' WHERE id = 'MAT001';

-- Desactivar materia
-- UPDATE signatures SET is_active = FALSE WHERE id = 'FIS002';

-- Reactivar materia
-- UPDATE signatures SET is_active = TRUE WHERE id = 'FIS002';

-- Cambiar nombre de materia
-- UPDATE signatures SET name = 'Matemáticas Avanzada' WHERE id = 'MAT002';


-- ====================================
-- PRUEBAS DE ELIMINACIÓN (DELETE)
-- ====================================
-- ⚠️ NO ELIMINAR si hay career_signatures asociadas
-- Verificar relaciones:
-- SELECT COUNT(*) FROM career_signatures WHERE signature_id = 'MAT001';

-- Eliminar materia (solo si no hay referenced)
-- DELETE FROM signatures WHERE id = 'MAT001';
