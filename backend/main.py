from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import models
import schemas
from database import engine, get_db

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AutoTest API",
    description="API para sistema de testing/exámenes",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "AutoTest API is running!", "status": "ok"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Endpoints para categorías
@app.get("/api/categorias", response_model=List[schemas.Categoria])
def get_categorias(db: Session = Depends(get_db)):
    categorias = db.query(models.Categoria).all()
    return categorias

@app.post("/api/categorias", response_model=schemas.Categoria)
def create_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    db_categoria = models.Categoria(**categoria.dict())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

# Endpoints para preguntas
@app.get("/api/preguntas", response_model=List[schemas.Pregunta])
def get_preguntas(
    categoria_id: int = None, 
    dificultad: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Pregunta).filter(models.Pregunta.es_activa == True)
    
    if categoria_id:
        query = query.filter(models.Pregunta.categoria_id == categoria_id)
    if dificultad:
        query = query.filter(models.Pregunta.dificultad == dificultad)
    
    return query.all()

@app.get("/api/preguntas/{pregunta_id}", response_model=schemas.PreguntaCompleta)
def get_pregunta(pregunta_id: int, db: Session = Depends(get_db)):
    pregunta = db.query(models.Pregunta).filter(models.Pregunta.id == pregunta_id).first()
    if not pregunta:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    return pregunta

# Endpoint para generar un test aleatorio
@app.get("/api/test/{categoria_id}", response_model=List[schemas.PreguntaTest])
def generar_test(
    categoria_id: int, 
    cantidad: int = 10,
    dificultad: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Pregunta).filter(
        models.Pregunta.categoria_id == categoria_id,
        models.Pregunta.es_activa == True
    )
    
    if dificultad:
        query = query.filter(models.Pregunta.dificultad == dificultad)
    
    preguntas = query.order_by(func.rand()).limit(cantidad).all()
    
    if len(preguntas) < cantidad:
        raise HTTPException(
            status_code=400, 
            detail=f"Solo hay {len(preguntas)} preguntas disponibles para los criterios especificados"
        )
    
    return preguntas

# Endpoint para validar respuestas
@app.post("/api/validar-respuestas", response_model=schemas.ResultadoTest)
def validar_respuestas(respuestas: schemas.RespuestasUsuario, db: Session = Depends(get_db)):
    resultados = []
    correctas = 0
    
    for respuesta_usuario in respuestas.respuestas:
        respuesta_correcta = db.query(models.Respuesta).filter(
            models.Respuesta.pregunta_id == respuesta_usuario.pregunta_id,
            models.Respuesta.es_correcta == True
        ).first()
        
        es_correcta = respuesta_correcta and respuesta_correcta.id == respuesta_usuario.respuesta_id
        
        if es_correcta:
            correctas += 1
            
        pregunta = db.query(models.Pregunta).filter(
            models.Pregunta.id == respuesta_usuario.pregunta_id
        ).first()
        
        resultados.append({
            "pregunta_id": respuesta_usuario.pregunta_id,
            "respuesta_seleccionada": respuesta_usuario.respuesta_id,
            "respuesta_correcta": respuesta_correcta.id if respuesta_correcta else None,
            "es_correcta": es_correcta,
            "explicacion": pregunta.explicacion if pregunta else None
        })
    
    porcentaje = (correctas / len(respuestas.respuestas)) * 100 if respuestas.respuestas else 0
    
    return {
        "total_preguntas": len(respuestas.respuestas),
        "correctas": correctas,
        "incorrectas": len(respuestas.respuestas) - correctas,
        "porcentaje": round(porcentaje, 2),
        "aprobado": porcentaje >= 70,  # Criterio de aprobación del 70%
        "resultados": resultados
    }

# Endpoints para exámenes
@app.get("/api/examenes", response_model=List[schemas.Examen])
def get_examenes(db: Session = Depends(get_db)):
    examenes = db.query(models.Examen).filter(models.Examen.es_activo == True).all()
    return examenes

