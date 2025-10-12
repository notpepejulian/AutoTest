#!/usr/bin/env python3
"""
Script para generar tests automáticamente desde el banco de 1309 preguntas DGT
Crea tests variados por categoría y tests mixtos con distribución equilibrada
"""

import random
from typing import List, Dict, Tuple
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Configuración directa de conexión
DATABASE_URL = "mysql+pymysql://nj17dssdsnj:zGmPTVYFkTQBUP2V7uizIfWjs5@localhost:3306/autotest_db"
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class GeneradorTestsAutomaticos:
    """Generador de tests automáticos basado en el banco de preguntas DGT"""
    
    def __init__(self):
        self.db = SessionLocal()
        self.categorias = self._obtener_categorias()
        self.preguntas_por_categoria = self._obtener_preguntas_por_categoria()
    
    def _obtener_categorias(self) -> Dict[int, str]:
        """Obtiene las categorías disponibles"""
        query = text("SELECT id, nombre FROM categorias ORDER BY id")
        result = self.db.execute(query).fetchall()
        return {row.id: row.nombre for row in result}
    
    def _obtener_preguntas_por_categoria(self) -> Dict[int, List[int]]:
        """Obtiene las preguntas agrupadas por categoría"""
        query = text("SELECT id, categoria_id FROM preguntas WHERE es_activa = 1 ORDER BY id")
        result = self.db.execute(query).fetchall()
        
        preguntas = {}
        for row in result:
            if row.categoria_id not in preguntas:
                preguntas[row.categoria_id] = []
            preguntas[row.categoria_id].append(row.id)
        
        return preguntas
    
    def limpiar_tests_existentes(self):
        """Limpia todos los tests existentes para empezar de cero"""
        print("🔄 Limpiando tests existentes...")
        
        try:
            # Eliminar preguntas de examenes
            self.db.execute(text("DELETE FROM preguntas_examenes"))
            
            # Eliminar examenes
            self.db.execute(text("DELETE FROM examenes"))
            
            # Resetear auto_increment
            self.db.execute(text("ALTER TABLE examenes AUTO_INCREMENT = 1"))
            self.db.execute(text("ALTER TABLE preguntas_examenes AUTO_INCREMENT = 1"))
            
            self.db.commit()
            print("✅ Tests existentes eliminados")
            
        except Exception as e:
            print(f"❌ Error limpiando tests: {e}")
            self.db.rollback()
            raise
    
    def crear_test_por_categoria(self, categoria_id: int, num_preguntas: int = 30, 
                                variante: int = 1) -> int:
        """Crea un test específico de una categoría"""
        
        categoria_nombre = self.categorias[categoria_id]
        preguntas_disponibles = self.preguntas_por_categoria.get(categoria_id, [])
        
        if len(preguntas_disponibles) < num_preguntas:
            print(f"⚠️  Solo hay {len(preguntas_disponibles)} preguntas en {categoria_nombre}")
            num_preguntas = len(preguntas_disponibles)
        
        # Seleccionar preguntas aleatorias
        preguntas_seleccionadas = random.sample(preguntas_disponibles, num_preguntas)
        
        # Crear el examen
        nombre = f"Test {categoria_nombre} - Variante {variante}"
        descripcion = f"Test especializado en {categoria_nombre.lower()} con {num_preguntas} preguntas seleccionadas aleatoriamente del banco oficial DGT."
        
        examen_id = self._crear_examen(nombre, descripcion, 30, num_preguntas, categoria_id)
        
        # Asignar preguntas al examen
        self._asignar_preguntas_a_examen(examen_id, preguntas_seleccionadas)
        
        return examen_id
    
    def crear_test_mixto(self, num_preguntas: int = 30, variante: int = 1,
                        distribucion_personalizada: Dict[int, int] = None) -> int:
        """Crea un test mixto con preguntas de todas las categorías"""
        
        if distribucion_personalizada:
            distribucion = distribucion_personalizada
        else:
            # Distribución equilibrada por defecto
            distribucion = self._calcular_distribucion_equilibrada(num_preguntas)
        
        preguntas_seleccionadas = []
        
        # Seleccionar preguntas de cada categoría según la distribución
        for categoria_id, cantidad in distribucion.items():
            if categoria_id in self.preguntas_por_categoria:
                disponibles = self.preguntas_por_categoria[categoria_id]
                if len(disponibles) >= cantidad:
                    seleccionadas = random.sample(disponibles, cantidad)
                    preguntas_seleccionadas.extend(seleccionadas)
                else:
                    # Si no hay suficientes, tomar todas las disponibles
                    preguntas_seleccionadas.extend(disponibles)
        
        # Mezclar las preguntas para que no estén agrupadas por categoría
        random.shuffle(preguntas_seleccionadas)
        
        # Ajustar al número exacto si es necesario
        if len(preguntas_seleccionadas) > num_preguntas:
            preguntas_seleccionadas = preguntas_seleccionadas[:num_preguntas]
        
        # Crear el examen
        nombre = f"Test Mixto - Variante {variante}"
        descripcion = f"Test integral con {len(preguntas_seleccionadas)} preguntas de todas las categorías, ideal para preparación completa del examen teórico."
        
        examen_id = self._crear_examen(nombre, descripcion, 30, len(preguntas_seleccionadas), 5)  # Categoría 5 = Test de examen
        
        # Asignar preguntas al examen
        self._asignar_preguntas_a_examen(examen_id, preguntas_seleccionadas)
        
        return examen_id
    
    def _calcular_distribucion_equilibrada(self, num_preguntas: int) -> Dict[int, int]:
        """Calcula una distribución equilibrada de preguntas por categoría"""
        
        # Distribución aproximada basada en el examen oficial DGT
        porcentajes = {
            1: 0.20,  # Señales de Tráfico - 20%
            2: 0.18,  # Normas de Circulación - 18%
            3: 0.25,  # Seguridad Vial - 25%
            4: 0.15,  # Mecánica y Mantenimiento - 15%
            5: 0.22,  # Test de examen (mixtas) - 22%
        }
        
        distribucion = {}
        total_asignadas = 0
        
        # Calcular preguntas por categoría
        for categoria_id, porcentaje in porcentajes.items():
            cantidad = int(num_preguntas * porcentaje)
            distribucion[categoria_id] = cantidad
            total_asignadas += cantidad
        
        # Ajustar diferencias por redondeo
        diferencia = num_preguntas - total_asignadas
        if diferencia > 0:
            # Añadir las preguntas restantes a la categoría con más preguntas disponibles
            categoria_mayor = max(self.preguntas_por_categoria.keys(), 
                                key=lambda k: len(self.preguntas_por_categoria[k]))
            distribucion[categoria_mayor] += diferencia
        
        return distribucion
    
    def _crear_examen(self, nombre: str, descripcion: str, duracion: int, 
                     num_preguntas: int, categoria_principal_id: int) -> int:
        """Crea un registro de examen en la base de datos"""
        
        query = text("""
            INSERT INTO examenes (nombre, descripcion, duracion_minutos, num_preguntas, 
                                categoria_principal_id, es_activo) 
            VALUES (:nombre, :descripcion, :duracion, :num_preguntas, :categoria_id, :activo)
        """)
        
        result = self.db.execute(query, {
            'nombre': nombre,
            'descripcion': descripcion,
            'duracion': duracion,
            'num_preguntas': num_preguntas,
            'categoria_id': categoria_principal_id,
            'activo': True
        })
        
        return result.lastrowid
    
    def _asignar_preguntas_a_examen(self, examen_id: int, preguntas: List[int]):
        """Asigna preguntas específicas a un examen"""
        
        for i, pregunta_id in enumerate(preguntas, 1):
            query = text("""
                INSERT INTO preguntas_examenes (examen_id, pregunta_id, orden_pregunta) 
                VALUES (:examen_id, :pregunta_id, :orden)
            """)
            
            self.db.execute(query, {
                'examen_id': examen_id,
                'pregunta_id': pregunta_id,
                'orden': i
            })
    
    def generar_coleccion_completa_tests(self):
        """Genera una colección completa de tests variados"""
        
        print("🚀 GENERANDO COLECCIÓN COMPLETA DE TESTS")
        print("=" * 50)
        
        tests_creados = []
        
        try:
            # 1. Tests específicos por categoría (3 variantes cada una)
            print("\n📚 Generando tests por categoría...")
            for categoria_id, categoria_nombre in self.categorias.items():
                print(f"  📖 Creando tests de {categoria_nombre}...")
                
                for variante in range(1, 4):  # 3 variantes por categoría
                    examen_id = self.crear_test_por_categoria(categoria_id, 30, variante)
                    tests_creados.append(examen_id)
                    print(f"    ✅ Test {categoria_nombre} - Variante {variante} (ID: {examen_id})")
            
            # 2. Tests mixtos con diferentes distribuciones (5 variantes)
            print("\n🎯 Generando tests mixtos...")
            for variante in range(1, 6):  # 5 variantes mixtas
                examen_id = self.crear_test_mixto(30, variante)
                tests_creados.append(examen_id)
                print(f"    ✅ Test Mixto - Variante {variante} (ID: {examen_id})")
            
            # 3. Tests especializados adicionales
            print("\n⭐ Generando tests especializados...")
            
            # Test enfocado en señales (mayor proporción de señales)
            distribucion_senales = {1: 15, 2: 5, 3: 5, 4: 3, 5: 2}
            examen_id = self.crear_test_mixto(30, distribucion_personalizada=distribucion_senales)
            tests_creados.append(examen_id)
            
            # Actualizar nombre para que sea más descriptivo
            self.db.execute(text("UPDATE examenes SET nombre = 'Test Especializado - Señales Intensivo' WHERE id = :id"), 
                          {'id': examen_id})
            print(f"    ✅ Test Especializado - Señales Intensivo (ID: {examen_id})")
            
            # Test enfocado en seguridad vial
            distribucion_seguridad = {1: 3, 2: 5, 3: 15, 4: 4, 5: 3}
            examen_id = self.crear_test_mixto(30, distribucion_personalizada=distribucion_seguridad)
            tests_creados.append(examen_id)
            
            self.db.execute(text("UPDATE examenes SET nombre = 'Test Especializado - Seguridad Vial Intensivo' WHERE id = :id"), 
                          {'id': examen_id})
            print(f"    ✅ Test Especializado - Seguridad Vial Intensivo (ID: {examen_id})")
            
            # Test de repaso general (distribución muy equilibrada)
            distribucion_repaso = {1: 6, 2: 6, 3: 6, 4: 6, 5: 6}
            examen_id = self.crear_test_mixto(30, distribucion_personalizada=distribucion_repaso)
            tests_creados.append(examen_id)
            
            self.db.execute(text("UPDATE examenes SET nombre = 'Test de Repaso General' WHERE id = :id"), 
                          {'id': examen_id})
            print(f"    ✅ Test de Repaso General (ID: {examen_id})")
            
            # Confirmar cambios
            self.db.commit()
            
            print(f"\n🎉 GENERACIÓN COMPLETADA")
            print(f"  📝 Total de tests creados: {len(tests_creados)}")
            print(f"  🎯 Tests por categoría: {len(self.categorias) * 3}")
            print(f"  🔀 Tests mixtos: 5")
            print(f"  ⭐ Tests especializados: 3")
            
            return tests_creados
            
        except Exception as e:
            print(f"❌ Error durante la generación: {e}")
            self.db.rollback()
            raise
    
    def mostrar_estadisticas_finales(self):
        """Muestra estadísticas de los tests generados"""
        
        print("\n📊 ESTADÍSTICAS FINALES")
        print("=" * 30)
        
        # Total de examenes
        total_examenes = self.db.execute(text("SELECT COUNT(*) as count FROM examenes")).fetchone()
        print(f"📝 Total de tests: {total_examenes.count}")
        
        # Total de preguntas en examenes
        total_preguntas_examenes = self.db.execute(text("SELECT COUNT(*) as count FROM preguntas_examenes")).fetchone()
        print(f"❓ Total de preguntas asignadas: {total_preguntas_examenes.count}")
        
        # Tests por categoría
        query = text("""
            SELECT c.nombre, COUNT(e.id) as num_tests
            FROM categorias c
            LEFT JOIN examenes e ON c.id = e.categoria_principal_id
            GROUP BY c.id, c.nombre
            ORDER BY num_tests DESC
        """)
        
        print("\n📊 Tests por categoría:")
        for row in self.db.execute(query):
            print(f"  {row.nombre}: {row.num_tests} tests")
        
        # Verificar integridad
        query_integridad = text("""
            SELECT 
                COUNT(DISTINCT e.id) as tests_con_preguntas,
                COUNT(pe.id) as total_asignaciones
            FROM examenes e
            JOIN preguntas_examenes pe ON e.id = pe.examen_id
        """)
        
        integridad = self.db.execute(query_integridad).fetchone()
        print(f"\n✅ Tests con preguntas asignadas: {integridad.tests_con_preguntas}")
        print(f"✅ Total de asignaciones pregunta-test: {integridad.total_asignaciones}")
    
    def close(self):
        """Cierra la conexión a la base de datos"""
        self.db.close()

def main():
    """Función principal para generar todos los tests"""
    
    generador = GeneradorTestsAutomaticos()
    
    try:
        # Limpiar tests existentes
        generador.limpiar_tests_existentes()
        
        # Generar colección completa
        tests_creados = generador.generar_coleccion_completa_tests()
        
        # Mostrar estadísticas
        generador.mostrar_estadisticas_finales()
        
        print("\n🎉 ¡Generación de tests completada exitosamente!")
        print(f"🔗 Los tests están listos para ser utilizados en el frontend")
        
    except Exception as e:
        print(f"\n❌ Error durante la generación: {e}")
        raise
    finally:
        generador.close()

if __name__ == "__main__":
    main()