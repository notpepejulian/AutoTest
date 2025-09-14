#!/usr/bin/env python3
"""
Script para insertar 1000 preguntas DGT en la base de datos AutoTest
Incluye generación de preguntas adicionales para completar 1000
"""

import sys
import random
from typing import List, Dict
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Importar el generador
from generar_preguntas_dgt import GeneradorPreguntasDGT

# Configuración directa de conexión
DATABASE_URL = "mysql+pymysql://nj17dssdsnj:zGmPTVYFkTQBUP2V7uizIfWjs5@localhost:3306/autotest_db"
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def generar_preguntas_adicionales(cantidad_necesaria: int) -> List[Dict]:
    """Genera preguntas adicionales para completar 1000"""
    
    preguntas_extras = [
        # Preguntas de verdadero/falso adicionales
        ("¿Es obligatorio usar el cinturón en taxis?", 
         ["Verdadero", "Falso"], 
         0, "Es obligatorio para todos los ocupantes. (Art. 117 RGC)"),
         
        ("¿Puede un ciclomotor circular por autopistas?", 
         ["Verdadero", "Falso"], 
         1, "Los ciclomotores no pueden circular por autopistas ni autovías."),
         
        ("¿Es válido el carné de conducir español en Francia?", 
         ["Verdadero", "Falso"], 
         0, "Es válido en todos los países de la Unión Europea."),
         
        ("¿Está prohibido adelantar a un ciclista en zona urbana?", 
         ["Verdadero", "Falso"], 
         1, "Se puede adelantar respetando la distancia de seguridad lateral."),
         
        ("¿Debe llevar rueda de repuesto obligatoriamente?", 
         ["Verdadero", "Falso"], 
         1, "No es obligatorio, pero sí recomendable."),
         
        # Preguntas de 3 opciones adicionales
        ("¿Cuál es la edad mínima para conducir un ciclomotor?", 
         ["14 años", "15 años", "16 años"], 
         1, "La edad mínima para ciclomotor es 15 años. (Art. 6 RGC)"),
         
        ("¿Cada cuánto debe revisar los frenos?", 
         ["Cada mes", "Según manual del fabricante", "Cada 6 meses"], 
         1, "Debe seguir las indicaciones del manual del fabricante."),
         
        ("¿Dónde debe mirar antes de abrir la puerta del vehículo?", 
         ["Hacia adelante", "Por el espejo retrovisor", "En todas las direcciones"], 
         2, "Debe comprobar en todas las direcciones antes de abrir."),
         
        ("¿Cuándo debe usar las luces de emergencia en ciudad?", 
         ["Nunca", "En situaciones de peligro", "Al aparcar"], 
         1, "En situaciones de peligro o cuando el vehículo constituya obstáculo."),
         
        ("¿Qué hacer si se queda sin combustible en autopista?", 
         ["Parar en el carril", "Parar en el arcén", "Continuar despacio"], 
         1, "Debe parar en el arcén derecho y señalizar correctamente."),
         
        ("¿Está permitido el uso de detectores de radar?", 
         ["Sí, siempre", "No", "Solo los pasivos"], 
         1, "Está prohibido el uso de detectores de radar."),
         
        ("¿Qué significa un panel naranja en un vehículo?", 
         ["Transporte de mercancías peligrosas", "Vehículo lento", "Transporte escolar"], 
         0, "Indica que transporta mercancías peligrosas."),
         
        ("¿Cuándo debe encender las luces de posición?", 
         ["Solo de noche", "Al anochecer y amanecer", "En túneles"], 
         1, "Durante el crepúsculo y cuando disminuye la visibilidad."),
         
        ("¿Qué tipo de vehículo tiene prioridad en una intersección?", 
         ["El más grande", "Los de emergencia", "El que llegue antes"], 
         1, "Los vehículos de emergencia en servicio tienen prioridad absoluta."),
         
        ("¿A qué distancia debe colocar la señal V-20 en travesías?", 
         ["30 metros", "50 metros", "100 metros"], 
         1, "En travesías debe colocarse a 50 metros como mínimo."),
         
        ("¿Cuándo debe cambiar el filtro del aceite?", 
         ["Cada cambio de aceite", "Cada dos cambios", "Una vez al año"], 
         0, "Se debe cambiar con cada cambio de aceite del motor."),
         
        ("¿Qué indica un testigo rojo en el cuadro de instrumentos?", 
         ["Aviso", "Peligro, parar inmediatamente", "Mantenimiento"], 
         1, "Un testigo rojo indica peligro y que debe parar inmediatamente."),
         
        ("¿Está permitido remolcar otro vehículo por autopista?", 
         ["Sí, siempre", "No", "Solo vehículos averiados"], 
         1, "Está prohibido remolcar por autopistas y autovías."),
         
        ("¿Dónde es obligatorio usar cadenas cuando está señalizado?", 
         ["Solo en neumáticos delanteros", "En las ruedas motrices", "En las cuatro ruedas"], 
         1, "Debe colocarlas en las ruedas motrices del vehículo."),
         
        ("¿Qué hacer ante un semáforo con flecha verde y roja?", 
         ["Parar", "Continuar en dirección de la flecha", "Esperar"], 
         1, "Puede continuar únicamente en la dirección de la flecha verde."),
         
        # Más preguntas variadas para completar
        ("¿Cuál es la presión recomendada para neumáticos de turismo?", 
         ["1,5 bar", "Según fabricante", "3 bar"], 
         1, "Debe seguir las recomendaciones específicas del fabricante del vehículo."),
         
        ("¿Qué hacer si llueve intensamente y no ve bien?", 
         ["Acelerar", "Parar en lugar seguro", "Encender emergencias"], 
         1, "Debe parar en un lugar seguro hasta que mejore la visibilidad."),
         
        ("¿Cada cuánto debe cambiar el líquido de frenos?", 
         ["Cada año", "Cada 2-4 años", "Nunca"], 
         1, "Debe cambiarse cada 2-4 años según especificaciones."),
         
        ("¿Qué significan las líneas amarillas en la calzada?", 
         ["Prohibición temporal", "Obras", "Zona de carga"], 
         0, "Indican una prohibición de carácter temporal."),
         
        ("¿Es obligatorio llevar extintor en vehículos particulares?", 
         ["Sí", "No", "Solo en furgonetas"], 
         1, "No es obligatorio en vehículos particulares."),
         
        ("¿Qué debe hacer al ver una ambulancia con sirena?", 
         ["Acelerar", "Facilitar el paso", "Parar"], 
         1, "Debe facilitar el paso y apartarse si es necesario."),
         
        ("¿Puede usar las luces antiniebla con lluvia?", 
         ["Sí, siempre", "Solo si reduce mucho la visibilidad", "No"], 
         1, "Solo cuando la lluvia reduzca considerablemente la visibilidad."),
         
        ("¿Cuánto tiempo puede aparcar en zona azul sin ticket?", 
         ["15 minutos", "No puede", "30 minutos"], 
         1, "No puede aparcar sin ticket en zona de estacionamiento regulado."),
         
        ("¿Qué hacer si se le enciende el testigo de aceite?", 
         ["Continuar despacio", "Parar inmediatamente", "Añadir aceite"], 
         1, "Debe parar inmediatamente para evitar daños al motor."),
         
        ("¿Es legal conducir con chanclas?", 
         ["Sí", "No", "Solo en verano"], 
         0, "No hay prohibición específica, pero debe asegurar un control adecuado."),
         
        ("¿Qué documento acredita la titularidad del vehículo?", 
         ["Permiso de circulación", "Tarjeta de inspección técnica", "Seguro"], 
         0, "El permiso de circulación acredita la titularidad del vehículo."),
         
        ("¿Cada cuánto debe pasar revisión un taxi?", 
         ["Cada año", "Cada 6 meses", "Cada 2 años"], 
         1, "Los vehículos de uso público pasan revisión cada 6 meses."),
         
        ("¿Qué significa la señal de 'Ceda el paso'?", 
         ["Parar siempre", "Ceder paso si viene alguien", "Reducir velocidad"], 
         1, "Debe ceder el paso a otros vehículos que tengan preferencia."),
         
        ("¿Puede girar a la derecha con semáforo en rojo?", 
         ["Sí, siempre", "No, nunca", "Solo si está permitido"], 
         2, "Solo cuando esté expresamente permitido por señalización."),
         
        ("¿Qué hacer si se pincha una rueda en autopista?", 
         ["Cambiarla en el carril", "Ir al arcén derecho", "Continuar despacio"], 
         1, "Debe dirigirse al arcén derecho y señalizar correctamente."),
         
        ("¿Cuándo debe usar luces de carretera?", 
         ["Siempre de noche", "Fuera de poblado sin alumbrado", "En autopistas"], 
         1, "En carreteras insuficientemente iluminadas y sin tráfico de frente."),
         
        ("¿Está permitido hablar por teléfono con manos libres?", 
         ["Sí", "No", "Solo llamadas cortas"], 
         0, "Está permitido usar dispositivos de manos libres."),
         
        ("¿Qué hacer ante un stop?", 
         ["Reducir velocidad", "Parar completamente", "Ceder el paso"], 
         1, "Debe realizar una parada completa antes de continuar."),
         
        ("¿Puede adelantar en un paso de peatones?", 
         ["Sí", "No", "Solo sin peatones"], 
         1, "Está prohibido adelantar en pasos de peatones."),
         
        ("¿Cuándo caduca el permiso de conducción temporal?", 
         ["Al mes", "A los 3 meses", "Al año"], 
         1, "El permiso temporal tiene validez de 3 meses."),
         
        ("¿Dónde debe situarse para girar a la izquierda?", 
         ["En el centro", "Lo más a la izquierda posible", "En cualquier carril"], 
         1, "Debe situarse lo más a la izquierda posible de su sentido de circulación."),
         
        ("¿Es obligatorio el uso de sistemas de navegación GPS?", 
         ["Sí", "No", "Solo en viajes largos"], 
         1, "No es obligatorio, aunque puede ser útil."),
         
        ("¿Qué hacer si el vehículo consume más combustible de lo normal?", 
         ["Revisar en taller", "Cambiar combustible", "Conducir más despacio"], 
         0, "Debe revisar el vehículo en un taller especializado."),
         
        ("¿Puede circular un vehículo sin ITV por ciudad?", 
         ["Sí, temporalmente", "No", "Solo para ir a la ITV"], 
         1, "No puede circular con la ITV caducada."),
         
        ("¿Cuál es la función del catalizador?", 
         ["Aumentar potencia", "Reducir contaminación", "Ahorrar combustible"], 
         1, "Reduce las emisiones contaminantes del escape."),
         
        ("¿Debe señalizar al salir de una rotonda?", 
         ["No", "Sí", "Solo si hay varios carriles"], 
         1, "Debe señalizar la salida de la rotonda."),
         
        ("¿Qué hacer ante hielo en la carretera?", 
         ["Acelerar", "Mantener velocidad constante y suave", "Frenar fuerte"], 
         1, "Mantener velocidad constante evitando movimientos bruscos."),
         
        ("¿Es legal llevar animales sueltos en el vehículo?", 
         ["Sí", "No", "Solo perros pequeños"], 
         1, "Los animales deben ir debidamente sujetos o separados."),
         
        ("¿Cuándo debe usar el intermitente?", 
         ["Solo para girar", "Para cambiar de carril y girar", "Solo en ciudad"], 
         1, "Para cualquier cambio de dirección o carril."),
         
        ("¿Puede estacionar delante de un vado?", 
         ["Sí", "No", "Solo temporalmente"], 
         1, "Está prohibido estacionar delante de vados señalizados."),
         
        ("¿Qué indica una marca vial blanca discontinua?", 
         ["Prohibido cruzar", "Se puede cruzar", "Solo para adelantar"], 
         1, "Indica que se puede cruzar con precaución."),
         
        ("¿Es obligatorio el cinturón en autobuses urbanos?", 
         ["Sí", "No", "Solo en autopistas"], 
         1, "No es obligatorio en autobuses urbanos."),
         
        ("¿Qué debe hacer si se avería el limpiaparabrisas?", 
         ["Continuar", "Parar si llueve", "Limpiar a mano"], 
         1, "Debe parar si las condiciones meteorológicas lo requieren."),
         
        ("¿Puede usar el teléfono móvil parado en un semáforo?", 
         ["Sí", "No", "Solo llamadas urgentes"], 
         1, "Está prohibido usar el móvil con el motor en marcha."),
         
        ("¿Cuándo debe revisar el nivel del líquido refrigerante?", 
         ["Solo en verano", "Regularmente", "Solo si se calienta"], 
         1, "Debe revisarse regularmente, especialmente antes del verano."),
         
        ("¿Está permitido adelantar por la derecha en autopistas?", 
         ["No", "Sí, en ciertas condiciones", "Solo a vehículos lentos"], 
         1, "Sí, cuando el tráfico circula en filas paralelas."),
         
        ("¿Qué hacer si no funciona el velocímetro?", 
         ["Estimar la velocidad", "No circular", "Ir despacio"], 
         1, "No debe circular hasta repararlo."),
         
        ("¿Es obligatorio llevar botiquín en vehículos particulares?", 
         ["Sí", "No", "Solo en viajes largos"], 
         1, "No es obligatorio en vehículos particulares."),
         
        ("¿Cuándo debe cambiar las escobillas del limpiaparabrisas?", 
         ["Cada año", "Cuando no limpien correctamente", "Cada 50.000 km"], 
         1, "Debe cambiarlas cuando no realicen su función correctamente."),
         
        ("¿Puede circular con el intermitente puesto permanentemente?", 
         ["Sí", "No", "Solo en averías"], 
         1, "No, puede confundir a otros conductores."),
         
        ("¿Qué documento debe llevar un conductor profesional?", 
         ["CAP", "Solo el permiso", "Certificado médico"], 
         0, "Debe llevar el Certificado de Aptitud Profesional (CAP)."),
         
        ("¿Está permitido circular sin camiseta?", 
         ["No", "Sí", "Solo en verano"], 
         1, "No hay prohibición específica sobre la vestimenta."),
         
        ("¿Cuándo debe usar las luces de niebla traseras?", 
         ["Con lluvia", "Solo con niebla densa", "De noche"], 
         1, "Solo cuando la niebla reduzca la visibilidad por debajo de 50 metros."),
         
        ("¿Puede aparcar en una plaza de minusválidos sin tarjeta?", 
         ["Sí, brevemente", "No", "Solo para cargar"], 
         1, "Está prohibido sin la tarjeta de estacionamiento correspondiente."),
         
        ("¿Qué hacer si se le rompe el acelerador?", 
         ["Usar freno de mano", "Parar con el freno de pie", "Quitar contacto"], 
         1, "Usar el freno de pie y parar en lugar seguro."),
         
        ("¿Es legal conducir con el brazo escayolado?", 
         ["Sí", "No", "Con adaptaciones"], 
         2, "Solo con las adaptaciones necesarias en el vehículo."),
         
        ("¿Cuándo debe comprobar la profundidad de los neumáticos?", 
         ["En cada viaje", "Regularmente", "Solo en la ITV"], 
         1, "Debe comprobarse regularmente y antes de viajes largos."),
         
        ("¿Puede adelantar a un vehículo que va a girar a la izquierda?", 
         ["No", "Sí, por la derecha", "Solo en ciudad"], 
         1, "Puede adelantarlo por la derecha con precaución."),
         
        ("¿Está permitido circular descalzo?", 
         ["No", "Sí", "Solo en verano"], 
         1, "No hay prohibición específica, pero debe asegurar el control."),
         
        ("¿Qué hacer si falla la dirección asistida?", 
         ["Continuar con cuidado", "Parar inmediatamente", "Ir al taller"], 
         2, "Dirigirse al taller más próximo, la dirección se vuelve más dura."),
         
        ("¿Cuándo debe usar el claxon?", 
         ["Para saludar", "Solo en caso de peligro", "En adelantamientos"], 
         1, "Solo para avisar de su presencia en caso de peligro."),
         
        ("¿Puede transportar niños en el asiento delantero?", 
         ["No", "Sí, con sistema de retención", "Solo mayores de 10 años"], 
         1, "Sí, utilizando el sistema de retención adecuado."),
         
        ("¿Está permitido fumar en un vehículo con menores?", 
         ["Sí", "No", "Solo con ventanillas abiertas"], 
         1, "Está prohibido fumar en vehículos con menores de edad."),
         
        ("¿Qué hacer ante una señal de obras en la carretera?", 
         ["Acelerar para pasar rápido", "Reducir velocidad y extremar precaución", "Parar"], 
         1, "Reducir velocidad y extremar las precauciones."),
         
        ("¿Cuándo debe renovar el carnet de conducir un conductor de 50 años?", 
         ["Cada 5 años", "Cada 10 años", "Cada 15 años"], 
         1, "Hasta los 65 años se renueva cada 10 años."),
         
        ("¿Puede adelantar en una pendiente pronunciada?", 
         ["No", "Sí, con precaución", "Solo cuesta abajo"], 
         1, "Sí, si tiene suficiente visibilidad y potencia."),
         
        ("¿Es obligatorio encender las luces en túneles?", 
         ["Solo los largos", "Sí, siempre", "Solo si están mal iluminados"], 
         1, "Es obligatorio encender las luces en todos los túneles."),
         
        ("¿Qué hacer si se queda sin batería?", 
         ["Arrancar empujando", "Usar cables de arranque", "Llamar asistencia"], 
         1, "Usar cables de arranque o llamar asistencia en carretera."),
         
        ("¿Puede circular un ciclomotor por el arcén?", 
         ["Sí", "No", "Solo si no molesta"], 
         1, "Los ciclomotores deben circular por la calzada, no por el arcén."),
         
        ("¿Cuándo debe usar las luces de emergencia?", 
         ["Al aparcar", "En situaciones de peligro", "De noche"], 
         1, "En situaciones de peligro, avería o cuando constituya obstáculo."),
         
        ("¿Es legal llevar el móvil en el salpicadero mientras conduce?", 
         ["Sí", "No", "Solo si no lo toca"], 
         2, "Sí, siempre que no lo manipule durante la conducción."),
         
        ("¿Qué significa una señal octogonal?", 
         ["Prohibición", "Stop", "Ceda el paso"], 
         1, "La señal octogonal es exclusivamente la señal de STOP."),
         
        ("¿Puede estacionar en una parada de autobús fuera de horario?", 
         ["Sí", "No", "Solo por la noche"], 
         1, "Está prohibido estacionar en paradas de transporte público."),
         
        ("¿Cuándo debe cambiar el filtro de combustible?", 
         ["Cada año", "Según manual del fabricante", "Cada 100.000 km"], 
         1, "Debe seguir las indicaciones del manual del fabricante."),
         
        ("¿Puede girar a la izquierda desde el carril derecho?", 
         ["Sí", "No", "Solo en ciudad"], 
         1, "No, debe situarse en el carril correspondiente."),
         
        ("¿Es obligatorio llevar herramientas en el vehículo?", 
         ["Sí", "No", "Solo llave de ruedas"], 
         1, "No es obligatorio, pero es recomendable."),
         
        ("¿Qué hacer si ve un vehículo circulando en sentido contrario?", 
         ["Acelerar", "Apartarse y avisar", "Tocar el claxon"], 
         1, "Apartarse del camino y avisar al 112 si es posible."),
         
        ("¿Puede usar auriculares mientras conduce?", 
         ["Sí", "No", "Solo uno"], 
         1, "Está prohibido usar auriculares que impidan oír el exterior."),
         
        ("¿Cuándo debe revisar la alineación de las ruedas?", 
         ["Cada año", "Si nota vibraciones o desgaste irregular", "Cada 50.000 km"], 
         1, "Cuando note vibraciones o desgaste irregular en los neumáticos."),
         
        ("¿Puede adelantar en un túnel?", 
         ["Sí", "No", "Solo si es largo"], 
         1, "Está prohibido adelantar en túneles."),
         
        ("¿Es obligatorio el uso de gafas de sol al conducir?", 
         ["Sí, siempre", "No", "Solo con mucho sol"], 
         1, "No es obligatorio, pero recomendable con mucha luminosidad."),
         
        ("¿Qué hacer si encuentra un animal muerto en la carretera?", 
         ["Quitarlo", "Avisar a las autoridades", "Rodearlo"], 
         1, "Avisar a las autoridades competentes para que lo retiren."),
         
        ("¿Puede circular con una rueda de repuesto pequeña por autopista?", 
         ["Sí", "No", "Solo a baja velocidad"], 
         2, "Solo a la velocidad máxima indicada en la rueda (normalmente 80 km/h)."),
         
        ("¿Cuándo debe cambiar las bujías?", 
         ["Cada año", "Según manual del fabricante", "Cada 10.000 km"], 
         1, "Debe seguir las recomendaciones del manual del fabricante."),
         
        ("¿Está permitido adelantar a un vehículo de emergencia?", 
         ["Sí", "No", "Solo si no lleva sirena"], 
         1, "No se debe adelantar a vehículos de emergencia en servicio."),
         
        ("¿Puede usar las luces antiniebla delanteras con lluvia?", 
         ["Sí", "No", "Solo si llueve mucho"], 
         2, "Solo cuando la lluvia sea muy intensa y reduzca la visibilidad."),
         
        ("¿Es obligatorio parar ante un autobús escolar parado?", 
         ["No", "Sí", "Solo en ciudad"], 
         1, "Debe extremar la precaución y reducir la velocidad."),
         
        ("¿Puede estacionar en pendiente sin poner el freno de mano?", 
         ["Sí", "No", "Solo en pendientes suaves"], 
         1, "Siempre debe poner el freno de mano al estacionar."),
         
        ("¿Cuándo debe usar el espejo retrovisor interior antideslumbrante?", 
         ["Solo de día", "Con luces de otros vehículos molestas", "Nunca"], 
         1, "Cuando las luces de otros vehículos molesten o deslumbren."),
         
        ("¿Puede transportar gasolina en bidones en el maletero?", 
         ["Sí", "No", "Solo pequeñas cantidades"], 
         1, "Está prohibido transportar combustible en recipientes."),
         
        ("¿Es legal conducir con flipflops?", 
         ["No", "Sí", "Solo en ciudad"], 
         1, "No hay prohibición específica, pero debe asegurar el control pedales."),
         
        ("¿Qué hacer si se le empañan los cristales?", 
         ["Limpiar con la mano", "Usar el sistema de ventilación", "Parar"], 
         1, "Usar el sistema de calefacción y ventilación del vehículo."),
         
        ("¿Puede adelantar a varios vehículos a la vez?", 
         ["No", "Sí, si hay visibilidad suficiente", "Solo en autopistas"], 
         1, "Sí, si tiene visibilidad y espacio suficiente para hacerlo con seguridad."),
         
        ("¿Es obligatorio llevar agua en el vehículo?", 
         ["Sí", "No", "Solo en verano"], 
         1, "No es obligatorio, pero es recomendable en viajes largos."),
         
        ("¿Cuándo debe usar las luces de posición?", 
         ["Solo parado", "Durante el crepúsculo", "Nunca"], 
         1, "Durante el crepúsculo y cuando esté estacionado en vías insuficientemente iluminadas."),
         
        ("¿Puede circular sin el tapacubos?", 
         ["No", "Sí", "Solo temporalmente"], 
         1, "Sí, los tapacubos son elementos estéticos, no obligatorios."),
         
        ("¿Qué hacer si se le cae algo al suelo mientras conduce?", 
         ["Recogerlo rápidamente", "Parar para recogerlo", "Dejarlo hasta parar"], 
         2, "No debe distraerse, dejarlo hasta poder parar con seguridad."),
         
        ("¿Es obligatorio el uso de neumáticos de invierno?", 
         ["Sí", "No, salvo señalización", "Solo en montaña"], 
         1, "No es obligatorio salvo señalización específica."),
         
        ("¿Puede adelantar por el arcén?", 
         ["Sí", "No", "Solo a ciclistas"], 
         1, "Está prohibido circular y adelantar por el arcén."),
         
        ("¿Cuándo debe comprobar la presión de los neumáticos?", 
         ["En caliente", "En frío", "Da igual"], 
         1, "Debe comprobarse en frío para obtener una medida exacta."),
         
        ("¿Puede usar el teléfono con el sistema de manos libres del vehículo?", 
         ["Sí", "No", "Solo llamadas cortas"], 
         0, "Sí, está permitido usar sistemas integrados de manos libres."),
         
        ("¿Es legal adelantar a un vehículo lento por la derecha en carretera?", 
         ["Sí", "No", "Solo si va muy lento"], 
         1, "No está permitido adelantar por la derecha en carreteras convencionales."),
         
        ("¿Qué hacer si se le avería el cuenta kilómetros?", 
         ["No circular", "Circular con precaución", "Reparar cuanto antes"], 
         2, "Puede circular pero debe repararlo cuanto antes."),
         
        ("¿Puede llevar animales en el asiento delantero?", 
         ["Sí", "No", "Solo perros pequeños"], 
         1, "No deben ir en el asiento delantero por seguridad."),
         
        ("¿Es obligatorio que funcione el claxon?", 
         ["Sí", "No", "Solo en ciudad"], 
         0, "Sí, es un elemento de seguridad obligatorio."),
         
        ("¿Cuándo debe usar las luces de cruce en ciudad?", 
         ["Nunca", "Entre el ocaso y la aurora", "Solo si llueve"], 
         1, "Entre la puesta y salida del sol y cuando sea necesario."),
         
        ("¿Puede estacionar delante de su propio garaje?", 
         ["Sí", "No", "Solo si no molesta"], 
         1, "No puede bloquear el acceso aunque sea su propio garaje."),
         
        ("¿Es necesario llevar documentación del seguro en el vehículo?", 
         ["Sí", "No", "Solo la póliza"], 
         0, "Sí, debe llevar el certificado del seguro obligatorio."),
         
        ("¿Puede circular con el cristal trasero roto?", 
         ["Sí", "No", "Solo si no impide la visión"], 
         1, "No puede circular con cristales de seguridad rotos."),
         
        ("¿Cuándo debe cambiar el filtro del aire acondicionado?", 
         ["Cada año", "Según manual", "Cuando huela mal"], 
         1, "Debe seguir las recomendaciones del manual de mantenimiento."),
         
        ("¿Puede adelantar en una intersección?", 
         ["Sí", "No", "Solo sin semáforos"], 
         1, "Está prohibido adelantar en intersecciones."),
         
        ("¿Es legal conducir con el brazo fuera de la ventanilla?", 
         ["Sí", "No", "Solo en verano"], 
         1, "No es recomendable por seguridad, aunque no esté prohibido específicamente."),
         
        ("¿Qué hacer si se le rompe el espejo retrovisor?", 
         ["Continuar", "Repararlo inmediatamente", "Usar solo espejos laterales"], 
         1, "Debe repararlo lo antes posible, es obligatorio tener espejos funcionales."),
         
        ("¿Puede transportar mascotas sin transportín?", 
         ["Sí", "No", "Solo atadas"], 
         1, "Deben ir en transportín o con sistemas que impidan que molesten al conductor."),
         
        ("¿Es obligatorio el cinturón de seguridad en vehículos de más de 3,5 toneladas?", 
         ["No", "Sí", "Solo en autopistas"], 
         1, "Sí, es obligatorio en todos los vehículos que lo lleven instalado."),
         
        ("¿Cuándo debe cambiar los amortiguadores?", 
         ["Cada 80.000 km", "Cuando no funcionen correctamente", "Cada 5 años"], 
         1, "Cuando no funcionen correctamente o presenten desgaste."),
         
        ("¿Puede usar luces de cruce y antiniebla a la vez?", 
         ["Sí", "No", "Solo con niebla muy densa"], 
         0, "Sí, pueden usarse simultáneamente cuando sea necesario."),
         
        ("¿Es legal conducir con gafas de sol por la noche?", 
         ["Sí", "No", "Solo si no reduce la visión"], 
         1, "No, pueden reducir peligrosamente la visión nocturna."),
         
        ("¿Qué hacer si ve humo saliendo del motor?", 
         ["Continuar despacio", "Parar inmediatamente", "Acelerar para ventilarlo"], 
         1, "Parar inmediatamente y apagar el motor."),
         
        ("¿Puede estacionar en una calle de sentido único en contra dirección?", 
         ["Sí", "No", "Solo por la noche"], 
         1, "No puede estacionar en contra de la dirección de circulación."),
         
        ("¿Es necesario que funcione el velocímetro?", 
         ["Sí", "No", "Solo en autopistas"], 
         0, "Sí, es obligatorio que el velocímetro funcione correctamente."),
         
        ("¿Cuándo debe usar el intermitente de emergencia?", 
         ["Al aparcar", "En situaciones de peligro", "En retenciones"], 
         1, "En situaciones de peligro, avería o cuando el vehículo pueda constituir un obstáculo."),
         
        ("¿Puede adelantar a un vehículo que circula a la velocidad máxima permitida?", 
         ["No", "Sí, si no supera el límite", "Solo en autopistas"], 
         0, "Sí, siempre que no supere el límite de velocidad establecido."),
         
        ("¿Es obligatorio llevar rueda de repuesto en motocicletas?", 
         ["Sí", "No", "Solo en viajes largos"], 
         1, "No es obligatorio en motocicletas."),
         
        ("¿Qué hacer si se le funde una luz durante la conducción nocturna?", 
         ["Continuar", "Parar en lugar seguro", "Encender emergencias"], 
         1, "Parar en lugar seguro y sustituir la bombilla si es posible."),
         
        ("¿Puede circular por un carril bici con el vehículo?", 
         ["Sí, despacio", "No", "Solo para aparcar"], 
         1, "Está prohibido circular por carriles bici con vehículos a motor."),
         
        ("¿Es legal llevar objetos sueltos en el salpicadero?", 
         ["Sí", "No", "Solo objetos pequeños"], 
         1, "No es recomendable, pueden convertirse en proyectiles en caso de frenazo."),
         
        ("¿Cuándo debe sustituir el líquido limpiaparabrisas?", 
         ["Cada año", "Cuando se agote", "Cada cambio de aceite"], 
         1, "Cuando se agote o esté contaminado."),
         
        ("¿Puede adelantar en un paso a nivel?", 
         ["Sí", "No", "Solo si no viene el tren"], 
         1, "Está prohibido adelantar en pasos a nivel."),
         
        ("¿Es obligatorio tener seguro a terceros en ciclomotores?", 
         ["Sí", "No", "Solo mayores de 50cc"], 
         0, "Sí, es obligatorio el seguro de responsabilidad civil."),
         
        ("¿Qué hacer si se le avería el intermitente?", 
         ["Usar señales con la mano", "No circular", "Repararlo cuanto antes"], 
         2, "Debe repararlo cuanto antes y puede usar señales manuales temporalmente."),
         
        ("¿Puede estacionar en una plaza de carga y descarga por la noche?", 
         ["Sí", "No", "Solo los sábados"], 
         0, "Generalmente sí, fuera de las horas de restricción indicadas."),
         
        ("¿Es legal usar el móvil parado en un atasco?", 
         ["Sí", "No", "Solo llamadas urgentes"], 
         1, "No, está prohibido usar el móvil con el motor en marcha."),
         
        ("¿Cuándo debe revisar el estado de la batería?", 
         ["Solo en invierno", "Regularmente", "Solo si no arranca"], 
         1, "Debe revisarse regularmente, especialmente antes del invierno."),
         
        ("¿Puede adelantar a un ciclista dejando menos de 1,5 metros?", 
         ["Sí", "No", "Solo en ciudad"], 
         1, "Debe mantener al menos 1,5 metros de separación lateral."),
         
        ("¿Es obligatorio que funcione la radio del vehículo?", 
         ["Sí", "No", "Solo la de emergencias"], 
         1, "No es obligatorio, la radio es un elemento de confort."),
         
        ("¿Qué hacer si se le calienta el motor en un atasco?", 
         ["Acelerar", "Apagar aire acondicionado", "Salir del atasco"], 
         1, "Apagar el aire acondicionado y si es necesario parar el motor."),
         
        ("¿Puede estacionar en batería en una vía de un solo sentido?", 
         ["No", "Sí, si está permitido", "Solo por la noche"], 
         1, "Sí, cuando esté permitido por la señalización."),
         
        ("¿Es necesario llevar el manual del vehículo?", 
         ["Sí", "No", "Solo en viajes largos"], 
         1, "No es obligatorio, pero es recomendable."),
         
        ("¿Cuándo debe cambiar las pastillas de freno?", 
         ["Cada año", "Cuando estén gastadas", "Cada 50.000 km"], 
         1, "Cuando estén gastadas o no frenen correctamente."),
         
        ("¿Puede usar las luces antiniebla traseras con lluvia?", 
         ["Sí", "No", "Solo si llueve mucho"], 
         1, "No, solo deben usarse con niebla densa."),
         
        ("¿Es legal conducir en calcetines?", 
         ["No", "Sí", "Solo en invierno"], 
         1, "No hay prohibición específica, pero debe asegurar el control de los pedales."),
         
        ("¿Qué hacer si se le avería el sistema de dirección?", 
         ["Continuar despacio", "Parar inmediatamente", "Ir al taller"], 
         1, "Parar inmediatamente en lugar seguro."),
         
        ("¿Puede transportar bicicletas en el techo del vehículo?", 
         ["No", "Sí, con el soporte adecuado", "Solo plegadas"], 
         1, "Sí, utilizando sistemas homologados para tal fin."),
         
        ("¿Es obligatorio el uso de casco en bicicleta?", 
         ["Sí", "No, salvo menores en vías interurbanas", "Solo en montaña"], 
         1, "No es obligatorio salvo para menores en vías interurbanas."),
    ]
    
    # Seleccionar aleatoriamente la cantidad necesaria
    return random.sample(preguntas_extras, min(cantidad_necesaria, len(preguntas_extras)))

