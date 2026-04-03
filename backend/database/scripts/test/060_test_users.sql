-- Script de prueba para operaciones CRUD de USUARIOS
-- ⚠️ EJECUTAR SEXTO - DEPENDE DE: roles (010)
-- Crear usuarios del sistema (profesores, coordinadores, administradores)

-- ====================================
-- PRUEBAS DE CREACIÓN (CREATE)
-- ====================================
-- Insertar usuarios de prueba
-- Nota: role_id debe existir en roles
-- reminder: password debe ser hasheado con get_password_hash()
-- INSERT INTO users (id, first_name, last_name, email, password, role_id, is_active)
-- VALUES 
--   ('ADM001', 'Admin', 'Sistema', 'admin@ubbj.edu', 'hashed_admin_password', 1, TRUE),
--   ('PROF001', 'Julio', 'Ramírez', 'julio.ramirez@ubbj.edu', 'hashed_prof_password_1', 2, TRUE),
--   ('PROF002', 'María', 'García', 'maria.garcia@ubbj.edu', 'hashed_prof_password_2', 2, TRUE),
--   ('PROF003', 'Carlos', 'López', 'carlos.lopez@ubbj.edu', 'hashed_prof_password_3', 2, TRUE),
--   ('COORD001', 'Patricia', 'Mendez', 'patricia.mendez@ubbj.edu', 'hashed_coord_password', 4, TRUE);


-- ====================================
-- PRUEBAS DE LECTURA (READ)
-- ====================================
-- Obtener todos los usuarios
-- SELECT id, first_name, last_name, email, role_id, is_active FROM users;

-- Obtener usuario por ID
-- SELECT * FROM users WHERE id = 'PROF001';

-- Obtener usuarios activos
-- SELECT id, first_name, last_name, email FROM users WHERE is_active = TRUE;

-- Obtener usuarios por rol (JOIN)
-- SELECT u.id, u.first_name, u.last_name, r.name as rol FROM users u
-- JOIN roles r ON u.role_id = r.id
-- WHERE r.name = 'Profesor'
-- ORDER BY u.last_name;

-- Obtener todos los profesores
-- SELECT id, first_name, last_name, email FROM users 
-- WHERE role_id = 2 AND is_active = TRUE;

-- Buscar usuario por email
-- SELECT * FROM users WHERE email = 'julio.ramirez@ubbj.edu';


-- ====================================
-- PRUEBAS DE ACTUALIZACIÓN (UPDATE)
-- ====================================
-- Actualizar nombre de usuario
-- UPDATE users SET first_name = 'Julio César' WHERE id = 'PROF001';

-- Actualizar email
-- UPDATE users SET email = 'julio.cesar@ubbj.edu' WHERE id = 'PROF001';

-- Desactivar usuario (soft delete)
-- UPDATE users SET is_active = FALSE WHERE id = 'PROF003';

-- Reactivar usuario
-- UPDATE users SET is_active = TRUE WHERE id = 'PROF003';


-- ====================================
-- PRUEBAS DE ELIMINACIÓN (DELETE)
-- ====================================
-- ⚠️ NO ELIMINAR si hay groups donde user_id apunta a este usuario
-- Verificar relaciones:
-- SELECT COUNT(*) FROM groups WHERE user_id = 'PROF001';

-- Eliminar usuario (solo si no hay groups referenced)
-- DELETE FROM users WHERE id = 'PROF003';
