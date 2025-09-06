-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS AutoTest_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE AutoTest_db;

-- Tabla de categorías
CREATE TABLE categorias (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla principal de preguntas
CREATE TABLE preguntas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    texto_pregunta TEXT NOT NULL,
    imagen_url VARCHAR(255),
    explicacion TEXT,
    categoria_id INT,
    dificultad ENUM('facil', 'medio', 'dificil') DEFAULT 'medio',
    es_activa BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

-- Tabla de respuestas
CREATE TABLE respuestas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    pregunta_id INT NOT NULL,
    texto_respuesta TEXT NOT NULL,
    es_correcta BOOLEAN DEFAULT FALSE,
    orden_respuesta TINYINT DEFAULT 1,
    FOREIGN KEY (pregunta_id) REFERENCES preguntas(id) ON DELETE CASCADE
);

-- Insertar categorías básicas
INSERT INTO categorias (nombre, descripcion) VALUES
('Señales de Tráfico', 'Preguntas sobre señales de circulación'),
('Normas de Circulación', 'Normativa y reglamentación vial'),
('Seguridad Vial', 'Conducción segura y defensiva'),
('Mecánica y Mantenimiento', 'Aspectos técnicos del vehículo');

-- Insertar preguntas de ejemplo
INSERT INTO preguntas (texto_pregunta, explicacion, categoria_id) VALUES
('¿Cuál es la velocidad máxima en autopista para turismos?', 'La velocidad máxima genérica en autopistas para vehículos turismo es de 120 km/h', 2),
('¿Qué significa una señal triangular con borde rojo?', 'Las señales triangulares con borde rojo son señales de advertencia o peligro', 1),
('¿Cada cuánto tiempo se debe revisar la presión de los neumáticos?', 'Se recomienda revisar la presión al menos una vez al mes', 4);

-- Insertar respuestas de ejemplo
INSERT INTO respuestas (pregunta_id, texto_respuesta, es_correcta, orden_respuesta) VALUES
-- Pregunta 1: Velocidad en autopista
(1, '100 km/h', FALSE, 1),
(1, '120 km/h', TRUE, 2),
(1, '130 km/h', FALSE, 3),
-- Pregunta 2: Señal triangular
(2, 'Señal de prohibición', FALSE, 1),
(2, 'Señal de advertencia', TRUE, 2),
(2, 'Señal de información', FALSE, 3),
-- Pregunta 3: Presión neumáticos
(3, 'Cada semana', FALSE, 1),
(3, 'Cada mes', TRUE, 2),
(3, 'Cada 6 meses', FALSE, 3);