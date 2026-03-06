#!/usr/bin/env python3
import os
import sys

# Añadir el directorio actual al path para importar modelos y base de datos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from models import DificultadEnum

def seed_professional_questions():
    print("🚀 Iniciando seeding de preguntas profesionales (Estilo DGT)...")
    db = SessionLocal()
    
    try:
        # 1. Limpiar datos existentes de preguntas (opcional, pero recomendado para calidad)
        # db.query(models.Respuesta).delete()
        # db.query(models.Pregunta).delete()
        # db.commit()

        # 2. Asegurar que las categorías existen
        categorias_data = [
            {"id": 1, "nombre": "Señales de Tráfico", "descripcion": "Señalización vertical, marcas viales y semáforos."},
            {"id": 2, "nombre": "Normas de Circulación", "descripcion": "Prioridades, velocidad, adelantamientos y maniobras."},
            {"id": 3, "nombre": "Seguridad Vial", "descripcion": "Alcohol, fatiga, distracciones y técnicas de conducción."},
            {"id": 4, "nombre": "Mecánica y Mantenimiento", "descripcion": "Sistemas del vehículo, neumáticos y revisiones."},
            {"id": 5, "nombre": "Primeros Auxilios", "descripcion": "Actuación en caso de accidente y protocolo PAS."}
        ]

        for cat in categorias_data:
            existing_cat = db.query(models.Categoria).filter(models.Categoria.id == cat["id"]).first()
            if not existing_cat:
                new_cat = models.Categoria(**cat)
                db.add(new_cat)
        db.commit()

        # 3. Preguntas Profesionales
        banco_preguntas = [
            # Categoria 1: Señales
            {
                "categoria_id": 1,
                "texto_pregunta": "¿Qué indica una señal de reglamentación de forma circular con el borde rojo y fondo blanco?",
                "explicacion": "Las señales circulares con borde rojo y fondo blanco son señales de prohibición o restricción.",
                "dificultad": DificultadEnum.facil,
                "respuestas": [
                    {"texto": "Una prohibición.", "correcta": True},
                    {"texto": "Una obligación.", "correcta": False},
                    {"texto": "Un peligro.", "correcta": False}
                ]
            },
            {
                "categoria_id": 1,
                "texto_pregunta": "Ante una señal de STOP y una marca vial de CEDA EL PASO en la misma intersección, ¿cuál debe obedecer?",
                "explicacion": "En caso de contradicción entre señales de distinta clase, prevalece la señal más restrictiva o la que tenga prioridad según el orden jerárquico. Las señales verticales (STOP) prevalecen sobre las marcas viales.",
                "dificultad": DificultadEnum.medio,
                "respuestas": [
                    {"texto": "La marca vial de ceda el paso.", "correcta": False},
                    {"texto": "La señal vertical de STOP.", "correcta": True},
                    {"texto": "La más cercana al vehículo.", "correcta": False}
                ]
            },
            # Categoria 2: Normas
            {
                "categoria_id": 2,
                "texto_pregunta": "Como norma general, en una intersección sin señalizar, ¿qué vehículo tiene prioridad de paso?",
                "explicacion": "A falta de señalización, la norma general de prioridad de paso es la de la derecha.",
                "dificultad": DificultadEnum.facil,
                "respuestas": [
                    {"texto": "El que circula por la vía más ancha.", "correcta": False},
                    {"texto": "El que aparece por la derecha del conductor.", "correcta": True},
                    {"texto": "El que circula a mayor velocidad.", "correcta": False}
                ]
            },
            {
                "categoria_id": 2,
                "texto_pregunta": "¿Cuál es la velocidad máxima permitida para un turismo en una carretera convencional con un solo carril por sentido y sin arcén?",
                "explicacion": "La velocidad máxima genérica en carreteras convencionales para turismos y motocicletas es de 90 km/h.",
                "dificultad": DificultadEnum.medio,
                "respuestas": [
                    {"texto": "90 km/h.", "correcta": True},
                    {"texto": "100 km/h.", "correcta": False},
                    {"texto": "80 km/h.", "correcta": False}
                ]
            },
            # Categoria 3: Seguridad
            {
                "categoria_id": 3,
                "texto_pregunta": "¿Cómo afecta el consumo de alcohol a la capacidad de conducción?",
                "explicacion": "El alcohol aumenta el tiempo de reacción, reduce el campo visual (efecto túnel) y disminuye la capacidad de atención.",
                "dificultad": DificultadEnum.medio,
                "respuestas": [
                    {"texto": "Aumenta el tiempo de reacción.", "correcta": True},
                    {"texto": "Disminuye el tiempo de reacción.", "correcta": False},
                    {"texto": "Mejora la agudeza visual.", "correcta": False}
                ]
            },
            # Categoria 4: Mecánica
            {
                "categoria_id": 4,
                "texto_pregunta": "¿Cuál es la profundidad mínima legal del dibujo de los neumáticos de un turismo?",
                "explicacion": "La profundidad mínima legal es de 1,6 milímetros, aunque se recomienda cambiarlos cuando el dibujo es inferior a 3 mm.",
                "dificultad": DificultadEnum.medio,
                "respuestas": [
                    {"texto": "1,6 milímetros.", "correcta": True},
                    {"texto": "2,0 milímetros.", "correcta": False},
                    {"texto": "1,0 milímetros.", "correcta": False}
                ]
            }
        ]

        # Añadir más preguntas para completar un set decente
        # (Aquí podrías expandir con más preguntas reales)

        for p_data in banco_preguntas:
            # Evitar duplicados por texto de pregunta
            exists = db.query(models.Pregunta).filter(models.Pregunta.texto_pregunta == p_data["texto_pregunta"]).first()
            if not exists:
                pregunta = models.Pregunta(
                    texto_pregunta=p_data["texto_pregunta"],
                    explicacion=p_data["explicacion"],
                    categoria_id=p_data["categoria_id"],
                    dificultad=p_data["dificultad"]
                )
                db.add(pregunta)
                db.flush() # Para obtener el ID

                for i, r_data in enumerate(p_data["respuestas"], 1):
                    respuesta = models.Respuesta(
                        pregunta_id=pregunta.id,
                        texto_respuesta=r_data["texto"],
                        es_correcta=r_data["correcta"],
                        orden_respuesta=i
                    )
                    db.add(respuesta)

        db.commit()
        print(f"✅ Seeding completado con éxito. Se han añadido {len(banco_preguntas)} preguntas de alta calidad.")

    except Exception as e:
        db.rollback()
        print(f"❌ Error durante el seeding: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_professional_questions()
