-- Script de prueba para operaciones CRUD de RELACIÓN CARRERA-MATERIA (CAREER_SIGNATURES)
-- ⚠️ EJECUTAR QUINTO - DEPENDE DE: careers (030), signatures (020)
-- Define qué materias pertenecen a cada carrera

-- ====================================
-- PRUEBAS DE CREACIÓN (CREATE)
-- ====================================
-- Insertar relaciones carrera-materia de prueba
-- Nota: career_id debe existir en careers, signature_id debe existir en signatures
-- INSERT INTO career_signatures (id, signature_id, career_id)
-- VALUES 
--   ('CS001', 'MAT001', 1),  -- Ingeniería Sistemas tiene Matemáticas I
--   ('CS002', 'MAT002', 1),
--   ('CS003', 'FIS001', 1),
--   ('CS004', 'FIS002', 1),
--   ('CS005', 'PRO001', 1),
--   ('CS006', 'PRO002', 1),
--   ('CS007', 'BDD001', 1),
--   ('CS008', 'BDD002', 1),
--   ('CS009', 'MAT001', 2),  -- Ingeniería Electrónica tiene Matemáticas I
--   ('CS010', 'FIS001', 2),
--   ('CS011', 'FIS002', 2),
--   ('CS012', 'MAT001', 3),  -- Administración tiene Matemáticas I
--   ('CS013', 'MAT001', 4);  -- Contabilidad tiene Matemáticas I


-- ====================================
-- PRUEBAS DE LECTURA (READ)
-- ====================================
-- Obtener todas las relaciones carrera-materia
-- SELECT * FROM career_signatures;

-- Obtener materias de una carrera específica
-- SELECT cs.id, s.name as materia, c.name as carrera FROM career_signatures cs
-- JOIN signatures s ON cs.signature_id = s.id
-- JOIN careers c ON cs.career_id = c.id
-- WHERE c.id = 1
-- ORDER BY s.name;

-- Obtener carreras que ofrecen una materia
-- SELECT DISTINCT c.name as carrera FROM career_signatures cs
-- JOIN careers c ON cs.career_id = c.id
-- WHERE cs.signature_id = 'MAT001';

-- Contar materias por carrera
-- SELECT c.name as carrera, COUNT(cs.id) as cantidad_materias FROM careers c
-- LEFT JOIN career_signatures cs ON c.id = cs.career_id
-- GROUP BY c.id, c.name
-- ORDER BY c.name;


-- ====================================
-- PRUEBAS DE ACTUALIZACIÓN (UPDATE)
-- ====================================
-- ⚠️ CUIDADO: Actualizar la materia de una relación afecta grupos
-- Cambiar materia de un career_signature
-- UPDATE career_signatures SET signature_id = 'BDD001' WHERE id = 'CS010';


-- ====================================
-- PRUEBAS DE ELIMINACIÓN (DELETE)
-- ====================================
-- ⚠️ NO ELIMINAR si hay groups que usen este career_signature
-- Verificar relaciones:
-- SELECT COUNT(*) FROM groups WHERE career_signature_id = 'CS001';

-- Eliminar relación carrera-materia (solo si no hay groups referenced)
-- DELETE FROM career_signatures WHERE id = 'CS013';
