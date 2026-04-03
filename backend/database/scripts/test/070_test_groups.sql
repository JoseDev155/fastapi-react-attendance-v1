-- Script de prueba para operaciones CRUD de GRUPOS
-- ⚠️ EJECUTAR SÉPTIMO - DEPENDE DE: users (060), career_signatures (050), academic_cycles (040)
-- Define los grupos de estudiantes para cada materia por carrera y ciclo

-- ====================================
-- PRUEBAS DE CREACIÓN (CREATE)
-- ====================================
-- Insertar grupos de prueba
-- Nota: user_id (profesor), career_signature_id, academic_cycle_id deben existir
-- INSERT INTO groups (id, name, user_id, career_signature_id, academic_cycle_id)
-- VALUES 
--   ('GRP001', 'A', 'PROF001', 'CS001', 1),  -- Grupo A de Matemáticas I, Ing. Sistemas, 1er sem 2025
--   ('GRP002', 'B', 'PROF002', 'CS001', 1),  -- Grupo B de Matemáticas I
--   ('GRP003', 'A', 'PROF001', 'CS005', 1),  -- Grupo A de Programación I
--   ('GRP004', 'B', 'PROF002', 'CS005', 1),  -- Grupo B de Programación I
--   ('GRP005', 'A', 'PROF003', 'CS007', 1),  -- Grupo A de Bases de Datos I
--   ('GRP006', 'A', 'PROF001', 'CS002', 2),  -- Grupo A de Matemáticas II, 2do sem 2025
--   ('GRP007', 'A', 'PROF002', 'CS009', 1);  -- Grupo A de Matemáticas I, Ing. Electrónica


-- ====================================
-- PRUEBAS DE LECTURA (READ)
-- ====================================
-- Obtener todos los grupos
-- SELECT * FROM groups;

-- Obtener grupo por ID
-- SELECT * FROM groups WHERE id = 'GRP001';

-- Obtener grupos de un profesor (JOIN)
-- SELECT g.id, g.name, s.name as materia, c.name as carrera FROM groups g
-- JOIN users u ON g.user_id = u.id
-- JOIN career_signatures cs ON g.career_signature_id = cs.id
-- JOIN signatures s ON cs.signature_id = s.id
-- JOIN careers c ON cs.career_id = c.id
-- WHERE g.user_id = 'PROF001'
-- ORDER BY g.id;

-- Obtener grupos en un ciclo académico
-- SELECT g.id, g.name, u.first_name as profesor, s.name as materia FROM groups g
-- JOIN users u ON g.user_id = u.id
-- JOIN career_signatures cs ON g.career_signature_id = cs.id
-- JOIN signatures s ON cs.signature_id = s.id
-- WHERE g.academic_cycle_id = 1
-- ORDER BY g.id;

-- Contar estudiantes por grupo
-- SELECT g.id, g.name, COUNT(e.id) as cantidad_estudiantes FROM groups g
-- LEFT JOIN enrollments e ON g.id = e.group_id
-- GROUP BY g.id, g.name;


-- ====================================
-- PRUEBAS DE ACTUALIZACIÓN (UPDATE)
-- ====================================
-- Cambiar profesor de un grupo
-- UPDATE groups SET user_id = 'PROF002' WHERE id = 'GRP001';

-- Cambiar materia de un grupo (raramente se hace)
-- UPDATE groups SET career_signature_id = 'CS002' WHERE id = 'GRP001';


-- ====================================
-- PRUEBAS DE ELIMINACIÓN (DELETE)
-- ====================================
-- ⚠️ NO ELIMINAR si hay enrollments o schedules asociados
-- Verificar relaciones:
-- SELECT COUNT(*) FROM enrollments WHERE group_id = 'GRP001';
-- SELECT COUNT(*) FROM schedules WHERE group_id = 'GRP001';

-- Eliminar grupo (solo si no hay referenced)
-- DELETE FROM groups WHERE id = 'GRP007';
