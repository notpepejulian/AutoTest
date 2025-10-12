#!/usr/bin/env python3
"""
Script para insertar 30 preguntas realistas de autoescuela para "Test Categoria"
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import random
from urllib.parse import quote_plus

# Configurar la URL de conexión usando root
password = "Vp@ei#A2N3shG!hGe"
encoded_password = quote_plus(password)
DATABASE_URL = os.getenv("DATABASE_URL", f"mysql+pymysql://nj17dssdsnj:zGmPTVYFkTQBUP2V7uizIfWjs5@database:3306/autotest_db")

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Preguntas para "Test Categoria" - Temática de autoescuela
preguntas_autoescuela = [
    {
        "texto_pregunta": "¿Cuál es la velocidad máxima permitida para turismos en autopistas?",
        "explicacion": "En España, la velocidad máxima genérica para turismos en autopistas es de 120 km/h, salvo señalización que indique lo contrario.",
        "dificultad": "facil",
        "respuestas": [
            {"texto_respuesta": "100 km/h", "es_correcta": False, "orden_respuesta": 1},
            {"texto_respuesta": "120 km/h", "es_correcta": True, "orden_respuesta": 2},
            {"texto_respuesta": "110 km/h", "es_correcta": False, "orden_respuesta": 3},
            {"texto_respuesta": "130 km/h", "es_correcta": False, "orden_respuesta": 4}
        ]
    },
    {
        "texto_pregunta": "¿Qué significa una señal triangular con borde rojo?",
        "explicacion": "Las señales triangulares con borde rojo son señales de peligro que advierten sobre un riesgo en la vía.",
        "dificultad": "medio",
        "respuestas": [
            {"texto_respuesta": "Señal de prohibición", "es_correcta": False, "orden_respuesta": 1},
            {"texto_respuesta": "Señal de peligro", "es_correcta": True, "orden_respuesta": 2},
            {"texto_respuesta": "Señal de información", "es_correcta": False, "orden_respuesta": 3},
            {"texto_respuesta": "Señal de obligación", "es_correcta": False, "orden_respuesta": 4}
        ]
    },
    {
        "texto_pregunta": "¿Es obligatorio el uso del cinturón de seguridad en vías urbanas?",
        "explicacion": "El cinturón de seguridad es obligatorio para todos los ocupantes del vehículo, tanto en vías urbanas como interurbanas.",
        "dificultad": "facil",
        "respuestas": [
            {"texto_respuesta": "Solo en autopistas", "es_correcta": False, "orden_respuesta": 1},
            {"texto_respuesta": "Sí, siempre es obligatorio", "es_correcta": True, "orden_respuesta": 2},
            {"texto_respuesta": "Solo para el conductor", "es_correcta": False, "orden_respuesta": 3},
            {"texto_respuesta": "No es obligatorio en ciudad", "es_correcta": False, "orden_respuesta": 4}
        ]
    },
    {
        "texto_pregunta": "¿Cuál es la tasa máxima de alcoholemia permitida para conductores profesionales?",
        "explicacion": "Los conductores profesionales tienen un límite más restrictivo de 0,15 mg/l en aire espirado o 0,3 g/l en sangre.",
        "dificultad": "dificil",
        "respuestas": [
            {"texto_respuesta": "0,25 mg/l en aire espirado", "es_correcta": False, "orden_respuesta": 1},
            {"texto_respuesta": "0,15 mg/l en aire espirado", "es_correcta": True, "orden_respuesta": 2},
            {"texto_respuesta": "0,50 mg/l en aire espirado", "es_correcta": False, "orden_respuesta": 3},
            {"texto_respuesta": "0,30 mg/l en aire espirado", "es_correcta": False, "orden_respuesta": 4}
        ]
    },
    {
        "texto_pregunta": "¿Qué indica una luz amarilla intermitente en un semáforo?",
        "explicacion": "La luz amarilla intermitente indica precaución y obliga a extremar las precauciones, respetando las normas de prioridad.",
        "dificultad": "medio",
        "respuestas": [
            {"texto_respuesta": "Detenerse obligatoriamente", "es_correcta": False, "orden_respuesta": 1},
            {"texto_respuesta": "Extremar precaución", "es_correcta": True, "orden_respuesta": 2},
            {"texto_respuesta": "Acelerar para pasar", "es_correcta": False, "orden_respuesta": 3},
            {"texto_respuesta": "Ceder el paso siempre", "es_correcta": False, "orden_respuesta": 4}
        ]
    },
    {
        "texto_pregunta": "¿Cada cuánto tiempo se debe revisar la presión de los neumáticos?",
        "explicacion": "Se recomienda revisar la presión de los neumáticos al menos una vez al mes y siempre antes de viajes largos.",
        "dificultad": "medio",
        "respuestas": [
            {"texto_respuesta": "Cada semana", "es_correcta": False, "orden_respuesta": 1},
            {"texto_respuesta": "Cada mes", "es_correcta": True, "orden_respuesta": 2},
            {"texto_respuesta": "Cada 6 meses", "es_correcta": False, "orden_respuesta": 3},
            {"texto_respuesta": "Solo cuando se noten pinchados", "es_correcta": False, "orden_respuesta": 4}
        ]
    },
    {
        "texto_pregunta": "¿Qué forma tienen las señales de prohibición?",
        "explicacion": "Las señales de prohibición son circulares con fondo blanco, pictograma negro y borde rojo.",
        "dificultad": "facil",
        "respuestas": [
            {"texto_respuesta": "Triangular", "es_correcta": False, "orden_respuesta": 1},
            {"texto_respuesta": "Circular", "es_correcta": True, "orden_respuesta": 2},
            {"texto_respuesta": "Cuadrada", "es_correcta": False, "orden_respuesta": 3},
            {"texto_respuesta": "Octogonal", "es_correcta": False, "orden_respuesta": 4}
        ]
    },
    {
        "texto_pregunta": "¿A qué distancia mínima debe colocar los triángulos de emergencia?",
        "explicacion": "Los triángulos deben colocarse a 50 metros del vehículo en vías urbanas y a 100 metros en carreteras.",
        "dificultad": "medio",
        "respuestas": [
            {"texto_respuesta": "25 metros en ciudad, 50 en carretera", "es_correcta": False, "orden_respuesta": 1},
            {"texto_respuesta": "50 metros en ciudad, 100 en carretera", "es_correcta": True, "orden_respuesta": 2},
            {"texto_respuesta": "100 metros siempre", "es_correcta": False, "orden_respuesta": 3},
            {"texto_respuesta": "30 metros en ambos casos", "es_correcta": False, "orden_respuesta": 4}
        ]
    },
    {
        "texto_pregunta": "¿Cuál es la velocidad máxima en vías urbanas?",
        "explicacion": "En vías urbanas, la velocidad máxima genérica es de 50 km/h, salvo en calles de un solo carril que es 30 km/h.",
        "dificultad": "facil",
        "respuestas": [
            {"texto_respuesta": "40 km/h", "es_correcta": False, "orden_respuesta": 1},
            {"texto_respuesta": "50 km/h", "es_correcta": True, "orden_respuesta": 2},
            {"texto_respuesta": "60 km/h", "es_correcta": False, "orden_respuesta": 3},
            {"texto_respuesta": "30 km/h", "es_correcta": False, "orden_respuesta": 4}
        ]
    },
    {
        "texto_pregunta": "¿Qué debe hacer ante un vehículo de emergencia con sirenas?",
        "explicacion": "Debe facilitar el paso inmediatamente, apartándose de forma segura y deteniéndose si es necesario.",
        "dificultad": "facil",
        "respuestas": [
            {"texto_respuesta": "Mantener la velocidad", "es_correcta": False, "orden_respuesta": 1},
            {"texto_respuesta": "Facilitar el paso inmediatamente", "es_correcta": True, "orden_respuesta": 2},
            {"texto_respuesta": "Acelerar para alejarse", "es_correcta": False, "orden_respuesta": 3},
            {"texto_respuesta": "Seguir al vehículo de emergencia", "es_correcta": False, "orden_respuesta": 4}
        ]
    },
    {
        "texto_pregunta": "¿Qué profundidad mínima debe tener el dibujo de los neumáticos?",
        "explicacion": "El dibujo de los neumáticos debe tener una profundidad mínima de 1,6 mm en toda la superficie de rodadura.",
        "dificultad": "dificil",
        "respuestas": [
            {"texto_respuesta": "1,0 mm", "es_correcta": False, "orden_respuesta": 1},
            {"texto_respuesta": "1,6 mm", "es_correcta": True, "orden_respuesta": 2},
            {"texto_respuesta": "2,0 mm", "es_correcta": False, "orden_respuesta": 3},
            {"texto_respuesta": "1,2 mm", "es_correcta": False, "orden_respuesta": 4}
        ]
    },
    {
        "texto_pregunta": "¿Está permitido usar el teléfono móvil mientras se conduce?",
        "explicacion": "Está prohibido usar el teléfono móvil mientras se conduce, salvo que se use con sistema de manos libres.",
        "dificultad": "facil",
        "respuestas": [
            {"texto_respuesta": "Sí, siempre", "es_correcta": False, "orden_respuesta": 1},
            {"texto_respuesta": "No, está prohibido salvo manos libres", "es_correcta": True, "orden_respuesta": 2},
            {"texto_respuesta": "Solo en atascos", "es_correcta": False, "orden_respuesta": 3},
            {"texto_respuesta": "Solo para llamadas urgentes", "es_correcta": False, "orden_respuesta": 4}
        ]
    },
    {
        "texto_pregunta": "¿Qué significa una señal octogonal roja?",
        "explicacion": "La señal octogonal roja es la señal de STOP, que obliga a la detención completa del vehículo.",
        "dificultad": "facil",
        "respuestas": [
            {"texto_respuesta": "Ceda el paso", "es_correcta": False, "orden_respuesta": 1},
            {"texto_respuesta": "Detención obligatoria (STOP)", "es_correcta": True, "orden_respuesta": 2},
            {"texto_respuesta": "Prohibido el paso", "es_correcta": False, "orden_respuesta": 3},
            {"texto_respuesta": "Reducir velocidad", "es_correcta": False, "orden_respuesta": 4}
        ]
    },
    {
        "texto_pregunta": "¿Cuándo debe encender las luces de posición?",
        "explicacion": "Las luces de posición deben encenderse desde el ocaso hasta el amanecer y cuando las condiciones lo requieran.",
        "dificultad": "medio",
        "respuestas": [
            {"texto_respuesta": "Solo de noche", "es_correcta": False, "orden_respuesta": 1},
            {"texto_respuesta": "Desde el ocaso hasta el amanecer", "es_correcta": True, "orden_respuesta": 2},
            {"texto_respuesta": "Solo con lluvia", "es_correcta": False, "orden_respuesta": 3},
            {"texto_respuesta": "Solo en autopista", "es_correcta": False, "orden_respuesta": 4}
        ]
    },
    {
        "texto_pregunta": "¿Qué debe comprobar antes de iniciar la marcha?",
        "explicacion": "Antes de iniciar la marcha debe comprobar espejos, asiento, volante, frenos y que no haya obstáculos.",
        "dificultad": "medio",
        "respuestas": [
            {"texto_respuesta": "Solo los espejos", "es_correcta": False, "orden_respuesta": 1},
            {"texto_respuesta": "Espejos, asiento, frenos y alrededores", "es_correcta": True, "orden_respuesta": 2},
            {"texto_respuesta": "Solo el combustible", "es_correcta": False, "orden_respuesta": 3},
            {"texto_respuesta": "Solo la documentación", "es_correcta": False, "orden_respuesta": 4}
        ]
    },
    {
        "texto_pregunta": "¿Qué indica una línea continua en la calzada?",
        "explicacion": "Una línea continua indica que está prohibido el adelantamiento y el cambio de carril.",
        "dificultad": "medio",
        "respuestas": [
            {"texto_respuesta": "Se puede adelantar con precaución", "es_correcta": False, "orden_respuesta": 1},
            {"texto_respuesta": "Prohibido adelantar y cambiar de carril", "es_correcta": True, "orden_respuesta": 2},
            {"texto_respuesta": "Límite de velocidad", "es_correcta": False, "orden_respuesta": 3},
            {"texto_respuesta": "Zona de aparcamiento", "es_correcta": False, "orden_respuesta": 4}
        ]
    },
    {
        "texto_pregunta": "¿Cuál es la edad mínima para obtener el permiso B?",
        "explicacion": "La edad mínima para obtener el permiso de conducir clase B (turismos) es de 18 años.",
        "dificultad": "facil",
        "respuestas": [
            {"texto_respuesta": "16 años", "es_correcta": False, "orden_respuesta": 1},
            {"texto_respuesta": "18 años", "es_correcta": True, "orden_respuesta": 2},
            {"texto_respuesta": "21 años", "es_correcta": False, "orden_respuesta": 3},
            {"texto_respuesta": "17 años", "es_correcta": False, "orden_respuesta": 4}
        ]
    },
    {
        "texto_pregunta": "¿Qué hacer en caso de reventón de un neumático?",
        "explicacion": "En caso de reventón, mantener el control del volante, no frenar bruscamente y dirigirse al arcén gradualmente.",
        "dificultad": "medio",
        "respuestas": [
            {"texto_respuesta": "Frenar inmediatamente", "es_correcta": False, "orden_respuesta": 1},
            {"texto_respuesta": "Mantener control y dirigirse al arcén", "es_correcta": True, "orden_respuesta": 2},
            {"texto_respuesta": "Acelerar para mantener estabilidad", "es_correcta": False, "orden_respuesta": 3},
            {"texto_respuesta": "Girar el volante bruscamente", "es_correcta": False, "orden_respuesta": 4}
        ]
    },
    {
        "texto_pregunta": "¿Cuántos puntos se pierden por conducir hablando por el móvil?",
        "explicacion": "Conducir utilizando el teléfono móvil supone la pérdida de 6 puntos del carnet de conducir.",
        "dificultad": "medio",
        "respuestas": [
            {"texto_respuesta": "3 puntos", "es_correcta": False, "orden_respuesta": 1},
            {"texto_respuesta": "6 puntos", "es_correcta": True, "orden_respuesta": 2},
            {"texto_respuesta": "4 puntos", "es_correcta": False, "orden_respuesta": 3},
            {"texto_respuesta": "2 puntos", "es_correcta": False, "orden_respuesta": 4}
        ]
    },
    {
        "texto_pregunta": "¿Qué documento NO es obligatorio llevar al conducir?",
        "explicacion": "No es obligatorio llevar el manual de instrucciones del vehículo. Sí son obligatorios: permiso, DNI, seguro y documentación del vehículo.",
        "dificultad": "medio",
        "respuestas": [
            {"texto_respuesta": "Permiso de conducir", "es_correcta": False, "orden_respuesta": 1},
            {"texto_respuesta": "Manual de instrucciones", "es_correcta": True, "orden_respuesta": 2},
            {"texto_respuesta": "Seguro del vehículo", "es_correcta": False, "orden_respuesta": 3},
            {"texto_respuesta": "DNI o pasaporte", "es_correcta": False, "orden_respuesta": 4}
        ]
    },
    {
        "texto_pregunta": "¿Qué color tienen las señales de obligación?",
        "explicacion": "Las señales de obligación tienen fondo azul con el pictograma en blanco.",
        "dificultad": "facil",
        "respuestas": [
            {"texto_respuesta": "Fondo rojo", "es_correcta": False, "orden_respuesta": 1},
            {"texto_respuesta": "Fondo azul", "es_correcta": True, "orden_respuesta": 2},
            {"texto_respuesta": "Fondo verde", "es_correcta": False, "orden_respuesta": 3},
            {"texto_respuesta": "Fondo amarillo", "es_correcta": False, "orden_respuesta": 4}
        ]
    },
    {
        "texto_pregunta": "¿Cuándo se debe usar el alumbrado antiniebla trasero?",
        "explicacion": "El alumbrado antiniebla trasero solo debe usarse cuando la visibilidad sea inferior a 50 metros por niebla o lluvia intensa.",
        "dificultad": "dificil",
        "respuestas": [
            {"texto_respuesta": "Siempre que llueva", "es_correcta": False, "orden_respuesta": 1},
            {"texto_respuesta": "Cuando la visibilidad sea inferior a 50m", "es_correcta": True, "orden_respuesta": 2},
            {"texto_respuesta": "Solo de noche", "es_correcta": False, "orden_respuesta": 3},
            {"texto_respuesta": "En cualquier condición adversa", "es_correcta": False, "orden_respuesta": 4}
        ]
    },
    {
        "texto_pregunta": "¿Qué maniobra está prohibida en un paso de peatones?",
        "explicacion": "En los pasos de peatones están prohibidas todas las maniobras: adelantar, parar, estacionar e incluso cambiar de sentido.",
        "dificultad": "medio",
        "respuestas": [
            {"texto_respuesta": "Solo adelantar", "es_correcta": False, "orden_respuesta": 1},
            {"texto_respuesta": "Adelantar, parar y estacionar", "es_correcta": True, "orden_respuesta": 2},
            {"texto_respuesta": "Solo estacionar", "es_correcta": False, "orden_respuesta": 3},
            {"texto_respuesta": "Solo parar", "es_correcta": False, "orden_respuesta": 4}
        ]
    },
    {
        "texto_pregunta": "¿Cuál es la distancia de seguridad recomendada?",
        "explicacion": "Se recomienda mantener una distancia equivalente a 3 segundos respecto al vehículo precedente.",
        "dificultad": "medio",
        "respuestas": [
            {"texto_respuesta": "1 segundo", "es_correcta": False, "orden_respuesta": 1},
            {"texto_respuesta": "3 segundos", "es_correcta": True, "orden_respuesta": 2},
            {"texto_respuesta": "5 segundos", "es_correcta": False, "orden_respuesta": 3},
            {"texto_respuesta": "2 metros por cada 10 km/h", "es_correcta": False, "orden_respuesta": 4}
        ]
    },
    {
        "texto_pregunta": "¿Qué indica una señal con flecha hacia la derecha sobre fondo azul?",
        "explicacion": "Una flecha sobre fondo azul indica dirección obligatoria hacia donde señala la flecha.",
        "dificultad": "facil",
        "respuestas": [
            {"texto_respuesta": "Prohibido girar a la derecha", "es_correcta": False, "orden_respuesta": 1},
            {"texto_respuesta": "Dirección obligatoria a la derecha", "es_correcta": True, "orden_respuesta": 2},
            {"texto_respuesta": "Recomendación de giro", "es_correcta": False, "orden_respuesta": 3},
            {"texto_respuesta": "Peligro curva a la derecha", "es_correcta": False, "orden_respuesta": 4}
        ]
    },
    {
        "texto_pregunta": "¿Cuándo debe revisar el nivel de aceite del motor?",
        "explicacion": "El nivel de aceite debe revisarse con el motor frío y el vehículo en una superficie plana y horizontal.",
        "dificultad": "medio",
        "respuestas": [
            {"texto_respuesta": "Con el motor caliente", "es_correcta": False, "orden_respuesta": 1},
            {"texto_respuesta": "Con el motor frío y en superficie plana", "es_correcta": True, "orden_respuesta": 2},
            {"texto_respuesta": "Solo en el taller", "es_correcta": False, "orden_respuesta": 3},
            {"texto_respuesta": "Con el motor en marcha", "es_correcta": False, "orden_respuesta": 4}
        ]
    },
    {
        "texto_pregunta": "¿Qué debe hacer si se enciende la luz roja del motor?",
        "explicacion": "Si se enciende la luz roja del motor debe detenerse inmediatamente de forma segura, ya que indica avería grave.",
        "dificultad": "medio",
        "respuestas": [
            {"texto_respuesta": "Continuar hasta el destino", "es_correcta": False, "orden_respuesta": 1},
            {"texto_respuesta": "Detenerse inmediatamente", "es_correcta": True, "orden_respuesta": 2},
            {"texto_respuesta": "Reducir la velocidad", "es_correcta": False, "orden_respuesta": 3},
            {"texto_respuesta": "Acelerar para llegar al taller", "es_correcta": False, "orden_respuesta": 4}
        ]
    },
    {
        "texto_pregunta": "¿Cuál es el protocolo PAS en caso de accidente?",
        "explicacion": "PAS significa: Proteger la zona, Avisar a los servicios de emergencia y Socorrer a los heridos.",
        "dificultad": "medio",
        "respuestas": [
            {"texto_respuesta": "Parar, Avisar, Salir", "es_correcta": False, "orden_respuesta": 1},
            {"texto_respuesta": "Proteger, Avisar, Socorrer", "es_correcta": True, "orden_respuesta": 2},
            {"texto_respuesta": "Pasar, Aparcar, Salvar", "es_correcta": False, "orden_respuesta": 3},
            {"texto_respuesta": "Precaución, Auxilio, Seguridad", "es_correcta": False, "orden_respuesta": 4}
        ]
    },
    {
        "texto_pregunta": "¿En qué casos puede circular por el arcén?",
        "explicacion": "Se puede circular por el arcén solo en caso de emergencia, avería o cuando lo autoricen agentes de tráfico.",
        "dificultad": "dificil",
        "respuestas": [
            {"texto_respuesta": "Cuando hay mucho tráfico", "es_correcta": False, "orden_respuesta": 1},
            {"texto_respuesta": "Solo en emergencia o avería", "es_correcta": True, "orden_respuesta": 2},
            {"texto_respuesta": "Para adelantar vehículos lentos", "es_correcta": False, "orden_respuesta": 3},
            {"texto_respuesta": "Siempre que esté libre", "es_correcta": False, "orden_respuesta": 4}
        ]
    },
    {
        "texto_pregunta": "¿Qué documentación debe llevar obligatoriamente un ciclomotor?",
        "explicacion": "Los ciclomotores deben llevar obligatoriamente el certificado de características, el seguro obligatorio y el permiso AM.",
        "dificultad": "dificil",
        "respuestas": [
            {"texto_respuesta": "Solo el permiso de conducir", "es_correcta": False, "orden_respuesta": 1},
            {"texto_respuesta": "Certificado, seguro y permiso AM", "es_correcta": True, "orden_respuesta": 2},
            {"texto_respuesta": "Solo el seguro", "es_correcta": False, "orden_respuesta": 3},
            {"texto_respuesta": "No necesita documentación", "es_correcta": False, "orden_respuesta": 4}
        ]
    },
    {
        "texto_pregunta": "¿Qué significa una señal vertical con un triángulo invertido de fondo blanco y borde rojo?",
        "explicacion": "Es la señal de ceda el paso, que obliga a ceder el paso a los vehículos que circulan por la vía a la que se aproxima.",
        "dificultad": "facil",
        "respuestas": [
            {"texto_respuesta": "Detención obligatoria", "es_correcta": False, "orden_respuesta": 1},
            {"texto_respuesta": "Ceda el paso", "es_correcta": True, "orden_respuesta": 2},
            {"texto_respuesta": "Intersección con prioridad", "es_correcta": False, "orden_respuesta": 3},
            {"texto_respuesta": "Peligro por obras", "es_correcta": False, "orden_respuesta": 4}
        ]
    },
    {
        "texto_pregunta": "¿Cuánto tiempo de validez tiene el permiso B para conductores noveles?",
        "explicacion": "El permiso de conducir B para conductores noveles tiene una validez inicial de 2 años, durante los cuales se aplican restricciones especiales.",
        "dificultad": "medio",
        "respuestas": [
            {"texto_respuesta": "1 año", "es_correcta": False, "orden_respuesta": 1},
            {"texto_respuesta": "2 años", "es_correcta": True, "orden_respuesta": 2},
            {"texto_respuesta": "3 años", "es_correcta": False, "orden_respuesta": 3},
            {"texto_respuesta": "5 años", "es_correcta": False, "orden_respuesta": 4}
        ]
    }
]

def insertar_preguntas_test_categoria():
    """Insertar las 30 preguntas para Test Categoria"""
    try:
        db = SessionLocal()
        
        # Buscar o crear la categoría "Test Categoria"
        result = db.execute(text("SELECT id FROM categorias WHERE nombre = 'Test Categoria'"))
        categoria_row = result.fetchone()
        
        if not categoria_row:
            # Crear la categoría
            db.execute(text("INSERT INTO categorias (nombre, descripcion) VALUES ('Test Categoria', 'Preguntas de examen teórico de autoescuela')"))
            db.commit()
            
            result = db.execute(text("SELECT id FROM categorias WHERE nombre = 'Test Categoria'"))
            categoria_row = result.fetchone()
        
        categoria_id = categoria_row[0]
        print(f"Categoría 'Test Categoria' encontrada/creada con ID: {categoria_id}")
        
        # Insertar las preguntas
        for i, pregunta_data in enumerate(preguntas_autoescuela, 1):
            # Insertar pregunta
            query_pregunta = """
                INSERT INTO preguntas (texto_pregunta, explicacion, categoria_id, dificultad, es_activa) 
                VALUES (:texto_pregunta, :explicacion, :categoria_id, :dificultad, :es_activa)
            """
            
            result = db.execute(text(query_pregunta), {
                'texto_pregunta': pregunta_data['texto_pregunta'],
                'explicacion': pregunta_data['explicacion'],
                'categoria_id': categoria_id,
                'dificultad': pregunta_data['dificultad'],
                'es_activa': True
            })
            
            # Obtener el ID de la pregunta insertada
            pregunta_id = result.lastrowid
            
            # Insertar respuestas
            for respuesta_data in pregunta_data['respuestas']:
                query_respuesta = """
                    INSERT INTO respuestas (pregunta_id, texto_respuesta, es_correcta, orden_respuesta) 
                    VALUES (:pregunta_id, :texto_respuesta, :es_correcta, :orden_respuesta)
                """
                
                db.execute(text(query_respuesta), {
                    'pregunta_id': pregunta_id,
                    'texto_respuesta': respuesta_data['texto_respuesta'],
                    'es_correcta': respuesta_data['es_correcta'],
                    'orden_respuesta': respuesta_data['orden_respuesta']
                })
            
            db.commit()
            print(f"✓ Pregunta {i}/30 insertada correctamente")
        
        print(f"\n🎉 Se han insertado exitosamente las 30 preguntas para 'Test Categoria'")
        
        # Verificar inserción
        result = db.execute(text("SELECT COUNT(*) FROM preguntas WHERE categoria_id = :categoria_id"), 
                          {'categoria_id': categoria_id})
        count = result.fetchone()[0]
        print(f"📊 Total de preguntas en 'Test Categoria': {count}")
        
    except Exception as e:
        print(f"❌ Error insertando preguntas: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Iniciando inserción de preguntas para 'Test Categoria'...")
    insertar_preguntas_test_categoria()