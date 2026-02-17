import unittest
import os
import gc
from models import Cliente, ClientePremium, ClienteRegular
from database import DatabaseManager

class TestSistemaGIC(unittest.TestCase):
    """
    Suite de pruebas unitarias para validar la integridad de la lógica de negocio, 
    la persistencia y el comportamiento polimórfico del sistema.
    """
    
    def setUp(self):
        """
        Configuración del entorno de pruebas. 
        Crea una base de datos temporal para no afectar los datos de producción.
        """
        self.db_test = "test_temp.db"
        self.manager = DatabaseManager(self.db_test)
        self.email_valido = "tester@solutiontech.com"
        self.tel_valido = "12345678"

    def tearDown(self):
        """
        Limpieza post-ejecución. 
        Libera recursos y elimina el archivo de base de datos temporal.
        """
        self.manager = None 
        gc.collect() # Fuerza la recolección de basura para liberar el archivo DB en Windows
        
        if os.path.exists(self.db_test):
            try:
                os.remove(self.db_test)
            except (PermissionError, OSError):
                pass

    def test_validaciones_avanzadas(self):
        """Valida que los setters de la clase Cliente disparen excepciones ante datos inválidos."""
        # Prueba de formato de email incorrecto
        with self.assertRaises(ValueError):
            Cliente("1", "Prueba", "email_incorrecto", self.tel_valido)
        
        # Prueba de teléfono con longitud insuficiente
        with self.assertRaises(ValueError):
            Cliente("2", "Prueba", self.email_valido, "123")

    def test_polimorfismo_y_herencia(self):
        """Verifica que las subclases mantengan la herencia y el comportamiento polimórfico."""
        premium = ClientePremium("P01", "Ana VIP", self.email_valido, self.tel_valido, descuento=25)
        # Comprueba que el atributo específico se asigne correctamente
        self.assertEqual(premium.descuento, 25)
        # Comprueba que el método sobrescrito responda según su clase (Polimorfismo)
        self.assertIn("25%", premium.obtener_beneficio())
        # Comprueba la relación de herencia
        self.assertTrue(isinstance(premium, Cliente))

    def test_persistencia_y_duplicados(self):
        """Valida la inserción en la DB y el manejo de restricciones de unicidad (Primary Key)."""
        cliente1 = ClienteRegular("ID_UNICO", "Juan Perez", self.email_valido, self.tel_valido)
        self.manager.guardar_cliente(cliente1)
        
        # Intento de guardar un cliente con un ID que ya existe
        cliente2 = ClienteRegular("ID_UNICO", "Otro Nombre", self.email_valido, self.tel_valido)
        with self.assertRaises(ValueError) as context:
            self.manager.guardar_cliente(cliente2)
        
        self.assertIn("ya existe", str(context.exception))

    def test_actualizacion_cliente(self):
        """Prueba que los cambios en un objeto se reflejen correctamente en la DB mediante UPDATE."""
        # 1. Registro inicial
        id_test = "ACT-01"
        cliente = ClienteRegular(id_test, "Original", self.email_valido, self.tel_valido)
        self.manager.guardar_cliente(cliente)

        # 2. Modificación de atributos
        nuevo_nombre = "Editado"
        cliente_editado = ClienteRegular(id_test, nuevo_nombre, self.email_valido, "99999999")
        
        # 3. Ejecución de la lógica de actualización en el gestor de base de datos
        resultado = self.manager.actualizar_cliente(cliente_editado)
        self.assertTrue(resultado)

        # 4. Verificación de integridad: el dato en la DB debe coincidir con el cambio
        todos = self.manager.obtener_todos()
        registro_db = next(row for row in todos if row[0] == id_test)
        self.assertEqual(registro_db[1], nuevo_nombre)

    def test_metodo_especial_eq(self):
        """Valida la sobrescritura del método __eq__ para comparar objetos por identidad de negocio."""
        c1 = ClienteRegular("ID_123", "Jose", self.email_valido, self.tel_valido)
        c2 = ClienteRegular("ID_123", "Jose Distinto", self.email_valido, self.tel_valido)
        # Deben ser considerados iguales por tener el mismo ID, a pesar de tener nombres distintos
        self.assertEqual(c1, c2)

if __name__ == "__main__":
    unittest.main()