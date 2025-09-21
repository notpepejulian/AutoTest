-- ========================================
-- SCRIPT DE CORRECCIÓN DE IDs DE EXÁMENES
-- ========================================
-- Propósito: Normalizar los IDs de exámenes para que inicien en 1

USE autotest_db;

-- PASO 1: Crear tabla temporal para mapear IDs antiguos a nuevos
CREATE TEMPORARY TABLE temp_id_mapping AS
SELECT 
    id as old_id,
    ROW_NUMBER() OVER (ORDER BY id) as new_id
FROM examenes 
ORDER BY id;

-- PASO 2: Crear tabla de respaldo de exámenes
CREATE TABLE examenes_backup AS SELECT * FROM examenes;

-- PASO 3: Crear tabla de respaldo de relaciones pregunta-examen
CREATE TABLE preguntas_examenes_backup AS SELECT * FROM preguntas_examenes;

-- PASO 4: Deshabilitar verificación de claves foráneas temporalmente
SET FOREIGN_KEY_CHECKS = 0;

-- PASO 5: Actualizar las relaciones en preguntas_examenes usando el mapeo
UPDATE preguntas_examenes pe 
INNER JOIN temp_id_mapping tm ON pe.examen_id = tm.old_id 
SET pe.examen_id = tm.new_id;

-- PASO 6: Actualizar los IDs en la tabla examenes
UPDATE examenes e 
INNER JOIN temp_id_mapping tm ON e.id = tm.old_id 
SET e.id = tm.new_id;

-- PASO 7: Reiniciar el AUTO_INCREMENT a partir del siguiente ID disponible
SET @max_id = (SELECT COALESCE(MAX(id), 0) FROM examenes);
SET @sql = CONCAT('ALTER TABLE examenes AUTO_INCREMENT = ', @max_id + 1);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- PASO 8: Reactivar verificación de claves foráneas
SET FOREIGN_KEY_CHECKS = 1;

-- PASO 9: Verificar los resultados
SELECT 
    'ANTES DE LA CORRECCIÓN' as estado,
    COUNT(*) as total_examenes,
    MIN(id) as id_minimo,
    MAX(id) as id_maximo
FROM examenes_backup

UNION ALL

SELECT 
    'DESPUÉS DE LA CORRECCIÓN' as estado,
    COUNT(*) as total_examenes,
    MIN(id) as id_minimo,
    MAX(id) as id_maximo
FROM examenes;

-- PASO 10: Mostrar estadísticas de la corrección
SELECT 
    CONCAT('IDs corregidos de ', 
           (SELECT MIN(old_id) FROM temp_id_mapping),
           '-',
           (SELECT MAX(old_id) FROM temp_id_mapping),
           ' a 1-',
           (SELECT MAX(new_id) FROM temp_id_mapping)
    ) as correccion_aplicada;

-- ADVERTENCIA: Eliminar tablas de respaldo solo después de verificar que todo funciona correctamente
-- DROP TABLE examenes_backup;
-- DROP TABLE preguntas_examenes_backup;

COMMIT;