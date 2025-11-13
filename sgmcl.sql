-- ======================================================
-- 🧠 SISTEMA DE GESTIÓN DE MANTENIMIENTO CORRECTIVO (SGMCL)
-- Laboratorio de Cómputo Escolar
-- Versión mejorada para múltiples equipos por tipo
-- ======================================================

DROP DATABASE IF EXISTS sgmcl;
CREATE DATABASE sgmcl CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE sgmcl;

-- ======================================================
-- TABLAS PRINCIPALES
-- ======================================================

-- 1️⃣ Usuarios del sistema
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    contrasena VARCHAR(100) NOT NULL,
    rol ENUM('Administrador', 'Técnico') NOT NULL,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2️⃣ Catálogo de tipos de equipo (para clasificar)
CREATE TABLE tipos_equipo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255)
);

-- 3️⃣ Equipos registrados en el laboratorio
CREATE TABLE equipos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    id_tipo INT NOT NULL,
    marca VARCHAR(50),
    modelo VARCHAR(50),
    numero_serie VARCHAR(100),
    ubicacion VARCHAR(100),
    estado ENUM('Operativo', 'En mantenimiento', 'Con falla', 'Fuera de servicio') DEFAULT 'Operativo',
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_tipo) REFERENCES tipos_equipo(id) ON DELETE CASCADE
);

-- 4️⃣ Fallas reportadas en equipos
CREATE TABLE fallas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_equipo INT NOT NULL,
    descripcion TEXT,
    fecha_reporte DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_equipo) REFERENCES equipos(id) ON DELETE CASCADE
);

-- 5️⃣ Tareas correctivas generadas
CREATE TABLE tareas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_falla INT NOT NULL,
    id_tecnico INT,
    prioridad ENUM('Alta', 'Media', 'Baja') NOT NULL,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_limite DATETIME,
    estado ENUM('Pendiente', 'En proceso', 'Completada') DEFAULT 'Pendiente',
    observaciones TEXT,
    FOREIGN KEY (id_falla) REFERENCES fallas(id) ON DELETE CASCADE,
    FOREIGN KEY (id_tecnico) REFERENCES usuarios(id)
);

-- 6️⃣ Inventario de repuestos
CREATE TABLE repuestos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo VARCHAR(100),
    cantidad INT DEFAULT 0,
    stock_minimo INT DEFAULT 1,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 7️⃣ Historial de mantenimientos realizados
CREATE TABLE historial (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_tarea INT NOT NULL,
    fecha_cierre DATETIME DEFAULT CURRENT_TIMESTAMP,
    descripcion TEXT,
    repuesto_usado VARCHAR(100),
    FOREIGN KEY (id_tarea) REFERENCES tareas(id) ON DELETE CASCADE
);

-- 8️⃣ Registro de alertas generadas automáticamente
CREATE TABLE alertas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(50),
    mensaje TEXT,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ======================================================
-- DATOS INICIALES
-- ======================================================

-- Tipos de equipos (catálogo base)
INSERT INTO tipos_equipo (nombre, descripcion) VALUES
('Computadora', 'Equipo de cómputo personal o de escritorio'),
('Switch', 'Equipo de red para conexión de PCs'),
('Proyector', 'Dispositivo de proyección'),
('Cable UTP', 'Infraestructura de red y energía'),
('Impresora', 'Equipo periférico de impresión');

-- Usuarios iniciales
INSERT INTO usuarios (nombre, usuario, contrasena, rol) VALUES
('Administrador General', 'admin', 'admin123', 'Administrador'),
('Técnico Juan', 'juan', 'tecnico123', 'Técnico');

-- Equipos de ejemplo (varias computadoras y switches)
INSERT INTO equipos (nombre, id_tipo, marca, modelo, numero_serie, ubicacion, estado) VALUES
('PC-01', 1, 'HP', 'ProDesk 400', 'SN001', 'Laboratorio 1', 'Operativo'),
('PC-02', 1, 'HP', 'ProDesk 400', 'SN002', 'Laboratorio 1', 'Operativo'),
('PC-03', 1, 'Lenovo', 'ThinkCentre', 'SN003', 'Laboratorio 2', 'Operativo'),
('Switch-01', 2, 'Cisco', 'SG95-08', 'SW001', 'Rack Principal', 'Operativo'),
('Switch-02', 2, 'TP-Link', 'TL-SG1008D', 'SW002', 'Laboratorio 2', 'Operativo'),
('Proyector-01', 3, 'Epson', 'X100', 'PR001', 'Laboratorio 1', 'Operativo'),
('Cable Cat6 Azul', 4, 'Belden', 'Cat6', 'CB001', 'Infraestructura', 'Operativo');

-- Repuestos iniciales
INSERT INTO repuestos (nombre, tipo, cantidad, stock_minimo) VALUES
('Fuente de poder 500W', 'Componente PC', 5, 2),
('Cable HDMI 2m', 'Conector', 10, 3),
('Ventilador CPU', 'Componente PC', 8, 2),
('Switch 8 puertos TP-Link', 'Equipo de red', 2, 1);

-- ======================================================
-- ✅ Esquema preparado para Flask o PHP
-- ======================================================
