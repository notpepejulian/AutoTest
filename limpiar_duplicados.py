#!/usr/bin/env python3
"""
Script para limpiar preguntas duplicadas y normalizar el formato de respuestas
"""
import sys
import os
sys.path.append('backend')

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Configuración directa de conexión
DATABASE_URL = "mysql+pymysql://nj17dssdsnj:zGmPTVYFkTQBUP2V7uizIfWjs5@localhost:3306/autotest_db"
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def limpiar_duplicados():
    """Limpia preguntas duplicadas manteniendo solo la primera ocurrencia"""
    
    print("🔄 Iniciando limpieza de preguntas duplicadas...")
    
    # Usar conexión directa para operaciones complejas
    with engine.connect() as connection:
        
        # 1. Identificar preguntas duplicadas
        query_duplicados = text("""
            SELECT MIN(id) as id_mantener, texto_pregunta, COUNT(*) as duplicados
            FROM preguntas 
            GROUP BY texto_pregunta 
            HAVING COUNT(*) > 1
        """)
        
        duplicados = connection.execute(query_duplicados).fetchall()
        print(f"📊 Encontradas {len(duplicados)} preguntas únicas con duplicados")
        
        total_eliminadas = 0
        
        for duplicado in duplicados:
            # 2. Eliminar todas las ocurrencias excepto la primera
            query_eliminar = text("""
                DELETE FROM preguntas 
                WHERE texto_pregunta = :texto_pregunta 
                AND id > :id_mantener
            """)
            
            result = connection.execute(query_eliminar, {
                'texto_pregunta': duplicado.texto_pregunta,
                'id_mantener': duplicado.id_mantener
            })
            
            eliminadas = result.rowcount
            total_eliminadas += eliminadas
            
            print(f"  ✅ '{duplicado.texto_pregunta[:60]}...' - Eliminadas {eliminadas} duplicadas")
        
        # 3. Normalizar preguntas con 4 respuestas (eliminar la 4ta respuesta)
        query_4_respuestas = text("""
            SELECT p.id, p.texto_pregunta
            FROM preguntas p
            WHERE (SELECT COUNT(*) FROM respuestas r WHERE r.pregunta_id = p.id) = 4
        """)
        
        preguntas_4_resp = connection.execute(query_4_respuestas).fetchall()
        print(f"📊 Encontradas {len(preguntas_4_resp)} preguntas con 4 respuestas")
        
        for pregunta in preguntas_4_resp:
            # Eliminar la respuesta con mayor orden_respuesta (la 4ta)
            query_eliminar_4ta = text("""
                DELETE FROM respuestas 
                WHERE pregunta_id = :pregunta_id 
                AND orden_respuesta = (
                    SELECT MAX(orden_respuesta) 
                    FROM (SELECT orden_respuesta FROM respuestas WHERE pregunta_id = :pregunta_id) as sub
                )
            """)
            
            connection.execute(query_eliminar_4ta, {'pregunta_id': pregunta.id})
            print(f"  ✅ Normalizada pregunta ID {pregunta.id}")
        
        # 4. Commit de los cambios
        connection.commit()
        
        print(f"\n🎉 Limpieza completada:")
        print(f"  📝 Total preguntas duplicadas eliminadas: {total_eliminadas}")
        print(f"  🔧 Total preguntas normalizadas (4→3 respuestas): {len(preguntas_4_resp)}")
        
        # 5. Estadísticas finales
        query_stats = text("""
            SELECT COUNT(*) as total_preguntas FROM preguntas;
        """)
        total_final = connection.execute(query_stats).fetchone()
        print(f"  📊 Total preguntas restantes: {total_final.total_preguntas}")

def verificar_integridad():
    """Verifica la integridad de las preguntas restantes"""
    
    print("\n🔍 Verificando integridad de datos...")
    
    with engine.connect() as connection:
        
        # Verificar preguntas sin respuestas
        query_sin_respuestas = text("""
            SELECT COUNT(*) as count
            FROM preguntas p
            LEFT JOIN respuestas r ON p.id = r.pregunta_id
            WHERE r.id IS NULL
        """)
        
        sin_respuestas = connection.execute(query_sin_respuestas).fetchone()
        
        # Verificar preguntas sin respuesta correcta
        query_sin_correcta = text("""
            SELECT COUNT(*) as count
            FROM preguntas p
            WHERE NOT EXISTS (
                SELECT 1 FROM respuestas r 
                WHERE r.pregunta_id = p.id AND r.es_correcta = 1
            )
        """)
        
        sin_correcta = connection.execute(query_sin_correcta).fetchone()
        
        # Distribución de respuestas
        query_distribucion = text("""
            SELECT num_respuestas, COUNT(*) as preguntas
            FROM (
                SELECT p.id, COUNT(r.id) as num_respuestas
                FROM preguntas p 
                LEFT JOIN respuestas r ON p.id = r.pregunta_id 
                GROUP BY p.id
            ) as sub
            GROUP BY num_respuestas
            ORDER BY num_respuestas
        """)
        
        distribucion = connection.execute(query_distribucion).fetchall()
        
        print(f"  ⚠️  Preguntas sin respuestas: {sin_respuestas.count}")
        print(f"  ⚠️  Preguntas sin respuesta correcta: {sin_correcta.count}")
        print("  📊 Distribución de número de respuestas:")
        for dist in distribucion:
            print(f"    {dist.num_respuestas} respuestas: {dist.preguntas} preguntas")

if __name__ == "__main__":
    try:
        limpiar_duplicados()
        verificar_integridad()
        print("\n✅ Proceso completado exitosamente")
    except Exception as e:
        print(f"\n❌ Error durante la limpieza: {e}")
        raise