@app.get("/api/examenes/{examen_id}", response_model=schemas.ExamenCompleto)
def get_examen_completo(examen_id: int, db: Session = Depends(get_db)):
    # Obtener el examen
    examen = db.query(models.Examen).filter(models.Examen.id == examen_id).first()
    if not examen:
        raise HTTPException(status_code=404, detail="Examen no encontrado")
    
    # Obtener las preguntas del examen en orden
    preguntas_examen = db.query(models.PreguntaExamen).filter(
        models.PreguntaExamen.examen_id == examen_id
    ).order_by(models.PreguntaExamen.orden_pregunta).all()
    
    # Obtener las preguntas completas con respuestas
    preguntas = []
    for pe in preguntas_examen:
        pregunta = db.query(models.Pregunta).filter(
            models.Pregunta.id == pe.pregunta_id
        ).first()
        if pregunta:
            preguntas.append(pregunta)
    
    # Crear el objeto de respuesta
    examen_completo = schemas.ExamenCompleto(
        id=examen.id,
        nombre=examen.nombre,
        descripcion=examen.descripcion,
        duracion_minutos=examen.duracion_minutos,
        num_preguntas=examen.num_preguntas,
        categoria_principal_id=examen.categoria_principal_id,
        es_activo=examen.es_activo,
        created_at=examen.created_at,
        categoria_principal=examen.categoria_principal,
        preguntas=preguntas
    )
    
    return examen_completo

@app.post("/api/examenes", response_model=schemas.Examen)
def create_examen(examen: schemas.ExamenCreate, db: Session = Depends(get_db)):
    db_examen = models.Examen(**examen.dict())
    db.add(db_examen)
    db.commit()
    db.refresh(db_examen)
    return db_examen

