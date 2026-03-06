"""
Sistema de autenticación seguro para AutoTest
- Solo usuarios registrados y anónimos
- Sin roles administrativos por seguridad
- Compatible con sistema existente
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Float, DateTime, TIMESTAMP, func, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
from datetime import datetime

# Importar Base existente o crear nueva
from database import Base


# Contexto para hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Usuario(Base):
    """
    Modelo simple de Usuario para autenticación
    - Sin roles administrativos por seguridad
    - Solo distinción entre registrado/anónimo
    """
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # Información personal opcional
    nombre = Column(String(100))
    apellidos = Column(String(200))
    
    # Estado del usuario
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)  # Para verificación por email
    
    # Tracking temporal
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    last_login = Column(DateTime, nullable=True)
    
    # Configuración de límites
    chatbot_preguntas_dia = Column(Integer, default=20)  # Usuarios registrados: 20/día
    
    # Relaciones
    historial_examenes = relationship("HistorialExamen", back_populates="usuario", cascade="all, delete-orphan")
    errores_frecuentes = relationship("ErrorFrecuente", back_populates="usuario", cascade="all, delete-orphan")
    progreso_categorias = relationship("ProgresoCategoria", back_populates="usuario", cascade="all, delete-orphan")
    
    def verify_password(self, password: str) -> bool:
        """Verifica si la contraseña es correcta"""
        return pwd_context.verify(password, self.password_hash)
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Genera hash de contraseña"""
        return pwd_context.hash(password)
    
    def to_dict(self):
        """Convierte el usuario a diccionario (sin información sensible)"""
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "nombre": self.nombre,
            "apellidos": self.apellidos,
            "is_verified": self.is_verified,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "chatbot_limite_diario": self.chatbot_preguntas_dia
        }


class HistorialExamen(Base):
    """
    Registro de exámenes completados por usuarios registrados
    """
    __tablename__ = "historial_examenes"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    examen_id = Column(Integer, ForeignKey("examenes.id"), nullable=True)
    
    # Información del examen
    nombre_examen = Column(String(200))
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=True)
    tipo_examen = Column(String(50), default="examen")  # examen, practica, chatbot
    
    # Resultados
    total_preguntas = Column(Integer, nullable=False)
    respuestas_correctas = Column(Integer, nullable=False)
    respuestas_incorrectas = Column(Integer, nullable=False)
    porcentaje = Column(Float, nullable=False)
    aprobado = Column(Boolean, nullable=False)
    
    # Tiempo
    duracion_segundos = Column(Integer)
    duracion_limite_minutos = Column(Integer, default=30)
    
    # Timestamps
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_finalizacion = Column(DateTime, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="historial_examenes")
    detalles_respuestas = relationship("DetalleRespuesta", back_populates="historial_examen", cascade="all, delete-orphan")
    
    # Índices para consultas eficientes
    __table_args__ = (
        Index('idx_historial_usuario_fecha', 'usuario_id', 'created_at'),
        Index('idx_historial_categoria', 'categoria_id', 'created_at'),
    )


class DetalleRespuesta(Base):
    """
    Detalle granular de cada respuesta en un examen
    """
    __tablename__ = "detalles_respuestas"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    historial_examen_id = Column(Integer, ForeignKey("historial_examenes.id"), nullable=False, index=True)
    pregunta_id = Column(Integer, ForeignKey("preguntas.id"), nullable=False, index=True)
    respuesta_seleccionada_id = Column(Integer, ForeignKey("respuestas.id"), nullable=True)
    respuesta_correcta_id = Column(Integer, ForeignKey("respuestas.id"), nullable=False)
    
    es_correcta = Column(Boolean, nullable=False)
    tiempo_respuesta_segundos = Column(Integer)
    orden_en_examen = Column(Integer)  # Posición de la pregunta en el examen
    
    # Relaciones
    historial_examen = relationship("HistorialExamen", back_populates="detalles_respuestas")


class ErrorFrecuente(Base):
    """
    Agregación de errores por usuario para identificar puntos débiles
    """
    __tablename__ = "errores_frecuentes"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    pregunta_id = Column(Integer, ForeignKey("preguntas.id"), nullable=False, index=True)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=True)
    
    # Contadores
    veces_fallada = Column(Integer, default=1)
    veces_acertada = Column(Integer, default=0)
    
    # Timestamps
    primera_vez_fallada = Column(DateTime, default=datetime.utcnow)
    ultima_vez_fallada = Column(DateTime, default=datetime.utcnow)
    ultima_vez_acertada = Column(DateTime, nullable=True)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="errores_frecuentes")
    
    # Índice único para evitar duplicados por usuario-pregunta
    __table_args__ = (
        Index('idx_unique_usuario_pregunta', 'usuario_id', 'pregunta_id', unique=True),
        Index('idx_errores_categoria', 'categoria_id', 'veces_fallada'),
    )


class ProgresoCategoria(Base):
    """
    Tracking de progreso por categoría temática
    """
    __tablename__ = "progreso_categorias"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False, index=True)
    
    # Estadísticas de progreso
    preguntas_vistas = Column(Integer, default=0)
    preguntas_correctas = Column(Integer, default=0)
    preguntas_incorrectas = Column(Integer, default=0)
    
    # Métricas calculadas
    porcentaje_acierto = Column(Float, default=0.0)
    racha_actual = Column(Integer, default=0)  # Preguntas correctas consecutivas
    mejor_racha = Column(Integer, default=0)
    
    # Nivel estimado (1-5)
    nivel_estimado = Column(Integer, default=1)
    
    # Timestamps
    primera_actividad = Column(DateTime, default=datetime.utcnow)
    ultima_actividad = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="progreso_categorias")
    
    # Índice único para evitar duplicados por usuario-categoría
    __table_args__ = (
        Index('idx_unique_usuario_categoria', 'usuario_id', 'categoria_id', unique=True),
        Index('idx_progreso_nivel', 'categoria_id', 'nivel_estimado'),
    )


class SesionChatbot(Base):
    """
    Control de límites del chatbot para usuarios anónimos
    """
    __tablename__ = "sesiones_chatbot"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    
    # Para usuarios anónimos
    session_token = Column(String(255), index=True, nullable=True)
    ip_address = Column(String(50), nullable=True)
    
    # Control de límites
    preguntas_realizadas = Column(Integer, default=0)
    fecha_sesion = Column(DateTime, default=datetime.utcnow)
    
    # Límite diario para anónimos: 5 preguntas
    LIMITE_ANONIMO = 5
    
    # Índices para consultas eficientes
    __table_args__ = (
        Index('idx_sesion_token_fecha', 'session_token', 'fecha_sesion'),
        Index('idx_sesion_ip_fecha', 'ip_address', 'fecha_sesion'),
    )