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

