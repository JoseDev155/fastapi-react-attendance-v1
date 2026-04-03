-- Script de prueba para operaciones CRUD de CICLOS ACADÉMICOS (ACADEMIC_CYCLES)
-- ⚠️ EJECUTAR CUARTO - SIN DEPENDENCIAS (pero necesaria para groups)
-- Este es un dato base: necesario para groups

-- ====================================
-- PRUEBAS DE CREACIÓN (CREATE)
-- ====================================
-- Insertar ciclos académicos de prueba
-- INSERT INTO academic_cycles (cycle_name, cycle_year, is_active)
-- VALUES 
--   ('Primer semestre 2025', '2025-01-01'::date, TRUE),
--   ('Segundo semestre 2025', '2025-06-01'::date, TRUE),
--   ('Primer semestre 2026', '2026-01-01'::date, FALSE),
--   ('Segundo semestre 2026', '2026-06-01'::date, FALSE);


-- ====================================
-- PRUEBAS DE LECTURA (READ)
-- ====================================
-- Obtener todos los ciclos académicos
-- SELECT * FROM academic_cycles;

-- Obtener ciclos académicos activos
-- SELECT * FROM academic_cycles WHERE is_active = TRUE;

-- Obtener ciclo por nombre
-- SELECT * FROM academic_cycles WHERE cycle_name LIKE '%2025%';

-- Obtener grupos en un ciclo académico (JOIN)
-- SELECT ac.cycle_name, COUNT(g.id) as cantidad_grupos FROM academic_cycles ac
-- LEFT JOIN groups g ON ac.id = g.academic_cycle_id
-- GROUP BY ac.id, ac.cycle_name;


-- ====================================
-- PRUEBAS DE ACTUALIZACIÓN (UPDATE)
-- ====================================
-- Actualizar nombre de ciclo
-- UPDATE academic_cycles SET cycle_name = 'Primer semestre 2026' WHERE id = 3;

-- Cambiar año de ciclo
-- UPDATE academic_cycles SET cycle_year = '2025-09-01'::date WHERE cycle_name = 'Segundo semestre 2025';

-- Desactivar ciclo
-- UPDATE academic_cycles SET is_active = FALSE WHERE cycle_name = 'Primer semestre 2025';

-- Reactivar ciclo
-- UPDATE academic_cycles SET is_active = TRUE WHERE cycle_name = 'Primer semestre 2025';


-- ====================================
-- PRUEBAS DE ELIMINACIÓN (DELETE)
-- ====================================
-- ⚠️ NO ELIMINAR si hay groups asociados
-- Verificar relaciones:
-- SELECT COUNT(*) FROM groups WHERE academic_cycle_id = 1;

-- Eliminar ciclo académico (solo si no hay referenced)
-- DELETE FROM academic_cycles WHERE id = 4;
