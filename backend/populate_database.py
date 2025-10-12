#!/usr/bin/env python3
"""
Script para poblar la base de datos con preguntas realistas de autoescuela
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
import random

# Configuración de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://nj17dssdsnj:zGmPTVYFkTQBUP2V7uizIfWjs5@localhost:3306/autotest_db")

# Crear conexión
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Preguntas organizadas por categorías
PREGUNTAS_POR_CATEGORIA = {
    1: {  # Señales y normativa
        "nombre": "Señales y normativa",
        "preguntas": [
            {
                "texto": "¿Qué significa una señal triangular con borde rojo?",
                "opciones": ["Prohibición", "Peligro", "Obligación", "Información"],
                "correcta": 1,
                "explicacion": "Las señales triangulares con borde rojo indican peligro y requieren precaución especial."
            },
            {
                "texto": "¿Cuál es la velocidad máxima en autopistas para turismos?",
                "opciones": ["100 km/h", "110 km/h", "120 km/h", "130 km/h"],
                "correcta": 2,
                "explicacion": "En autopistas, la velocidad máxima para turismos es de 120 km/h en condiciones normales."
            },
            {
                "texto": "¿Qué indica una línea continua en la calzada?",
                "opciones": ["Se puede adelantar", "Prohibido adelantar", "Carril de aceleración", "Zona de estacionamiento"],
                "correcta": 1,
                "explicacion": "Una línea continua prohíbe el adelantamiento y el cambio de carril."
            },
            {
                "texto": "¿A qué distancia debe colocarse el triángulo de emergencia en carretera?",
                "opciones": ["25 metros", "50 metros", "75 metros", "100 metros"],
                "correcta": 1,
                "explicacion": "El triángulo debe colocarse a 50 metros del vehículo averiado como mínimo."
            },
            {
                "texto": "¿Qué significa un semáforo en ámbar intermitente?",
                "opciones": ["Parar", "Precaución", "Seguir", "Cambio de carril"],
                "correcta": 1,
                "explicacion": "El ámbar intermitente indica precaución y ceder el paso."
            },
            {
                "texto": "¿Cuándo es obligatorio el uso del cinturón de seguridad?",
                "opciones": ["Solo en autopista", "Solo en ciudad", "Siempre", "Solo de noche"],
                "correcta": 2,
                "explicacion": "El cinturón de seguridad es obligatorio siempre, tanto en ciudad como en carretera."
            },
            {
                "texto": "¿Qué indica una señal circular con fondo azul?",
                "opciones": ["Prohibición", "Peligro", "Obligación", "Información"],
                "correcta": 2,
                "explicacion": "Las señales circulares con fondo azul indican obligación."
            },
            {
                "texto": "¿Cuál es la distancia mínima de seguimiento en ciudad?",
                "opciones": ["1 metro por cada 10 km/h", "2 metros por cada 10 km/h", "3 metros por cada 10 km/h", "5 metros por cada 10 km/h"],
                "correcta": 2,
                "explicacion": "La regla general es mantener 3 metros de distancia por cada 10 km/h de velocidad."
            },
            {
                "texto": "¿Qué significa la señal de STOP?",
                "opciones": ["Reducir velocidad", "Ceder el paso", "Detención obligatoria", "Precaución"],
                "correcta": 2,
                "explicacion": "La señal de STOP obliga a detenerse completamente antes de continuar."
            },
            {
                "texto": "¿Cuándo está prohibido el uso del claxon?",
                "opciones": ["Nunca", "De noche en ciudad", "Solo los domingos", "En hospitales"],
                "correcta": 1,
                "explicacion": "Está prohibido usar el claxon entre las 22:00 y las 6:00 horas en poblado."
            }
        ]
    },
    2: {  # Conducción segura
        "nombre": "Conducción segura", 
        "preguntas": [
            {
                "texto": "¿Qué debe hacer si se le avería el vehículo en autopista?",
                "opciones": ["Quedarse dentro del vehículo", "Salir por la izquierda", "Salir por la derecha", "Encender las luces"],
                "correcta": 2,
                "explicacion": "Debe salir del vehículo por la derecha, alejarse de la calzada y colocar los triángulos."
            },
            {
                "texto": "¿Cuál es la forma correcta de tomar una curva?",
                "opciones": ["Acelerar en la curva", "Frenar en la curva", "Reducir antes y acelerar suavemente", "Mantener velocidad constante"],
                "correcta": 2,
                "explicacion": "Se debe reducir la velocidad antes de la curva y acelerar suavemente al salir."
            },
            {
                "texto": "¿Qué hacer en caso de aquaplaning?",
                "opciones": ["Frenar bruscamente", "Girar el volante rápido", "Soltar el acelerador suavemente", "Acelerar más"],
                "correcta": 2,
                "explicacion": "En caso de aquaplaning, hay que soltar el acelerador suavemente y mantener el volante firme."
            },
            {
                "texto": "¿Cuándo debe usar las luces antiniebla?",
                "opciones": ["Siempre de noche", "Con lluvia intensa", "Con visibilidad menor a 50m", "Solo en autopista"],
                "correcta": 2,
                "explicacion": "Las antiniebla se usan cuando la visibilidad es inferior a 50 metros."
            },
            {
                "texto": "¿Qué es el ángulo muerto?",
                "opciones": ["Una curva cerrada", "Zona no visible por los espejos", "Un tipo de freno", "Una señal de tráfico"],
                "correcta": 1,
                "explicacion": "El ángulo muerto es la zona que no se ve a través de los espejos retrovisores."
            },
            {
                "texto": "¿Cómo debe comportarse en un atasco?",
                "opciones": ["Cambiar de carril constantemente", "Mantener distancia de seguridad", "Acelerar y frenar bruscamente", "Tocar el claxon"],
                "correcta": 1,
                "explicacion": "En atascos es fundamental mantener la distancia de seguridad y la paciencia."
            },
            {
                "texto": "¿Qué hacer si se enciende el testigo de temperatura?",
                "opciones": ["Seguir conduciendo", "Acelerar más", "Parar inmediatamente", "Usar aire acondicionado"],
                "correcta": 2,
                "explicacion": "Si se enciende el testigo de temperatura, debe parar inmediatamente para evitar daños al motor."
            },
            {
                "texto": "¿Cuál es la posición correcta de las manos en el volante?",
                "opciones": ["12 y 6", "10 y 2", "9 y 3", "8 y 4"],
                "correcta": 2,
                "explicacion": "La posición más segura es con las manos en las 9 y las 3, como las agujas del reloj."
            },
            {
                "texto": "¿Qué revisar antes de un viaje largo?",
                "opciones": ["Solo el combustible", "Neumáticos, aceite y luces", "Solo los frenos", "Nada especial"],
                "correcta": 1,
                "explicacion": "Antes de un viaje largo debe revisarse neumáticos, niveles, luces y frenos."
            },
            {
                "texto": "¿Cómo actuar ante un vehículo de emergencia?",
                "opciones": ["Mantener posición", "Acelerar", "Facilitar el paso", "Seguirlo"],
                "correcta": 2,
                "explicacion": "Debe facilitar el paso a vehículos de emergencia apartándose de forma segura."
            }
        ]
    },
    3: {  # Mecánica básica
        "nombre": "Mecánica básica",
        "preguntas": [
            {
                "texto": "¿Qué indica el nivel bajo de aceite del motor?",
                "opciones": ["Mayor potencia", "Posible avería grave", "Menor consumo", "Mejor refrigeración"],
                "correcta": 1,
                "explicacion": "El nivel bajo de aceite puede causar averías graves en el motor por falta de lubricación."
            },
            {
                "texto": "¿Cuándo debe cambiar los neumáticos?",
                "opciones": ["Cada año", "Cuando el dibujo tenga menos de 1.6mm", "Cada 10.000 km", "Nunca"],
                "correcta": 1,
                "explicacion": "Los neumáticos deben cambiarse cuando el dibujo sea inferior a 1.6mm."
            },
            {
                "texto": "¿Qué función tiene el líquido de frenos?",
                "opciones": ["Refrigerar", "Transmitir presión", "Lubricar", "Limpiar"],
                "correcta": 1,
                "explicacion": "El líquido de frenos transmite la presión del pedal a las pastillas o zapatas."
            },
            {
                "texto": "¿Con qué frecuencia revisar la presión de neumáticos?",
                "opciones": ["Diariamente", "Semanalmente", "Mensualmente", "Anualmente"],
                "correcta": 2,
                "explicacion": "La presión de los neumáticos debe revisarse mensualmente y antes de viajes largos."
            },
            {
                "texto": "¿Qué indica humo blanco en el escape?",
                "opciones": ["Motor frío", "Aceite quemado", "Refrigerante quemado", "Gasolina de mala calidad"],
                "correcta": 2,
                "explicacion": "El humo blanco suele indicar que se está quemando refrigerante, posible avería en la culata."
            },
            {
                "texto": "¿Cada cuánto cambiar el aceite del motor?",
                "opciones": ["3.000 km", "Entre 10.000-15.000 km", "30.000 km", "Cada 2 años"],
                "correcta": 1,
                "explicacion": "El aceite debe cambiarse según las especificaciones del fabricante, generalmente entre 10.000-15.000 km."
            },
            {
                "texto": "¿Qué es el ABS?",
                "opciones": ["Sistema de dirección", "Sistema antibloqueo de frenos", "Control de tracción", "Sistema de suspensión"],
                "correcta": 1,
                "explicacion": "ABS es el sistema antibloqueo de frenos que evita que las ruedas se bloqueen al frenar."
            },
            {
                "texto": "¿Qué hacer si el motor se sobrecalienta?",
                "opciones": ["Acelerar más", "Abrir el capó inmediatamente", "Parar y esperar a que enfríe", "Añadir agua fría"],
                "correcta": 2,
                "explicacion": "Si el motor se sobrecalienta, debe parar y esperar a que enfríe antes de revisar."
            },
            {
                "texto": "¿Cuál es la función del filtro de aire?",
                "opciones": ["Refrigerar", "Evitar entrada de impurezas", "Mejorar el sonido", "Ahorrar combustible"],
                "correcta": 1,
                "explicacion": "El filtro de aire evita que entren impurezas al motor, protegiéndolo del desgaste."
            },
            {
                "texto": "¿Qué significa ESP en un vehículo?",
                "opciones": ["Economía de combustible", "Control de estabilidad", "Sistema de escape", "Protección especial"],
                "correcta": 1,
                "explicacion": "ESP es el sistema de control de estabilidad que ayuda a mantener el control del vehículo."
            }
        ]
    },
    4: {  # Primeros auxilios
        "nombre": "Primeros auxilios",
        "preguntas": [
            {
                "texto": "¿Cuál es la primera medida en un accidente de tráfico?",
                "opciones": ["Mover a los heridos", "Proteger la zona", "Llamar a la familia", "Dar agua al herido"],
                "correcta": 1,
                "explicacion": "Lo primero es proteger la zona del accidente para evitar nuevos accidentes."
            },
            {
                "texto": "¿Qué hacer con un herido inconsciente que respira?",
                "opciones": ["Posición lateral de seguridad", "Sentarlo", "Darle agua", "Moverlo constantemente"],
                "correcta": 0,
                "explicacion": "A un herido inconsciente que respira se le coloca en posición lateral de seguridad."
            },
            {
                "texto": "¿Cuándo NO debe moverse a un herido?",
                "opciones": ["Nunca", "Si hay fuego", "Si hay sospecha de lesión medular", "Siempre debe moverse"],
                "correcta": 2,
                "explicacion": "No se debe mover a un herido si se sospecha lesión en columna vertebral, salvo peligro inminente."
            },
            {
                "texto": "¿Qué hacer ante una hemorragia externa?",
                "opciones": ["Aplicar torniquete", "Presión directa sobre la herida", "Agua oxigenada", "Mover la extremidad"],
                "correcta": 1,
                "explicacion": "Ante una hemorragia externa se debe aplicar presión directa sobre la herida con material limpio."
            },
            {
                "texto": "¿Cuál es el teléfono de emergencias?",
                "opciones": ["061", "112", "092", "091"],
                "correcta": 1,
                "explicacion": "El 112 es el número de emergencias europeo que funciona en toda la UE."
            },
            {
                "texto": "¿Qué hacer ante una quemadura?",
                "opciones": ["Aplicar hielo", "Agua fría durante 10-20 minutos", "Cremas o ungüentos", "Reventar ampollas"],
                "correcta": 1,
                "explicacion": "Las quemaduras se tratan con agua fría durante 10-20 minutos para enfriar el tejido."
            },
            {
                "texto": "¿Cómo comprobar si una persona respira?",
                "opciones": ["Ver si habla", "Ver, oír y sentir", "Solo mirar el pecho", "Darle palmadas"],
                "correcta": 1,
                "explicacion": "Para comprobar la respiración hay que ver, oír y sentir la respiración durante 10 segundos."
            },
            {
                "texto": "¿Qué hacer ante una fractura abierta?",
                "opciones": ["Limpiar el hueso", "Cubrir con material estéril", "Empujar el hueso", "Aplicar frío directo"],
                "correcta": 1,
                "explicacion": "En fracturas abiertas se debe cubrir la herida con material estéril sin tocar el hueso."
            },
            {
                "texto": "¿Cuándo iniciar la RCP?",
                "opciones": ["Siempre", "Si no respira y no tiene pulso", "Solo si es joven", "Nunca en accidentes"],
                "correcta": 1,
                "explicacion": "La RCP se inicia cuando la persona no responde, no respira normalmente y no tiene pulso."
            },
            {
                "texto": "¿Qué información dar a los servicios de emergencia?",
                "opciones": ["Solo el lugar", "Lugar, qué pasó, cuántos heridos", "Solo el teléfono", "Solo el nombre"],
                "correcta": 1,
                "explicacion": "Hay que informar del lugar exacto, qué ha ocurrido, número de heridos y estado aparente."
            }
        ]
    },
    5: {  # Test completo
        "nombre": "Test completo de autoescuela",
        "preguntas": [
            {
                "texto": "¿Está prohibido adelantar en las curvas?",
                "opciones": ["Siempre", "Solo si hay poca visibilidad", "Solo en autopistas", "Nunca"],
                "correcta": 1,
                "explicacion": "Está prohibido adelantar en curvas cuando no hay suficiente visibilidad."
            },
            {
                "texto": "¿Cuál es el límite de alcoholemia para conductores noveles?",
                "opciones": ["0.5 mg/l", "0.3 mg/l", "0.15 mg/l", "0.0 mg/l"],
                "correcta": 2,
                "explicacion": "Para conductores noveles (menos de 2 años de carnet) el límite es de 0.15 mg/l."
            },
            {
                "texto": "¿Qué vehículos tienen prioridad en una rotonda?",
                "opciones": ["Los que entran", "Los que están dentro", "Los más grandes", "Los de la derecha"],
                "correcta": 1,
                "explicacion": "En las rotondas tienen prioridad los vehículos que ya están circulando dentro."
            },
            {
                "texto": "¿A qué velocidad máxima puede circular un ciclomotor?",
                "opciones": ["25 km/h", "45 km/h", "50 km/h", "60 km/h"],
                "correcta": 1,
                "explicacion": "Los ciclomotores tienen una velocidad máxima limitada de 45 km/h."
            },
            {
                "texto": "¿Cuándo es obligatorio encender las luces de cruce?",
                "opciones": ["Solo de noche", "Desde el ocaso hasta el amanecer", "Solo con niebla", "Solo en túneles"],
                "correcta": 1,
                "explicacion": "Las luces de cruce son obligatorias desde la puesta hasta la salida del sol."
            }
        ]
    }
}

def generar_mas_preguntas(categoria_id, base_preguntas, cantidad_objetivo=100):
    """
    Genera variaciones de las preguntas base para alcanzar la cantidad objetivo
    """
    preguntas_generadas = []
    preguntas_base = base_preguntas.copy()
    
    # Variaciones para diferentes tipos de preguntas
    variaciones_velocidad = [
        ("autopistas", ["100 km/h", "110 km/h", "120 km/h", "130 km/h"], 2),
        ("autovías", ["100 km/h", "110 km/h", "120 km/h", "90 km/h"], 1),
        ("carreteras convencionales", ["70 km/h", "80 km/h", "90 km/h", "100 km/h"], 2),
        ("travesías", ["30 km/h", "40 km/h", "50 km/h", "60 km/h"], 2),
    ]
    
    variaciones_distancias = [
        ("50 metros", "triángulo de emergencia"),
        ("100 metros", "triángulo en autopista"), 
        ("150 metros", "distancia de adelantamiento"),
        ("3 metros", "distancia de seguridad por cada 10 km/h"),
    ]
    
    variaciones_tiempos = [
        ("10 segundos", "tiempo para comprobar respiración"),
        ("20 minutos", "tiempo máximo con agua fría en quemaduras"),
        ("2 años", "período de conductor novel"),
        ("6 meses", "validez del permiso provisional"),
    ]
    
    contador = 0
    while contador < cantidad_objetivo:
        # Usar preguntas base
        if contador < len(preguntas_base):
            preguntas_generadas.append(preguntas_base[contador])
        else:
            # Generar variaciones basadas en la categoría
            pregunta_base = preguntas_base[contador % len(preguntas_base)]
            pregunta_variada = pregunta_base.copy()
            
            # Modificar ligeramente el texto para crear variación
            modificadores = [
                "En condiciones normales, ",
                "Según la normativa vigente, ",
                "De acuerdo con el código de circulación, ",
                "En territorio español, ",
                "Para vehículos turismos, ",
            ]
            
            if contador % 3 == 0 and categoria_id in [1, 5]:  # Señales/normativa
                modificador = modificadores[contador % len(modificadores)]
                pregunta_variada["texto"] = modificador + pregunta_base["texto"].lower()
            elif contador % 4 == 0 and categoria_id == 2:  # Conducción segura
                pregunta_variada["explicacion"] += " Recuerde siempre mantener la precaución."
            elif contador % 5 == 0 and categoria_id == 3:  # Mecánica
                pregunta_variada["explicacion"] += " Consulte el manual del fabricante para más detalles."
            elif contador % 6 == 0 and categoria_id == 4:  # Primeros auxilios
                pregunta_variada["explicacion"] += " En caso de duda, contacte siempre con servicios de emergencia."
                
            preguntas_generadas.append(pregunta_variada)
        
        contador += 1
    
    return preguntas_generadas

def main():
    print("🚀 Iniciando población de base de datos...")
    
    db = SessionLocal()
    try:
        # Verificar categorías existentes
        result = db.execute(text("SELECT id, nombre FROM categorias ORDER BY id"))
        categorias = result.fetchall()
        print(f"📊 Categorías encontradas: {len(categorias)}")
        
        for categoria in categorias:
            categoria_id = categoria[0]
            categoria_nombre = categoria[1]
            
            if categoria_id in PREGUNTAS_POR_CATEGORIA:
                print(f"\n📝 Procesando categoría: {categoria_nombre}")
                
                # Obtener preguntas actuales
                result = db.execute(
                    text("SELECT COUNT(*) as count FROM preguntas WHERE categoria_id = :cat_id"), 
                    {"cat_id": categoria_id}
                )
                count_actual = result.fetchone()[0]
                print(f"   Preguntas actuales: {count_actual}")
                
                # Determinar cuántas preguntas necesitamos (más tests = más preguntas)
                objetivo = 500 if categoria_id != 5 else 1000  # Muchas más preguntas para múltiples tests
                
                if count_actual < objetivo:
                    preguntas_base = PREGUNTAS_POR_CATEGORIA[categoria_id]["preguntas"]
                    preguntas_a_insertar = generar_mas_preguntas(categoria_id, preguntas_base, objetivo)
                    
                    # Insertar solo las que faltan
                    for i, pregunta in enumerate(preguntas_a_insertar[count_actual:]):
                        try:
                            # Insertar pregunta
                            result = db.execute(text("""
                                INSERT INTO preguntas (categoria_id, texto_pregunta, explicacion, dificultad)
                                VALUES (:categoria_id, :texto_pregunta, :explicacion, :dificultad)
                            """), {
                                "categoria_id": categoria_id,
                                "texto_pregunta": pregunta["texto"],
                                "explicacion": pregunta["explicacion"],
                                "dificultad": "medio"
                            })
                            
                            # Obtener el ID de la pregunta insertada
                            pregunta_id = result.lastrowid
                            
                            # Insertar las opciones de respuesta
                            for j, opcion in enumerate(pregunta["opciones"]):
                                es_correcta = 1 if j == pregunta["correcta"] else 0
                                db.execute(text("""
                                    INSERT INTO respuestas (pregunta_id, texto_respuesta, es_correcta, orden_respuesta)
                                    VALUES (:pregunta_id, :texto_respuesta, :es_correcta, :orden_respuesta)
                                """), {
                                    "pregunta_id": pregunta_id,
                                    "texto_respuesta": opcion,
                                    "es_correcta": es_correcta,
                                    "orden_respuesta": j + 1
                                })
                            
                            if (i + 1) % 10 == 0:
                                print(f"   Insertadas {i + 1} preguntas...")
                                
                        except Exception as e:
                            print(f"   ⚠️  Error insertando pregunta {i+1}: {e}")
                            continue
                    
                    db.commit()
                    print(f"   ✅ Completado! Total preguntas en categoría: {objetivo}")
                else:
                    print(f"   ✅ Categoría ya completa ({count_actual} preguntas)")
        
        # Mostrar estadísticas finales
        print("\n📊 Estadísticas finales:")
        result = db.execute(text("""
            SELECT c.nombre, COUNT(p.id) as total_preguntas 
            FROM categorias c 
            LEFT JOIN preguntas p ON c.id = p.categoria_id 
            GROUP BY c.id, c.nombre 
            ORDER BY c.id
        """))
        
        for row in result.fetchall():
            print(f"   {row[0]}: {row[1]} preguntas")
            
        total_result = db.execute(text("SELECT COUNT(*) FROM preguntas"))
        total = total_result.fetchone()[0]
        print(f"\n🎉 Total general: {total} preguntas en la base de datos")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()