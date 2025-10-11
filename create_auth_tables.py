#!/usr/bin/env python3
"""
Script para crear las tablas de autenticación en la base de datos
"""

import os
import sys
from sqlalchemy import create_engine

# Añadir el directorio backend al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from database import DATABASE_URL, Base
from models import Categoria, Pregunta, Respuesta, Examen, PreguntaExamen
from models_auth import Usuario, HistorialExamen, DetalleRespuesta, ErrorFrecuente, ProgresoCategoria, SesionChatbot

def crear_tablas_autenticacion():
    """
    Crea las tablas de autenticación sin borrar las tablas existentes
    """
    print("Conectando a la base de datos...")
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    
    try:
        print("Creando tablas de autenticación...")
        
        # Crear solo las tablas que no existen (no borra las existentes)
        Base.metadata.create_all(bind=engine)
        
        print("\n=== TABLAS CREADAS ===")
        print("✓ usuarios")
        print("✓ historial_examenes")
        print("✓ detalles_respuestas")
        print("✓ errores_frecuentes")
        print("✓ progreso_categorias")
        print("✓ sesiones_chatbot")
        print("\n¡Tablas de autenticación creadas correctamente!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise

if __name__ == "__main__":
    print("="*60)
    print("CREACIÓN DE TABLAS DE AUTENTICACIÓN")
    print("="*60)
    print("\nEste script creará las tablas necesarias para el sistema de usuarios:")
    print("  • Tabla de usuarios")
    print("  • Historial de exámenes")
    print("  • Errores frecuentes")
    print("  • Progreso por categorías")
    print("  • Sesiones de chatbot")
    print("\n" + "="*60)
    
    crear_tablas_autenticacion()
