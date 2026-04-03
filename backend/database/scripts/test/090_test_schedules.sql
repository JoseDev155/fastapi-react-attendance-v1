-- Script de prueba para operaciones CRUD de HORARIOS (SCHEDULES)
-- ⚠️ EJECUTAR NOVENO - DEPENDE DE: groups (070)
-- Define los horarios en los que se reúne cada grupo

-- ====================================
-- PRUEBAS DE CREACIÓN (CREATE)
-- ====================================
-- Insertar horarios de prueba
-- Nota: group_id debe existir en groups
-- day_of_week: 0=Lunes, 1=Martes, 2=Miércoles, 3=Jueves, 4=Viernes, 5=Sábado, 6=Domingo (convención Python)
-- start_time y end_time en formato HH:MM:SS
-- INSERT INTO schedules (day_of_week, start_time, end_time, max_entry_minutes, minutes_to_be_late, group_id)
-- VALUES 
--   (0, '08:00:00'::time, '09:30:00'::time, 5, 30, 'GRP001'),   -- Lunes 8:00-9:30
--   (2, '08:00:00'::time, '09:30:00'::time, 5, 30, 'GRP001'),   -- Miércoles 8:00-9:30
--   (0, '10:00:00'::time, '11:30:00'::time, 5, 30, 'GRP002'),   -- Lunes 10:00-11:30
--   (2, '10:00:00'::time, '11:30:00'::time, 5, 30, 'GRP002'),   -- Miércoles 10:00-11:30
--   (1, '14:00:00'::time, '15:30:00'::time, 10, 40, 'GRP003'),  -- Martes 14:00-15:30
--   (3, '14:00:00'::time, '15:30:00'::time, 10, 40, 'GRP003'),  -- Jueves 14:00-15:30
--   (1, '16:00:00'::time, '17:30:00'::time, 10, 40, 'GRP004'),  -- Martes 16:00-17:30
--   (3, '16:00:00'::time, '17:30:00'::time, 10, 40, 'GRP004'),  -- Jueves 16:00-17:30
--   (4, '08:00:00'::time, '10:00:00'::time, 5, 30, 'GRP005');   -- Viernes 8:00-10:00 (laboratorio)


-- ====================================
-- PRUEBAS DE LECTURA (READ)
-- ====================================
-- Obtener todos los horarios
-- SELECT * FROM schedules;

-- Obtener horarios de un grupo (JOIN)
-- SELECT s.id, 
--        CASE WHEN s.day_of_week = 1 THEN 'Lunes'
--             WHEN s.day_of_week = 2 THEN 'Martes'
--             WHEN s.day_of_week = 3 THEN 'Miércoles'
--             WHEN s.day_of_week = 4 THEN 'Jueves'
--             WHEN s.day_of_week = 5 THEN 'Viernes'
--        END as día,
--        s.start_time, s.end_time, g.name as grupo FROM schedules s
-- JOIN groups g ON s.group_id = g.id
-- WHERE s.group_id = 'GRP001'
-- ORDER BY s.day_of_week, s.start_time;

-- Obtener horarios de un profesor (JOIN)
-- SELECT g.id as grupo, s.day_of_week, s.start_time, s.end_time FROM schedules s
-- JOIN groups g ON s.group_id = g.id
-- WHERE g.user_id = 'PROF001'
-- ORDER BY s.day_of_week, s.start_time;

-- Obtener horarios en un día específico (Lunes = 1)
-- SELECT g.id, g.name, s.start_time, s.end_time FROM schedules s
-- JOIN groups g ON s.group_id = g.id
-- WHERE s.day_of_week = 1
-- ORDER BY s.start_time;


-- ====================================
-- PRUEBAS DE ACTUALIZACIÓN (UPDATE)
-- ====================================
-- Cambiar hora de inicio
-- UPDATE schedules SET start_time = '08:30:00'::time WHERE id = 1;

-- Cambiar hora de fin
-- UPDATE schedules SET end_time = '10:00:00'::time WHERE id = 1;

-- Actualizar minutos máximos para entrada
-- UPDATE schedules SET max_entry_minutes = 10 WHERE group_id = 'GRP001';

-- Cambiar día de la semana
-- UPDATE schedules SET day_of_week = 5 WHERE id = 2;  -- Cambiar a Viernes


-- ====================================
-- PRUEBAS DE ELIMINACIÓN (DELETE)
-- ====================================
-- Eliminar un horario específico
-- DELETE FROM schedules WHERE id = 9;

-- Eliminar todos los horarios de un grupo
-- DELETE FROM schedules WHERE group_id = 'GRP005';

-- ⚠️ CUIDADO: Eliminar horarios puede afectar asistencias asociadas
-- Si attendances referencia schedules, primero verificar:
-- SELECT COUNT(*) FROM schedules WHERE group_id = 'GRP001';
