-- Script de datos de prueba extraídos del Excel original ("Lista de Asistencias UBBJ.xlsx")
-- Incluye la recreación de la jerarquía completa de la aplicación.

-- 1. ROLES
INSERT INTO roles (name, description, is_active) VALUES 
('Admin', 'Administrador del sistema', TRUE),
('Professor', 'Profesor de la asignatura', TRUE);

-- 2. USUARIOS (Utilizando el Password de ejemplo: hashed_admin_password)
INSERT INTO users (id, first_name, last_name, email, password, is_active, role_id) VALUES 
('USR-A01', 'Admin', 'UBBJ', 'admin@ubbj.edu.mx', '$2b$12$SorGU9AYL.ZjKSa04uhI6OP4R3rNXUkyRLrNnwfpu8HbXZtSrRaCK', TRUE, 1),
('USR-P01', 'Profesor', 'Principal', 'profesor@ubbj.edu.mx', '$2b$12$SorGU9AYL.ZjKSa04uhI6OP4R3rNXUkyRLrNnwfpu8HbXZtSrRaCK', TRUE, 2);

-- 3. ASIGNATURAS (Signatures)
INSERT INTO signatures (id, name, description, is_active) VALUES 
('SIG-001', 'Taller de Sistemas de Información', 'Materia práctica', TRUE),
('SIG-002', 'Programación Orientada a Objetos', 'Materia práctica', TRUE);

-- 4. CARRERAS
INSERT INTO careers (name, description, is_active) VALUES 
('Ingeniería en Computación', 'Área de tecnología y software', TRUE),
('Ingeniería en Mecatrónica', 'Área de tecnología y mecatrónica', TRUE);

-- 5. RELACIÓN ASIGNATURA-CARRERA
INSERT INTO career_signatures (id, signature_id, career_id) VALUES 
('CS-001', 'SIG-001', 1),
('CS-002', 'SIG-002', 2);

-- 6. CICLOS ACADÉMICOS
INSERT INTO academic_cycles (cycle_name, cycle_year) VALUES 
('Ciclo A 2026', '2026-01-01');

-- 7. ESTUDIANTES (Datos exactos extraídos del Excel)
INSERT INTO students (id, nickname, first_name, last_name, email, enrollment_date, is_active) VALUES 
('ALU-1001', 'Mendoza', 'Jesus', 'Mendoza Carreola', 'jesus.mendoza@student.ubbj.edu', '2026-01-10', TRUE),
('ALU-1002', 'Moy', 'Moises', 'Escutia Loalza', 'moises.escutia@student.ubbj.edu', '2026-01-10', TRUE),
('ALU-1003', 'Diana', 'Diana', 'Becerra Lopez', 'diana.becerra@student.ubbj.edu', '2026-01-10', TRUE),
('ALU-1004', 'Gabe', 'Gabriel', 'Moreno Tapia', 'gabriel.moreno@student.ubbj.edu', '2026-01-10', TRUE),
('ALU-1005', 'Govea', 'Jose Jesus', 'Govea Navarro', 'jose.govea@student.ubbj.edu', '2026-01-10', TRUE),
('ALU-1006', 'Suyen', 'Suyen', 'Alcocez Hernandez', 'suyen.alcocez@student.ubbj.edu', '2026-01-10', TRUE),
('ALU-1007', 'Laura', 'Laura Alejandra', 'Arriola Mosqueda', 'laura.arriola@student.ubbj.edu', '2026-01-10', TRUE),
('ALU-1008', 'Esme', 'Esmeralda', 'Vera Alcaraz', 'esmeralda.vera@student.ubbj.edu', '2026-01-10', TRUE);

-- 8. GRUPOS (Asignado al profesor USR-P01)
INSERT INTO groups (id, name, user_id, career_signature_id, academic_cycle_id) VALUES 
('GRP001', 'TSI-A', 'USR-P01', 'CS-001', 1),
('GRP002', 'TSI-B', 'USR-P01', 'CS-002', 1);