def insertar_pregunta_en_bd(pregunta: Dict, db_session):
    """Inserta una pregunta individual en la base de datos"""
    
    try:
        # Insertar la pregunta
        query_pregunta = text("""
            INSERT INTO preguntas (texto_pregunta, explicacion, categoria_id, dificultad, es_activa) 
            VALUES (:texto_pregunta, :explicacion, :categoria_id, :dificultad, :es_activa)
        """)
        
        result = db_session.execute(query_pregunta, {
            'texto_pregunta': pregunta['enunciado'],
            'explicacion': pregunta['explicacion'],
            'categoria_id': pregunta['categoria_id'],
            'dificultad': pregunta['dificultad'],
            'es_activa': True
        })
        
        pregunta_id = result.lastrowid
        
        # Insertar las respuestas
        for i, opcion in enumerate(pregunta['opciones']):
            query_respuesta = text("""
                INSERT INTO respuestas (pregunta_id, texto_respuesta, es_correcta, orden_respuesta) 
                VALUES (:pregunta_id, :texto_respuesta, :es_correcta, :orden_respuesta)
            """)
            
            db_session.execute(query_respuesta, {
                'pregunta_id': pregunta_id,
                'texto_respuesta': opcion,
                'es_correcta': i == pregunta['correcta'],
                'orden_respuesta': i + 1
            })
        
        return pregunta_id
        
    except Exception as e:
        print(f"❌ Error insertando pregunta: {pregunta['enunciado'][:50]}... - {e}")
        return None

