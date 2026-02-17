import tkinter as tk
from gui import GIC_App
from database import DatabaseManager
from logger import registrar_evento, registrar_error

def iniciar_sistema():
    """Función principal para orquestar el arranque del Gestor Inteligente de Clientes."""
    try:
        # Registro de inicio de sesión en el log (Requerimiento de auditoría) 
        registrar_evento("Iniciando el sistema GIC - Solution Tech...")

        # Inicialización de persistencia (SQLite)
        # Se asegura que las tablas existan antes de cargar la interfaz
        db = DatabaseManager()
        
        # Configuración de la ventana principal (GUI)
        root = tk.Tk()
        root.geometry("600x500") # Dimensiones sugeridas para visualización fluida
        
        # Carga de la lógica de negocio y componentes visuales
        app = GIC_App(root)
        
        registrar_evento("Interfaz gráfica cargada exitosamente. Sistema listo para operar.")
        
        # Ejecución del bucle principal
        root.mainloop()

    except Exception as e:
        # Manejo de errores estructurado para el arranque
        error_msg = f"Error crítico durante el arranque del sistema: {e}"
        registrar_error(error_msg)
        print(error_msg) # Salida por consola para soporte técnico

if __name__ == "__main__":
    iniciar_sistema()