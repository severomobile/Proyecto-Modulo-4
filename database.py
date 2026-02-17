import sqlite3
import json
import csv
import os
from logger import registrar_evento, registrar_error

class DatabaseManager:
    """Clase responsable de la persistencia de datos en SQLite y backups externos."""
    
    def __init__(self, db_name="solution_tech.db"):
        self.db_name = db_name
        self.crear_tabla()

    def crear_tabla(self):
        """Crea la estructura de la tabla y aplica migraciones de columnas si es necesario."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                # Inicialización de la tabla base con campos de negocio
                cursor.execute('''CREATE TABLE IF NOT EXISTS clientes 
                                 (id TEXT PRIMARY KEY, nombre TEXT, email TEXT, 
                                  tipo TEXT, extra TEXT)''')
                
                # Proceso de migración para asegurar la existencia de la columna 'telefono'
                cursor.execute("PRAGMA table_info(clientes)")
                columnas = [col[1] for col in cursor.fetchall()]
                
                if 'telefono' not in columnas:
                    cursor.execute("ALTER TABLE clientes ADD COLUMN telefono TEXT DEFAULT 'Sin Teléfono'")
                
                conn.commit()
        except sqlite3.Error as e:
            registrar_error(f"Error en la migración de DB: {e}")

    def eliminar_cliente_db(self, id_cliente):
        """Elimina un registro de la base de datos basándose en su ID único."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM clientes WHERE id = ?", (id_cliente,))
                conn.commit()
                if cursor.rowcount > 0:
                    registrar_evento(f"ID {id_cliente} eliminado de la base de datos.")
                    return True
                return False
        except sqlite3.Error as e:
            registrar_error(f"Error al eliminar: {e}")
            return False

    def guardar_cliente(self, cliente):
        """Persiste un objeto cliente extrayendo datos específicos mediante inspección de atributos."""
        try:
            # Determinamos el dato extra según la subclase (Premium o Corporativo)
            extra = ""
            if hasattr(cliente, 'descuento'): extra = f"Descuento: {cliente.descuento}%"
            elif hasattr(cliente, 'empresa'): extra = f"Empresa: {cliente.empresa}"
            
            # Identificamos el tipo de cliente por el nombre de su clase
            tipo_nombre = type(cliente).__name__

            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                # Inserción parametrizada para evitar inyección SQL
                cursor.execute("INSERT INTO clientes (id, nombre, email, telefono, tipo, extra) VALUES (?, ?, ?, ?, ?, ?)",
                               (cliente.id_cliente, cliente.nombre, cliente.email, cliente.telefono, tipo_nombre, extra))
                conn.commit()
            
            registrar_evento(f"Cliente {cliente.id_cliente} ({tipo_nombre}) guardado exitosamente.")
        except sqlite3.IntegrityError:
            registrar_error(f"Intento de duplicación de ID: {cliente.id_cliente}")
            raise ValueError("El ID del cliente ya existe en el sistema.")
        except Exception as e:
            registrar_error(f"Error inesperado al guardar: {e}")
            raise

    def actualizar_cliente(self, cliente):
        """Actualiza la información de un registro existente utilizando el ID como referencia."""
        try:
            extra = ""
            if hasattr(cliente, 'descuento'): extra = f"Descuento: {cliente.descuento}%"
            elif hasattr(cliente, 'empresa'): extra = f"Empresa: {cliente.empresa}"
            
            tipo_nombre = type(cliente).__name__

            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("""UPDATE clientes 
                                  SET nombre = ?, email = ?, telefono = ?, tipo = ?, extra = ? 
                                  WHERE id = ?""",
                               (cliente.nombre, cliente.email, cliente.telefono, tipo_nombre, extra, cliente.id_cliente))
                conn.commit()
            
            registrar_evento(f"Cliente {cliente.id_cliente} actualizado correctamente.")
            return True
        except Exception as e:
            registrar_error(f"Error al actualizar cliente {cliente.id_cliente}: {e}")
            raise

    def obtener_todos(self):
        """Recupera todos los registros de la tabla para alimentar la vista de la aplicación."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, nombre, email, telefono, tipo, extra FROM clientes")
                return cursor.fetchall()
        except sqlite3.Error as e:
            registrar_error(f"Error al consultar: {e}")
            return []

    def exportar_datos(self):
        """Implementa la exportación masiva de datos a archivos planos JSON y CSV."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                conn.row_factory = sqlite3.Row  # Permite acceso por nombre de columna
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM clientes")
                filas = [dict(row) for row in cursor.fetchall()]

            if not filas:
                registrar_evento("Exportación cancelada: No hay datos para exportar.")
                return

            # Generación de archivo JSON para interoperabilidad
            with open("clientes_backup.json", "w", encoding='utf-8') as f:
                json.dump(filas, f, indent=4, ensure_ascii=False)
            
            # Generación de archivo CSV para compatibilidad con hojas de cálculo
            keys = filas[0].keys()
            with open("clientes_backup.csv", "w", newline='', encoding='utf-8') as f:
                dict_writer = csv.DictWriter(f, fieldnames=keys)
                dict_writer.writeheader()
                dict_writer.writerows(filas)
                
            registrar_evento("Backup exportado correctamente en formatos JSON y CSV.")
        except Exception as e:
            registrar_error(f"Fallo en la exportación de datos: {e}")