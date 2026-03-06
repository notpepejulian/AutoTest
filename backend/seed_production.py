#!/usr/bin/env python3
import os
import sys

# Añadir el directorio actual al path para importar modelos y base de datos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models
from models import DificultadEnum
import models_auth
import auth_backend

def seed_production():
    print("🚀 Iniciando seeding de producción...")
    db = SessionLocal()
    
    try:
        # 1. Eliminar y recrear esquema para evitar problemas de sincronización de columnas
        print("🛠️  Recreando esquema de base de datos...")
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

        # 2. Crear usuario de test
        test_user = auth_backend.get_usuario_by_username(db, "admin")
        if not test_user:
            print("👤 Creando usuario de prueba (admin / admin123)...")
            nuevo_usuario = models_auth.Usuario(
                email="admin@autotest.com",
                username="admin",
                password_hash=models_auth.Usuario.hash_password("admin123"),
                nombre="Admin",
                apellidos="AutoTest",
                is_active=True,
                is_verified=True,
                chatbot_preguntas_dia=100
            )
            db.add(nuevo_usuario)
            db.commit()

        # 3. Asegurar categorías
        categorias_data = [
            {"id": 1, "nombre": "Señales de Tráfico", "descripcion": "Señalización vertical, marcas viales y semáforos."},
            {"id": 2, "nombre": "Normas de Circulación", "descripcion": "Prioridades, velocidad, adelantamientos y maniobras."},
            {"id": 3, "nombre": "Seguridad Vial", "descripcion": "Alcohol, fatiga, distracciones y técnicas de conducción."},
            {"id": 4, "nombre": "Mecánica y Mantenimiento", "descripcion": "Sistemas del vehículo, neumáticos y revisiones."},
            {"id": 5, "nombre": "Test Mixtos", "descripcion": "Exámenes completos con preguntas de todas las categorías"}
        ]

        categorias = []
        for cat in categorias_data:
            existing_cat = db.query(models.Categoria).filter(models.Categoria.id == cat["id"]).first()
            if not existing_cat:
                new_cat = models.Categoria(**cat)
                db.add(new_cat)
                db.flush()
                categorias.append(new_cat)
            else:
                existing_cat.nombre = cat["nombre"]
                categorias.append(existing_cat)
        db.commit()

        # 4. Generar 40 preguntas por cada categoría
        print("📚 Generando preguntas...")
        banco_base = [
            # Categoria 1: Señales
            {"t": "¿Qué indica la señal X?", "r1": "Correcta", "r2": "Incorrecta 1", "r3": "Incorrecta 2"},
            # Esto se multiplicará
        ]
        
        for cat_id in range(1, 5):
            for i in range(1, 41):
                pregunta = models.Pregunta(
                    texto_pregunta=f"Pregunta de prueba generada automáticamente {i} para la categoría {cat_id}?",
                    explicacion=f"Explicación detallada para la pregunta {i} de la categoría {cat_id}.",
                    categoria_id=cat_id,
                    dificultad=DificultadEnum.medio
                )
                db.add(pregunta)
                db.flush()
                
                respuestas = [
                    {"texto": f"Respuesta correcta {i}", "correcta": True},
                    {"texto": f"Respuesta incorrecta A {i}", "correcta": False},
                    {"texto": f"Respuesta incorrecta B {i}", "correcta": False}
                ]
                
                import random
                random.shuffle(respuestas)
                
                for j, r_data in enumerate(respuestas, 1):
                    respuesta = models.Respuesta(
                        pregunta_id=pregunta.id,
                        texto_respuesta=r_data["texto"],
                        es_correcta=r_data["correcta"],
                        orden_respuesta=j
                    )
                    db.add(respuesta)

        db.commit()
        
        # 5. Generar exámenes
        print("📄 Generando exámenes...")
        todas_preguntas = db.query(models.Pregunta).all()
        
        for i in range(1, 6):
            examen = models.Examen(
                nombre=f"Examen Oficial Variante {i}",
                descripcion=f"Simulacro oficial número {i}",
                duracion_minutos=30,
                num_preguntas=30,
                categoria_principal_id=5,
                es_activo=True
            )
            db.add(examen)
            db.flush()
            
            # Asignar 30 preguntas aleatorias
            import random
            preguntas_examen = random.sample(todas_preguntas, 30)
            
            for orden, pre in enumerate(preguntas_examen, 1):
                pe = models.PreguntaExamen(
                    examen_id=examen.id,
                    pregunta_id=pre.id,
                    orden_pregunta=orden
                )
                db.add(pe)
                
        db.commit()
        print("✅ Seeding completado con éxito.")

    except Exception as e:
        db.rollback()
        print(f"❌ Error durante el seeding: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    import auth_backend
    seed_production()