def insertar_todas_las_preguntas():
    """Función principal para insertar las 1000 preguntas"""
    
    print("🚀 INSERCIÓN MASIVA DE PREGUNTAS DGT")
    print("=" * 50)
    print("📊 Generando banco completo de 1000 preguntas...")
    
    # Generar preguntas con el generador DGT
    generador = GeneradorPreguntasDGT()
    preguntas = generador.generar_todas_las_preguntas()
    
    # Añadir preguntas verdadero/falso
    generador.crear_preguntas_verdadero_falso(100)
    
    # Calcular cuántas preguntas adicionales necesitamos
    preguntas_actuales = len(generador.preguntas)
    print(f"📋 Preguntas generadas inicialmente: {preguntas_actuales}")
    
    if preguntas_actuales < 1000:
        adicionales_necesarias = 1000 - preguntas_actuales
        print(f"🔄 Generando {adicionales_necesarias} preguntas adicionales...")
        
        preguntas_adicionales = generar_preguntas_adicionales(adicionales_necesarias)
        
        # Añadir las preguntas adicionales al generador
        for pregunta_extra in preguntas_adicionales:
            generador.agregar_pregunta(
                pregunta_extra[0], 
                pregunta_extra[1], 
                pregunta_extra[2], 
                pregunta_extra[3], 
                categoria_id=5  # Asignar a "Test de examen"
            )
    
    total_preguntas = len(generador.preguntas)
    print(f"✅ Total de preguntas preparadas: {total_preguntas}")
    
    # Insertar en la base de datos
    db = SessionLocal()
    try:
        insertadas = 0
        errores = 0
        
        print("\n🔄 Insertando preguntas en la base de datos...")
        
        for i, pregunta in enumerate(generador.preguntas):
            if i % 50 == 0:
                print(f"  📝 Procesando pregunta {i+1}/{total_preguntas}...")
            
            pregunta_id = insertar_pregunta_en_bd(pregunta, db)
            
            if pregunta_id:
                insertadas += 1
            else:
                errores += 1
        
        # Confirmar cambios
        db.commit()
        
        print(f"\n✅ INSERCIÓN COMPLETADA:")
        print(f"  📝 Preguntas insertadas: {insertadas}")
        print(f"  ❌ Errores: {errores}")
        print(f"  📊 Tasa de éxito: {(insertadas*100/total_preguntas):.1f}%")
        
        # Estadísticas finales
        query_stats = text("""
            SELECT COUNT(*) as total FROM preguntas;
        """)
        
        total_bd = db.execute(query_stats).fetchone()
        print(f"  🎯 Total en base de datos: {total_bd.total} preguntas")
        
    except Exception as e:
        print(f"❌ Error durante la inserción: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    insertar_todas_las_preguntas()
    print("\n🎉 Proceso completado exitosamente")