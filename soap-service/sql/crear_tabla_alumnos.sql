-- ============================================
-- Script SQL para crear tabla ALUMNOS
-- Sistema de Integración Académica - UAV
-- Base de datos: MySQL Railway
-- ============================================

-- Crear tabla alumnos
CREATE TABLE IF NOT EXISTS alumnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    matricula VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_matricula (matricula),
    INDEX idx_email (email),
    INDEX idx_nombre (nombre),
    INDEX idx_apellido (apellido)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Datos de ejemplo para pruebas
-- ============================================

INSERT INTO alumnos (matricula, nombre, apellido, email) VALUES
('S20014578', 'Juan Carlos', 'García López', 'juan.garcia@uv.mx'),
('S20014579', 'María Fernanda', 'Rodríguez Pérez', 'maria.rodriguez@uv.mx'),
('S20014580', 'Pedro Antonio', 'Martínez Sánchez', 'pedro.martinez@uv.mx'),
('S20014581', 'Ana Laura', 'Hernández Gómez', 'ana.hernandez@uv.mx'),
('S20014582', 'Luis Miguel', 'Díaz Torres', 'luis.diaz@uv.mx');

-- ============================================
-- Verificar datos insertados
-- ============================================

SELECT * FROM alumnos;

-- ============================================
-- Consultas útiles para pruebas
-- ============================================

-- Ver todos los alumnos registrados
SELECT * FROM alumnos ORDER BY fecha_registro DESC;

-- Buscar alumno por matrícula
SELECT * FROM alumnos WHERE matricula = 'S20014578';

-- Buscar alumnos por nombre
SELECT * FROM alumnos WHERE nombre LIKE '%Juan%';

-- Contar total de alumnos
SELECT COUNT(*) as total_alumnos FROM alumnos;

-- Ver alumnos registrados hoy
SELECT * FROM alumnos WHERE DATE(fecha_registro) = CURDATE();

-- Verificar unicidad de matrícula
SELECT matricula, COUNT(*) as repeticiones
FROM alumnos
GROUP BY matricula
HAVING repeticiones > 1;

-- Verificar unicidad de email
SELECT email, COUNT(*) as repeticiones
FROM alumnos
GROUP BY email
HAVING repeticiones > 1;
