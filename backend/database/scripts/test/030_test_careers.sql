-- Script de prueba para operaciones CRUD de CARRERAS (CAREERS)
-- ⚠️ EJECUTAR TERCERO - SIN DEPENDENCIAS (pero necesaria para career_signatures)
-- Este es un dato base: necesario para career_signatures

-- ====================================
-- PRUEBAS DE CREACIÓN (CREATE)
-- ====================================
-- Insertar carreras de prueba
-- INSERT INTO careers (id, name, description, is_active)
-- VALUES 
--   (1, 'Ingeniería en Sistemas', 'Carrera de 5 años en sistemas computacionales', TRUE),
--   (2, 'Ingeniería en Electrónica', 'Carrera de 5 años en electrónica y control', TRUE),
--   (3, 'Administración de Empresas', 'Carrera de 4 años en administración', TRUE),
--   (4, 'Contabilidad', 'Carrera de 4 años en contabilidad', TRUE);


-- ====================================
-- PRUEBAS DE LECTURA (READ)
-- ====================================
-- Obtener todas las carreras
-- SELECT * FROM careers;

-- Obtener carreras activas
-- SELECT * FROM careers WHERE is_active = TRUE;

-- Buscar carrera por nombre
-- SELECT * FROM careers WHERE name LIKE '%Ingeniería%';

-- Obtener materias de una carrera (JOIN)
-- SELECT c.name as carrera, s.id as materia_id, s.name as materia FROM careers c
-- JOIN career_signatures cs ON c.id = cs.career_id
-- JOIN signatures s ON cs.signature_id = s.id
-- WHERE c.id = 1
-- ORDER BY s.name;

-- Contar materias por carrera
-- SELECT c.name as carrera, COUNT(cs.id) as cantidad_materias FROM careers c
-- LEFT JOIN career_signatures cs ON c.id = cs.career_id
-- GROUP BY c.id, c.name;


-- ====================================
-- PRUEBAS DE ACTUALIZACIÓN (UPDATE)
-- ====================================
-- Actualizar descripción de carrera
-- UPDATE careers SET description = 'Carrera de 4 años con énfasis en ciberseguridad' WHERE id = 1;

-- Desactivar carrera
-- UPDATE careers SET is_active = FALSE WHERE id = 4;

-- Reactivar carrera
-- UPDATE careers SET is_active = TRUE WHERE id = 4;

-- Cambiar nombre de carrera
-- UPDATE careers SET name = 'Ingeniería de Sistemas Computacionales' WHERE id = 1;


-- ====================================
-- PRUEBAS DE ELIMINACIÓN (DELETE)
-- ====================================
-- ⚠️ NO ELIMINAR si hay career_signatures asociadas
-- Verificar relaciones:
-- SELECT COUNT(*) FROM career_signatures WHERE career_id = 1;

-- Eliminar carrera (solo si no hay referenced)
-- DELETE FROM careers WHERE id = 4;
