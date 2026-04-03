-- Script de prueba para operaciones CRUD de ROLES
-- ⚠️ EJECUTAR PRIMERO - SIN DEPENDENCIAS
-- Este es un dato base: otros datos dependen de esto (users)

-- ====================================
-- PRUEBAS DE CREACIÓN (CREATE)
-- ====================================
-- Insertar roles de prueba
-- INSERT INTO roles (id, name, description, is_active)
-- VALUES 
--   (1, 'Administrador', 'Acceso completo al sistema', TRUE),
--   (2, 'Profesor', 'Acceso para gestionar grupos y asistencias', TRUE),
--   (3, 'Estudiante', 'Acceso limitado solo para ver asistencias', TRUE),
--   (4, 'Coordinador', 'Acceso para gestionar académica', TRUE);


-- ====================================
-- PRUEBAS DE LECTURA (READ)
-- ====================================
-- Obtener todos los roles
-- SELECT * FROM roles;

-- Obtener roles activos
-- SELECT * FROM roles WHERE is_active = TRUE;

-- Obtener rol por nombre
-- SELECT * FROM roles WHERE name = 'Profesor';

-- Obtener usuarios con rol específico (JOIN con users)
-- SELECT u.id, u.first_name, u.last_name, r.name as rol FROM users u
-- JOIN roles r ON u.role_id = r.id
-- WHERE r.name = 'Profesor';


-- ====================================
-- PRUEBAS DE ACTUALIZACIÓN (UPDATE)
-- ====================================
-- Actualizar descripción de rol
-- UPDATE roles SET description = 'Administrador del sistema con acceso total' WHERE name = 'Administrador';

-- Desactivar rol
-- UPDATE roles SET is_active = FALSE WHERE name = 'Coordinador';

-- Reactivar rol
-- UPDATE roles SET is_active = TRUE WHERE name = 'Coordinador';


-- ====================================
-- PRUEBAS DE ELIMINACIÓN (DELETE)
-- ====================================
-- ⚠️ NO ELIMINAR si hay usuarios con este rol
-- Verificar relaciones antes:
-- SELECT COUNT(*) FROM users WHERE role_id = 1;

-- Eliminar rol (solo si no hay referenced)
-- DELETE FROM roles WHERE id = 4;
