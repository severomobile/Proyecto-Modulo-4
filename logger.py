import logging

# Configuración global del motor de logging para el proyecto GIC.
# Esto garantiza el cumplimiento del requerimiento técnico de "Registro de actividad" 
# permitiendo auditar operaciones y fallos en un archivo físico persistente.
logging.basicConfig(
    filename='sistema_gic.log',       # Archivo donde se almacenará el historial
    level=logging.INFO,                # Nivel mínimo de severidad a registrar
    format='%(asctime)s - %(levelname)s - %(message)s', # Estructura del mensaje: Tiempo - Nivel - Contenido
    datefmt='%Y-%m-%d %H:%M:%S'        # Formato de fecha y hora legible
)

def registrar_evento(mensaje):
    """
    Registra sucesos informativos o flujos exitosos dentro de la aplicación.
    Se utiliza para el seguimiento de registros, actualizaciones y exportaciones.
    """
    logging.info(mensaje)

def registrar_error(mensaje):
    """
    Registra excepciones y fallos críticos en el archivo log.
    Es fundamental para el soporte técnico y la depuración del sistema en producción.
    """
    logging.error(mensaje)