-- 9. HORARIOS (Schedules)
-- Lunes (0), Martes (1), Miércoles (2), Jueves (3), Viernes (4).
-- En el Excel la hora de entraa ronda las 07:45 - 08:00 AM.
INSERT INTO schedules (id, day_of_week, start_time, end_time, max_entry_minutes, minutes_to_be_late, group_id) VALUES 
('SCH-001', 0, '08:00:00', '10:00:00', 15, 15, 'GRP002'), -- Lunes
('SCH-002', 1, '08:00:00', '10:00:00', 15, 15, 'GRP002'), -- Martes
('SCH-003', 2, '08:00:00', '10:00:00', 15, 15, 'GRP002'), -- Miércoles
('SCH-004', 3, '08:00:00', '10:00:00', 15, 15, 'GRP002'), -- Jueves
('SCH-005', 4, '08:00:00', '10:00:00', 15, 15, 'GRP002'); -- Viernes

-- 10. INSCRIPCIONES (Enrollments)
INSERT INTO enrollments (enrollment_date, student_id, group_id) VALUES 
('2026-01-15', 'ALU-1001', 'GRP002'), -- ID 1 (Mendoza)
('2026-01-15', 'ALU-1002', 'GRP002'), -- ID 2 (Moy)
('2026-01-15', 'ALU-1003', 'GRP002'), -- ID 3 (Diana)
('2026-01-15', 'ALU-1004', 'GRP002'), -- ID 4 (Gabe)
('2026-01-15', 'ALU-1005', 'GRP002'), -- ID 5 (Govea)
('2026-01-15', 'ALU-1006', 'GRP002'), -- ID 6 (Suyen)
('2026-01-15', 'ALU-1007', 'GRP002'), -- ID 7 (Laura)
('2026-01-15', 'ALU-1008', 'GRP002'); -- ID 8 (Esme)

-- 11. ASISTENCIAS (Attendances)
-- Extraído de la primera fecha del reporte del excel (Fecha Serial 45936) 
-- La fracción ej: 0.322916 equivale a las 07:45:00 AM (0.322916 * 24 horas = 7.749 = 07:45 hs)
-- La regla es simple: si llegan antes o a las 08:00: PRESENT. Límite de retardo 08:15.
INSERT INTO attendances (attendance_date, arrival_time, notes, enrollment_id) VALUES 
-- Mendoza (0.3229 -> 07:45:00)
('2026-01-19', '07:45:00', NULL, 1),
-- Moy (0.3236 -> 07:46:00)
('2026-01-19', '07:46:00', NULL, 2),
-- Diana (0.3256 -> 07:49:00)
('2026-01-19', '07:49:00', NULL, 3),
-- Gabe (0.3312 -> 07:57:00)
('2026-01-19', '07:57:00', NULL, 4),
-- Govea (0.3312 -> 07:57:00)
('2026-01-19', '07:57:00', NULL, 5),
-- Suyen (0.3333 -> 08:00:00)
('2026-01-19', '08:00:00', NULL, 6),
-- Laura (0.3333 -> 08:00:00)
('2026-01-19', '08:00:00', NULL, 7),
-- Esme (0.4236 -> 10:10:00) - Llegó extremadamente tarde. Se contará como LEFT_EARLY/ABSENT
('2026-01-19', '10:10:00', 'Llegada reportada tras de límite de la clase', 8),

-- Segunda fecha extraída (Fecha Serial 45937)
-- Mendoza (0.3229 -> 07:45:00)
('2026-01-20', '07:45:00', NULL, 1),
-- Moy (0.3236 -> 07:46:00)
('2026-01-20', '07:46:00', NULL, 2),
-- Diana (0.3263 -> 07:50:00)
('2026-01-20', '07:50:00', NULL, 3),
-- Gabe (0.3298 -> 07:55:00)
('2026-01-20', '07:55:00', NULL, 4),
-- Govea (0.3125 -> 07:30:00) - Llegó super temprano
('2026-01-20', '07:30:00', NULL, 5),
-- Suyen (0.3305 -> 07:56:00)
('2026-01-20', '07:56:00', NULL, 6),
-- Laura (0.3319 -> 07:58:00)
('2026-01-20', '07:58:00', NULL, 7),
-- Esme (0.3250 -> 07:48:00)
('2026-01-20', '07:48:00', NULL, 8);