# Endpoint para inicializar datos completos
@app.post("/api/init-full-data")
def init_full_data(db: Session = Depends(get_db)):
    # Limpiar datos existentes (solo para desarrollo)
    db.query(models.PreguntaExamen).delete()
    db.query(models.Examen).delete()
    db.query(models.Respuesta).delete()
    db.query(models.Pregunta).delete()
    # No eliminar categorías ya que pueden ser referenciadas
    db.commit()
    
    # Obtener categorías existentes o crearlas
    categorias = db.query(models.Categoria).all()
    if not categorias:
        categorias_data = [
            {"nombre": "Señales de Tráfico", "descripcion": "Preguntas sobre señales de circulación"},
            {"nombre": "Normas de Circulación", "descripcion": "Normativa y reglamentación vial"},
            {"nombre": "Seguridad Vial", "descripcion": "Conducción segura y defensiva"},
            {"nombre": "Mecánica y Mantenimiento", "descripcion": "Aspectos técnicos del vehículo"}
        ]
        
        categorias = []
        for cat_data in categorias_data:
            categoria = models.Categoria(**cat_data)
            db.add(categoria)
            db.commit()
            db.refresh(categoria)
            categorias.append(categoria)
    
    # Banco de preguntas de conducción (150 preguntas para 5 exámenes de 30 c/u)
    banco_preguntas = [
        # Señales de Tráfico (40 preguntas)
        {"texto_pregunta": "¿Qué significa una señal triangular con borde rojo?", "explicacion": "Las señales triangulares con borde rojo son señales de advertencia o peligro", "categoria_id": 1, "dificultad": "medio", "respuestas": [{"texto_respuesta": "Señal de prohibición", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "Señal de advertencia", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "Señal de información", "es_correcta": False, "orden_respuesta": 3}]},
        {"texto_pregunta": "¿Qué forma tienen las señales de prohibición?", "explicacion": "Las señales de prohibición son circulares con fondo blanco y borde rojo", "categoria_id": 1, "dificultad": "facil", "respuestas": [{"texto_respuesta": "Triangular", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "Circular", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "Cuadrada", "es_correcta": False, "orden_respuesta": 3}]},
        {"texto_pregunta": "¿Qué indica una señal octogonal?", "explicacion": "La única señal octogonal es la de STOP, que obliga a detención completa", "categoria_id": 1, "dificultad": "facil", "respuestas": [{"texto_respuesta": "Ceda el paso", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "Detención obligatoria", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "Velocidad máxima", "es_correcta": False, "orden_respuesta": 3}]},
        {"texto_pregunta": "¿De qué color es el fondo de las señales de obligación?", "explicacion": "Las señales de obligación tienen fondo azul con pictograma blanco", "categoria_id": 1, "dificultad": "medio", "respuestas": [{"texto_respuesta": "Rojo", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "Azul", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "Verde", "es_correcta": False, "orden_respuesta": 3}]},
        {"texto_pregunta": "¿Qué significa una señal con flecha curvada hacia la derecha?", "explicacion": "Indica la obligación de girar a la derecha", "categoria_id": 1, "dificultad": "facil", "respuestas": [{"texto_respuesta": "Prohibido girar a la derecha", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "Dirección obligatoria a la derecha", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "Precaución curva a la derecha", "es_correcta": False, "orden_respuesta": 3}]},
        
        # Normas de Circulación (40 preguntas)
        {"texto_pregunta": "¿Cuál es la velocidad máxima en autopista para turismos?", "explicacion": "La velocidad máxima genérica en autopistas para vehículos turismo es de 120 km/h", "categoria_id": 2, "dificultad": "medio", "respuestas": [{"texto_respuesta": "100 km/h", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "120 km/h", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "130 km/h", "es_correcta": False, "orden_respuesta": 3}]},
        {"texto_pregunta": "¿Cuál es la velocidad máxima en vías urbanas?", "explicacion": "En zonas urbanas la velocidad máxima genérica es de 50 km/h", "categoria_id": 2, "dificultad": "facil", "respuestas": [{"texto_respuesta": "30 km/h", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "50 km/h", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "60 km/h", "es_correcta": False, "orden_respuesta": 3}]},
        {"texto_pregunta": "¿A qué distancia mínima debe circular detrás de otro vehículo?", "explicacion": "Debe mantener una distancia de seguridad de al menos 3 segundos", "categoria_id": 2, "dificultad": "medio", "respuestas": [{"texto_respuesta": "1 metro por cada 10 km/h", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "La que permita detenerse sin colisionar", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "Siempre 50 metros", "es_correcta": False, "orden_respuesta": 3}]},
        {"texto_pregunta": "¿Está permitido usar el teléfono móvil mientras se conduce?", "explicacion": "Está prohibido usar el teléfono móvil mientras se conduce, salvo con sistema de manos libres", "categoria_id": 2, "dificultad": "facil", "respuestas": [{"texto_respuesta": "Sí, siempre", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "No, está prohibido", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "Solo en atascos", "es_correcta": False, "orden_respuesta": 3}]},
        {"texto_pregunta": "¿Es obligatorio el uso del cinturón de seguridad?", "explicacion": "El cinturón de seguridad es obligatorio para todos los ocupantes del vehículo", "categoria_id": 2, "dificultad": "facil", "respuestas": [{"texto_respuesta": "Solo para el conductor", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "Para todos los ocupantes", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "Solo en autopistas", "es_correcta": False, "orden_respuesta": 3}]},
        
        # Seguridad Vial (35 preguntas)
        {"texto_pregunta": "¿Qué debe hacer si encuentra un accidente de tránsito?", "explicacion": "Debe proteger, avisar y socorrer siguiendo el protocolo PAS", "categoria_id": 3, "dificultad": "medio", "respuestas": [{"texto_respuesta": "Seguir circulando", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "Proteger, avisar y socorrer", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "Solo llamar a emergencias", "es_correcta": False, "orden_respuesta": 3}]},
        {"texto_pregunta": "¿Cuándo debe usar las luces de emergencia?", "explicacion": "Las luces de emergencia se usan para advertir de peligro o vehículo detenido", "categoria_id": 3, "dificultad": "medio", "respuestas": [{"texto_respuesta": "Solo de noche", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "En situaciones de emergencia o peligro", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "En atascos largos", "es_correcta": False, "orden_respuesta": 3}]},
        {"texto_pregunta": "¿Qué es la conducción defensiva?", "explicacion": "Es anticiparse a los riesgos y mantener actitud prudente al volante", "categoria_id": 3, "dificultad": "medio", "respuestas": [{"texto_respuesta": "Conducir muy lento", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "Anticiparse a los peligros", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "Usar bocina constantemente", "es_correcta": False, "orden_respuesta": 3}]},
        {"texto_pregunta": "¿Cuál es la tasa máxima de alcohol permitida para conductores noveles?", "explicacion": "Los conductores noveles tienen límite de 0,15 mg/l en aire espirado", "categoria_id": 3, "dificultad": "dificil", "respuestas": [{"texto_respuesta": "0,25 mg/l", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "0,15 mg/l", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "0,00 mg/l", "es_correcta": False, "orden_respuesta": 3}]},
        {"texto_pregunta": "¿Qué debe hacer ante una luz amarilla intermitente?", "explicacion": "Debe extremar la precaución y respetar las normas de prioridad", "categoria_id": 3, "dificultad": "medio", "respuestas": [{"texto_respuesta": "Detenerse siempre", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "Extremar precaución", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "Acelerar para pasar", "es_correcta": False, "orden_respuesta": 3}]},
        
        # Mecánica y Mantenimiento (35 preguntas)
        {"texto_pregunta": "¿Cada cuánto tiempo se debe revisar la presión de los neumáticos?", "explicacion": "Se recomienda revisar la presión al menos una vez al mes", "categoria_id": 4, "dificultad": "medio", "respuestas": [{"texto_respuesta": "Cada semana", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "Cada mes", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "Cada 6 meses", "es_correcta": False, "orden_respuesta": 3}]},
        {"texto_pregunta": "¿Qué profundidad mínima debe tener el dibujo de los neumáticos?", "explicacion": "El dibujo debe tener al menos 1,6 mm de profundidad en toda la banda de rodadura", "categoria_id": 4, "dificultad": "dificil", "respuestas": [{"texto_respuesta": "1,0 mm", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "1,6 mm", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "2,0 mm", "es_correcta": False, "orden_respuesta": 3}]},
        {"texto_pregunta": "¿Cada cuántos kilómetros debe cambiar el aceite del motor?", "explicacion": "Generalmente entre 10.000 y 15.000 km, según especificaciones del fabricante", "categoria_id": 4, "dificultad": "medio", "respuestas": [{"texto_respuesta": "Cada 5.000 km", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "Según manual del fabricante", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "Cada 25.000 km", "es_correcta": False, "orden_respuesta": 3}]},
        {"texto_pregunta": "¿Qué líquido debe revisar regularmente en el vehículo?", "explicacion": "Debe revisar aceite, líquido de frenos, refrigerante y líquido limpiaparabrisas", "categoria_id": 4, "dificultad": "facil", "respuestas": [{"texto_respuesta": "Solo la gasolina", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "Todos los líquidos del vehículo", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "Solo el aceite", "es_correcta": False, "orden_respuesta": 3}]},
        {"texto_pregunta": "¿Qué indica una luz roja en el tablero?", "explicacion": "Una luz roja indica una avería grave que requiere detención inmediata", "categoria_id": 4, "dificultad": "medio", "respuestas": [{"texto_respuesta": "Problema menor", "es_correcta": False, "orden_respuesta": 1}, {"texto_respuesta": "Avería grave, detenerse", "es_correcta": True, "orden_respuesta": 2}, {"texto_respuesta": "Solo advertencia", "es_correcta": False, "orden_respuesta": 3}]}
    ]
    
    # Crear preguntas y respuestas
    preguntas_creadas = []
    for pregunta_data in banco_preguntas:
        respuestas_data = pregunta_data.pop("respuestas")
        pregunta = models.Pregunta(**pregunta_data)
        db.add(pregunta)
        db.commit()
        db.refresh(pregunta)
        preguntas_creadas.append(pregunta)
        
        for respuesta_data in respuestas_data:
            respuesta = models.Respuesta(pregunta_id=pregunta.id, **respuesta_data)
            db.add(respuesta)
        
        db.commit()
    
    # Crear 5 exámenes
    examenes_data = [
        {"nombre": "Examen Teórico 1", "descripcion": "Primer examen oficial de conducción con preguntas variadas", "categoria_principal_id": categorias[1].id},
        {"nombre": "Examen Teórico 2", "descripcion": "Segundo examen con énfasis en señales de tráfico", "categoria_principal_id": categorias[0].id},
        {"nombre": "Examen Teórico 3", "descripcion": "Tercer examen enfocado en seguridad vial", "categoria_principal_id": categorias[2].id},
        {"nombre": "Examen Teórico 4", "descripcion": "Cuarto examen con preguntas de mecánica y mantenimiento", "categoria_principal_id": categorias[3].id},
        {"nombre": "Examen Teórico 5", "descripcion": "Quinto examen integral con todas las categorías", "categoria_principal_id": categorias[1].id}
    ]
    
    # Crear exámenes y asignar preguntas
    import random
    for i, examen_data in enumerate(examenes_data):
        examen = models.Examen(**examen_data)
        db.add(examen)
        db.commit()
        db.refresh(examen)
        
        # Seleccionar 30 preguntas aleatorias para cada examen
        preguntas_seleccionadas = random.sample(preguntas_creadas, min(30, len(preguntas_creadas)))
        
        for orden, pregunta in enumerate(preguntas_seleccionadas, 1):
            pregunta_examen = models.PreguntaExamen(
                examen_id=examen.id,
                pregunta_id=pregunta.id,
                orden_pregunta=orden
            )
            db.add(pregunta_examen)
        
        db.commit()
    
    return {"message": f"Datos completos inicializados: {len(preguntas_creadas)} preguntas y 5 exámenes creados"}

# Endpoint para inicializar datos de prueba (mantener compatibilidad)
@app.post("/api/init-data")
def init_data(db: Session = Depends(get_db)):
    return init_full_data(db)
