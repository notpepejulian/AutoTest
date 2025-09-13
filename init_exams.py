#!/usr/bin/env python3
import requests
import json
import time
from requests.exceptions import RequestException

API_BASE = "http://localhost:8000/api"
MAX_RETRIES = 3
RETRY_DELAY = 5

# Banco completo de preguntas de conducción
banco_preguntas = [
    # Señales de Tráfico
    {"texto_pregunta": "¿Qué significa una señal triangular con borde rojo?", "explicacion": "Las señales triangulares con borde rojo son señales de advertencia o peligro", "categoria_id": 1, "dificultad": "medio", "respuestas": [{"texto_respuesta": "Señal de prohibición", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "Señal de advertencia", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "Señal de información", "es_correcta": False, "orden_respuesta": 3}]},
    {"texto_pregunta": "¿Qué forma tienen las señales de prohibición?", "explicacion": "Las señales de prohibición son circulares con fondo blanco y borde rojo", "categoria_id": 1, "dificultad": "facil", "respuestas": [{"texto_respuesta": "Triangular", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "Circular", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "Cuadrada", "es_correcta": False, "orden_respuesta": 3}]},
    {"texto_pregunta": "¿Qué indica una señal octogonal?", "explicacion": "La única señal octogonal es la de STOP, que obliga a detención completa", "categoria_id": 1, "dificultad": "facil", "respuestas": [{"texto_respuesta": "Ceda el paso", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "Detención obligatoria", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "Velocidad máxima", "es_correcta": False, "orden_respuesta": 3}]},
    {"texto_pregunta": "¿De qué color es el fondo de las señales de obligación?", "explicacion": "Las señales de obligación tienen fondo azul con pictograma blanco", "categoria_id": 1, "dificultad": "medio", "respuestas": [{"texto_respuesta": "Rojo", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "Azul", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "Verde", "es_correcta": False, "orden_respuesta": 3}]},
    {"texto_pregunta": "¿Qué significa una señal con flecha curvada hacia la derecha?", "explicacion": "Indica la obligación de girar a la derecha", "categoria_id": 1, "dificultad": "facil", "respuestas": [{"texto_respuesta": "Prohibido girar a la derecha", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "Dirección obligatoria a la derecha", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "Precaución curva a la derecha", "es_correcta": False, "orden_respuesta": 3}]},
    
    # Normas de Circulación
    {"texto_pregunta": "¿Cuál es la velocidad máxima en autopista para turismos?", "explicacion": "La velocidad máxima genérica en autopistas para vehículos turismo es de 120 km/h", "categoria_id": 2, "dificultad": "medio", "respuestas": [{"texto_respuesta": "100 km/h", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "120 km/h", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "130 km/h", "es_correcta": False, "orden_respuesta": 3}]},
    {"texto_pregunta": "¿Cuál es la velocidad máxima en vías urbanas?", "explicacion": "En zonas urbanas la velocidad máxima genérica es de 50 km/h", "categoria_id": 2, "dificultad": "facil", "respuestas": [{"texto_respuesta": "30 km/h", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "50 km/h", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "60 km/h", "es_correcta": False, "orden_respuesta": 3}]},
    {"texto_pregunta": "¿A qué distancia mínima debe circular detrás de otro vehículo?", "explicacion": "Debe mantener una distancia de seguridad de al menos 3 segundos", "categoria_id": 2, "dificultad": "medio", "respuestas": [{"texto_respuesta": "1 metro por cada 10 km/h", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "La que permita detenerse sin colisionar", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "Siempre 50 metros", "es_correcta": False, "orden_respuesta": 3}]},
    {"texto_pregunta": "¿Está permitido usar el teléfono móvil mientras se conduce?", "explicacion": "Está prohibido usar el teléfono móvil mientras se conduce, salvo con sistema de manos libres", "categoria_id": 2, "dificultad": "facil", "respuestas": [{"texto_respuesta": "Sí, siempre", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "No, está prohibido", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "Solo en atascos", "es_correcta": False, "orden_respuesta": 3}]},
    {"texto_pregunta": "¿Es obligatorio el uso del cinturón de seguridad?", "explicacion": "El cinturón de seguridad es obligatorio para todos los ocupantes del vehículo", "categoria_id": 2, "dificultad": "facil", "respuestas": [{"texto_respuesta": "Solo para el conductor", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "Para todos los ocupantes", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "Solo en autopistas", "es_correcta": False, "orden_respuesta": 3}]},
    
    # Seguridad Vial
    {"texto_pregunta": "¿Qué debe hacer si encuentra un accidente de tránsito?", "explicacion": "Debe proteger, avisar y socorrer siguiendo el protocolo PAS", "categoria_id": 3, "dificultad": "medio", "respuestas": [{"texto_respuesta": "Seguir circulando", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "Proteger, avisar y socorrer", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "Solo llamar a emergencias", "es_correcta": False, "orden_respuesta": 3}]},
    {"texto_pregunta": "¿Cuándo debe usar las luces de emergencia?", "explicacion": "Las luces de emergencia se usan para advertir de peligro o vehículo detenido", "categoria_id": 3, "dificultad": "medio", "respuestas": [{"texto_respuesta": "Solo de noche", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "En situaciones de emergencia o peligro", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "En atascos largos", "es_correcta": False, "orden_respuesta": 3}]},
    {"texto_pregunta": "¿Qué es la conducción defensiva?", "explicacion": "Es anticiparse a los riesgos y mantener actitud prudente al volante", "categoria_id": 3, "dificultad": "medio", "respuestas": [{"texto_respuesta": "Conducir muy lento", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "Anticiparse a los peligros", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "Usar bocina constantemente", "es_correcta": False, "orden_respuesta": 3}]},
    {"texto_pregunta": "¿Cuál es la tasa máxima de alcohol permitida para conductores noveles?", "explicacion": "Los conductores noveles tienen límite de 0,15 mg/l en aire espirado", "categoria_id": 3, "dificultad": "dificil", "respuestas": [{"texto_respuesta": "0,25 mg/l", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "0,15 mg/l", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "0,00 mg/l", "es_correcta": False, "orden_respuesta": 3}]},
    {"texto_pregunta": "¿Qué debe hacer ante una luz amarilla intermitente?", "explicacion": "Debe extremar la precaución y respetar las normas de prioridad", "categoria_id": 3, "dificultad": "medio", "respuestas": [{"texto_respuesta": "Detenerse siempre", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "Extremar precaución", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "Acelerar para pasar", "es_correcta": False, "orden_respuesta": 3}]},
    
    # Mecánica y Mantenimiento
    {"texto_pregunta": "¿Cada cuánto tiempo se debe revisar la presión de los neumáticos?", "explicacion": "Se recomienda revisar la presión al menos una vez al mes", "categoria_id": 4, "dificultad": "medio", "respuestas": [{"texto_respuesta": "Cada semana", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "Cada mes", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "Cada 6 meses", "es_correcta": False, "orden_respuesta": 3}]},
    {"texto_pregunta": "¿Qué profundidad mínima debe tener el dibujo de los neumáticos?", "explicacion": "El dibujo debe tener al menos 1,6 mm de profundidad en toda la banda de rodadura", "categoria_id": 4, "dificultad": "dificil", "respuestas": [{"texto_respuesta": "1,0 mm", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "1,6 mm", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "2,0 mm", "es_correcta": False, "orden_respuesta": 3}]},
    {"texto_pregunta": "¿Cada cuántos kilómetros debe cambiar el aceite del motor?", "explicacion": "Generalmente entre 10.000 y 15.000 km, según especificaciones del fabricante", "categoria_id": 4, "dificultad": "medio", "respuestas": [{"texto_respuesta": "Cada 5.000 km", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "Según manual del fabricante", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "Cada 25.000 km", "es_correcta": False, "orden_respuesta": 3}]},
    {"texto_pregunta": "¿Qué líquido debe revisar regularmente en el vehículo?", "explicacion": "Debe revisar aceite, líquido de frenos, refrigerante y líquido limpiaparabrisas", "categoria_id": 4, "dificultad": "facil", "respuestas": [{"texto_respuesta": "Solo la gasolina", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "Todos los líquidos del vehículo", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "Solo el aceite", "es_correcta": False, "orden_respuesta": 3}]},
    {"texto_pregunta": "¿Qué indica una luz roja en el tablero?", "explicacion": "Una luz roja indica una avería grave que requiere detención inmediata", "categoria_id": 4, "dificultad": "medio", "respuestas": [{"texto_respuesta": "Problema menor", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "Avería grave, detenerse", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "Solo advertencia", "es_correcta": False, "orden_respuesta": 3}]}
]

def create_questions_with_retry():
    """Crear todas las preguntas del banco con reintentos"""
    for attempt in range(MAX_RETRIES):
        try:
            print(f"Intento {attempt + 1} de crear preguntas...")
            for i, pregunta_data in enumerate(banco_preguntas):
                respuestas_data = pregunta_data.pop("respuestas")
                response = requests.post(
                    f"{API_BASE}/preguntas", 
                    json={"respuestas": respuestas_data, **pregunta_data}
                )
                response.raise_for_status()
                print(f"✓ Pregunta {i+1} creada: {pregunta_data['texto_pregunta'][:50]}...")
            return True
        except RequestException as e:
            print(f"Error en el intento {attempt + 1}: {e}")
            if attempt < MAX_RETRIES - 1:
                print(f"Reintentando en {RETRY_DELAY} segundos...")
                time.sleep(RETRY_DELAY)
            else:
                print("Se alcanzó el máximo número de intentos")
                return False

def main():
    print("Inicializando datos completos para AutoTest")
    print("=" * 50)
    
    success = create_questions_with_retry()
    
    print("=" * 50)
    if success:
        print("Inicialización completada!")
    else:
        print("La inicialización falló después de varios intentos")

if __name__ == "__main__":
    main()
