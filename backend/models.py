from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Enum, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()

class DificultadEnum(str, enum.Enum):
    facil = "facil"
    medio = "medio"
    dificil = "dificil"

class Categoria(Base):
    __tablename__ = "categorias"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    
    # Relación con preguntas
    preguntas = relationship("Pregunta", back_populates="categoria")

class Pregunta(Base):
    __tablename__ = "preguntas"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    texto_pregunta = Column(Text, nullable=False)
    imagen_url = Column(String(255))
    explicacion = Column(Text)
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    dificultad = Column(Enum(DificultadEnum), default=DificultadEnum.medio)
    es_activa = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    
    # Relaciones
    categoria = relationship("Categoria", back_populates="preguntas")
    respuestas = relationship("Respuesta", back_populates="pregunta", cascade="all, delete-orphan")

class Respuesta(Base):
    __tablename__ = "respuestas"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    pregunta_id = Column(Integer, ForeignKey("preguntas.id"), nullable=False)
    texto_respuesta = Column(Text, nullable=False)
    es_correcta = Column(Boolean, default=False)
    orden_respuesta = Column(Integer, default=1)
    
    # Relación
    pregunta = relationship("Pregunta", back_populates="respuestas")

class Examen(Base):
    __tablename__ = "examenes"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    duracion_minutos = Column(Integer, default=30)
    num_preguntas = Column(Integer, default=30)
    categoria_principal_id = Column(Integer, ForeignKey("categorias.id"))
    es_activo = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    
    # Relaciones
    categoria_principal = relationship("Categoria")
    preguntas_examen = relationship("PreguntaExamen", back_populates="examen")

class PreguntaExamen(Base):
    __tablename__ = "preguntas_examenes"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    examen_id = Column(Integer, ForeignKey("examenes.id"), nullable=False)
    pregunta_id = Column(Integer, ForeignKey("preguntas.id"), nullable=False)
    orden_pregunta = Column(Integer, nullable=False)
    
    # Relaciones
    examen = relationship("Examen", back_populates="preguntas_examen")
    pregunta = relationship("Pregunta")
