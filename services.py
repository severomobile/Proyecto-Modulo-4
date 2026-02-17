"""
Módulo de Servicios Externos - Proyecto GIC
Este módulo cumple con la integración de APIs para validación y notificaciones.
"""

import time
from logger import registrar_evento, registrar_error

class ServicioExternoError(Exception):
    """
    Excepción personalizada para capturar y tipificar errores específicos 
    que ocurran durante la comunicación con servicios fuera del sistema.
    """
    pass

def validar_identidad_api(id_cliente):
    """
    Simula la integración con una API de validación de identidad oficial.
    Este paso es un requisito de seguridad antes de persistir cualquier dato.
    """
    try:
        # Registro en log del inicio de la petición externa
        registrar_evento(f"Consultando API de identidad para ID: {id_cliente}...")
        
        # Simulación de latencia de red (tiempo de respuesta del servidor externo)
        time.sleep(0.5) 
        
        # Validación de integridad de los parámetros de entrada
        if not id_cliente:
            raise ServicioExternoError("ID de cliente vacío o nulo.")

        # Simulación de la respuesta lógica del servidor (suponemos éxito para este caso)
        es_valido = True 
        
        # Trazabilidad del resultado obtenido de la API
        registrar_evento(f"Resultado API Identidad: {'Válido' if es_valido else 'Inválido'}")
        return es_valido

    except Exception as e:
        # En caso de fallo de conexión o timeout, se registra el error y se escala la excepción
        registrar_error(f"Fallo en conexión con API de Identidad: {e}")
        raise ServicioExternoError(f"No se pudo validar la identidad: {e}")

def enviar_notificacion_bienvenida(cliente):
    """
    Simula el envío automatizado de correos electrónicos tras un registro exitoso.
    Utiliza el objeto 'cliente' para demostrar el paso de parámetros por referencia.
    """
    try:
        # Validación de pre-condición: el objeto debe tener un destino de correo válido
        if not cliente.email:
            raise ValueError("El cliente no tiene un email configurado.")

        registrar_evento(f"Intentando enviar email de bienvenida a: {cliente.email}")
        
        # Simulación de respuesta de una API REST de mensajería (ej. SendGrid o Mailchimp)
        time.sleep(0.3)
        
        # Registro del éxito de la operación con datos del objeto cliente
        log_exito = f"API NOTIFICACIÓN: Email enviado exitosamente a {cliente.nombre} ({cliente.email})"
        registrar_evento(log_exito)
        
        return True

    except Exception as e:
        # El fallo en notificaciones se registra pero no detiene el flujo principal del programa
        registrar_error(f"Error en servicio de notificaciones: {e}")
        return False