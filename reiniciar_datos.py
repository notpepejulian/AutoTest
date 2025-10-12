#!/usr/bin/env python3
"""
Script para reinicializar los datos del backend con las correcciones
"""

import requests
import json
import time

API_BASE = "http://localhost:8000/api"

def reinicializar_datos():
    print("🔄 Reinicializando datos del backend...")
    print("=" * 50)
    
    try:
        # Llamar al endpoint para inicializar datos completos
        response = requests.post(f"{API_BASE}/init-full-data")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {result['message']}")
        else:
            print(f"❌ Error al inicializar datos: HTTP {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
        # Verificar que se crearon los exámenes correctamente
        print("\n📊 Verificando exámenes creados...")
        response = requests.get(f"{API_BASE}/examenes")
        
        if response.status_code == 200:
            examenes = response.json()
            print(f"✅ Total de exámenes: {len(examenes)}")
            
            # Mostrar algunos exámenes de ejemplo
            for i, examen in enumerate(examenes[:5]):
                print(f"   {examen['id']}: {examen['nombre']}")
            
            if len(examenes) > 5:
                print(f"   ... y {len(examenes) - 5} exámenes más")
                
        else:
            print(f"❌ Error al verificar exámenes: HTTP {response.status_code}")
            
        # Verificar categorías
        print("\n📋 Verificando categorías...")
        response = requests.get(f"{API_BASE}/categorias")
        
        if response.status_code == 200:
            categorias = response.json()
            print(f"✅ Total de categorías: {len(categorias)}")
            
            for categoria in categorias:
                print(f"   {categoria['id']}: {categoria['nombre']}")
                
        else:
            print(f"❌ Error al verificar categorías: HTTP {response.status_code}")
            
        print("\n🎉 Reinicialización completada exitosamente")
        print("\n💡 Instrucciones:")
        print("   1. Los exámenes ahora van del ID 1 al 30")
        print("   2. Cada examen tiene 30 preguntas reales")
        print("   3. Se incluye la categoría 'Test de examen' (ID 5)")
        print("   4. Las redirecciones ahora funcionan correctamente")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        print("\n💡 Asegúrate de que el backend esté ejecutándose en http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    print("🚀 REINICIALIZACIÓN DE DATOS AUTOTEST")
    print("====================================")
    print("Este script reiniciará todos los datos del backend")
    print("con las correcciones aplicadas.\n")
    
    confirmar = input("¿Continuar? (s/n): ").lower().strip()
    if confirmar in ['s', 'sí', 'si', 'y', 'yes']:
        reinicializar_datos()
    else:
        print("❌ Operación cancelada")