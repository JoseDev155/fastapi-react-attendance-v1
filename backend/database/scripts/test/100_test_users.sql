-- Script de prueba para operaciones CRUD de usuarios
-- Este archivo contiene plantillas para pruebas de usuarios
-- NO incluye datos de seed, solo estructura para pruebas

-- ====================================
-- PRUEBAS DE CREACIÓN (CREATE)
-- ====================================
-- Insertar usuarios de prueba
-- INSERT INTO users (id, first_name, last_name, email, password, role_id, is_active)
-- VALUES 
--   ('USR001', 'Juan', 'Pérez', 'juan@example.com', 'hashed_password_1', 1, TRUE),
--   ('USR002', 'María', 'González', 'maria@example.com', 'hashed_password_2', 2, TRUE),
--   ('USR003', 'Carlos', 'López', 'carlos@example.com', 'hashed_password_3', 2, TRUE);


-- ====================================
-- PRUEBAS DE LECTURA (READ)
-- ====================================
-- Obtener todos los usuarios
-- SELECT * FROM users;

-- Obtener usuario por ID
-- SELECT * FROM users WHERE id = 'USR001';

-- Obtener usuarios activos
-- SELECT * FROM users WHERE is_active = TRUE;

-- Obtener usuarios por rol
-- SELECT * FROM users WHERE role_id = 2;


-- ====================================
-- PRUEBAS DE ACTUALIZACIÓN (UPDATE)
-- ====================================
-- Actualizar nombre de usuario
-- UPDATE users SET first_name = 'Juan Carlos' WHERE id = 'USR001';

-- Actualizar email de usuario
-- UPDATE users SET email = 'juancarlos@example.com' WHERE id = 'USR001';

-- Desactivar usuario (soft delete)
-- UPDATE users SET is_active = FALSE WHERE id = 'USR003';

-- Reactivar usuario
-- UPDATE users SET is_active = TRUE WHERE id = 'USR003';


-- ====================================
-- PRUEBAS DE ELIMINACIÓN (DELETE)
-- ====================================
-- Eliminar usuario (hard delete - solo si no tiene referencias)
-- DELETE FROM users WHERE id = 'USR001';
