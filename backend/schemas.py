from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Esquemas base para Respuesta
class RespuestaBase(BaseModel):
    texto_respuesta: str
    es_correcta: bool = False
    orden_respuesta: int = 1

class RespuestaCreate(RespuestaBase):
    pass

class Respuesta(RespuestaBase):
    id: int
    pregunta_id: int
    
    class Config:
        from_attributes = True

# Esquemas para Respuesta sin mostrar la correcta (para tests)
class RespuestaPublica(BaseModel):
    id: int
    texto_respuesta: str
    orden_respuesta: int
    
    class Config:
        from_attributes = True

# Esquemas base para Categoria
class CategoriaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Esquemas base para Pregunta
class PreguntaBase(BaseModel):
    texto_pregunta: str
    imagen_url: Optional[str] = None
    explicacion: Optional[str] = None
    categoria_id: int
    dificultad: str = "medio"
    es_activa: bool = True

class PreguntaCreate(PreguntaBase):
    respuestas: Optional[List[RespuestaCreate]] = []

class Pregunta(PreguntaBase):
    id: int
    created_at: datetime
    categoria: Optional[Categoria] = None
    
    class Config:
        from_attributes = True

class PreguntaCompleta(Pregunta):
    respuestas: List[Respuesta] = []
    
    class Config:
        from_attributes = True

# Esquema para preguntas en tests (sin mostrar respuestas correctas)
class PreguntaTest(BaseModel):
    id: int
    texto_pregunta: str
    imagen_url: Optional[str] = None
    respuestas: List[RespuestaPublica] = []
    
    class Config:
        from_attributes = True

# Esquemas para validar respuestas de usuario
class RespuestaUsuario(BaseModel):
    pregunta_id: int
    respuesta_id: int

class RespuestasUsuario(BaseModel):
    respuestas: List[RespuestaUsuario]

# Esquema para resultado de test
class ResultadoPregunta(BaseModel):
    pregunta_id: int
    respuesta_seleccionada: int
    respuesta_correcta: Optional[int]
    es_correcta: bool
    explicacion: Optional[str] = None

class ResultadoTest(BaseModel):
    total_preguntas: int
    correctas: int
    incorrectas: int
    porcentaje: float
    aprobado: bool
    resultados: List[ResultadoPregunta]

# Esquemas para Exámenes
class ExamenBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    duracion_minutos: int = 30
    num_preguntas: int = 30
    categoria_principal_id: Optional[int] = None
    es_activo: bool = True

class ExamenCreate(ExamenBase):
    pass

class Examen(ExamenBase):
    id: int
    created_at: datetime
    categoria_principal: Optional[Categoria] = None
    
    class Config:
        from_attributes = True

class ExamenCompleto(Examen):
    preguntas: List[PreguntaTest] = []
    
    class Config:
        from_attributes = True
