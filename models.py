import re

class Cliente:
    """Clase base que define la estructura principal de un cliente y sus validaciones."""
    
    def __init__(self, id_cliente, nombre, email, telefono):
        self.id_cliente = id_cliente
        self.nombre = nombre
        # El setter de email y telefono se activa aquí para validar desde la creación
        self.email = email  
        self.telefono = telefono

    @property
    def email(self):
        """Getter para acceder al email de forma controlada."""
        return self.__email

    @email.setter
    def email(self, valor):
        """Valida que el email tenga un formato estándar (usuario@dominio.com)."""
        patron = r"[^@]+@[^@]+\.[^@]+"
        if not re.match(patron, valor):
            raise ValueError(f"Formato de email inválido: {valor}")
        self.__email = valor

    @property
    def telefono(self):
        """Getter para el atributo privado del teléfono."""
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        """Asegura que el teléfono contenga solo números y tenga una longitud mínima."""
        if not str(valor).isdigit() or len(str(valor)) < 7:
            raise ValueError(f"Número de teléfono inválido. Debe ser numérico y mayor a 7 dígitos.")
        self.__telefono = valor

    def obtener_beneficio(self):
        """Método base para polimorfismo: será sobrescrito por las subclases."""
        return "Acceso básico al sistema."

    def __str__(self):
        """Retorna una cadena legible representativa del objeto."""
        return f"ID: {self.id_cliente} | Nombre: {self.nombre}"

    def __eq__(self, otro):
        """Define igualdad entre clientes si comparten el mismo ID."""
        if not isinstance(otro, Cliente): return False
        return self.id_cliente == otro.id_cliente

# Aplicación de Herencia: Subclases especializadas
class ClienteRegular(Cliente):
    def obtener_beneficio(self):
        return "Cliente Regular: Sin descuentos especiales."

class ClientePremium(Cliente):
    def __init__(self, id_cliente, nombre, email, telefono, descuento=15):
        # Llama al constructor de la clase padre
        super().__init__(id_cliente, nombre, email, telefono)
        self.descuento = descuento

    def obtener_beneficio(self):
        """Implementación polimórfica del beneficio Premium."""
        return f"Cliente Premium: Posee un {self.descuento}% de descuento."

class ClienteCorporativo(Cliente):
    def __init__(self, id_cliente, nombre, email, telefono, empresa):
        super().__init__(id_cliente, nombre, email, telefono)
        self.empresa = empresa

    def obtener_beneficio(self):
        """Implementación polimórfica que resalta la asociación corporativa."""
        return f"Cliente Corporativo: Facturación directa para {self.empresa}."