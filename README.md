# Gestor Inteligente de Clientes (GIC) - Solution Tech 🚀

Sistema integral de gestión de clientes desarrollado en Python para optimizar la administración de datos, eliminar duplicidades y asegurar la escalabilidad operativa.

## 📂 Contenido del Proyecto
* **POO Avanzada**: Implementación de clases con herencia y polimorfismo.
* **Persistencia**: Uso de SQLite, JSON y CSV.
* **Interfaz**: GUI desarrollada en Tkinter.
* **Calidad**: Suite de pruebas unitarias y registro de logs.

## 🏛️ Entregables Técnicos

### 1. Paradigma de Orientación a Objetos (POO)
El sistema se basa en POO para permitir una estructura modular y segura. 
* **Encapsulación**: Validación de atributos como email y teléfono mediante métodos internos.
* **Herencia y Polimorfismo**: Especialización en tipos de clientes: Regular, Premium y Corporativo. Se utilizan métodos sobrescritos y `super()` para reutilización de código.
* **Métodos Especiales**: Implementación de `__str__` y `__eq__` para una gestión de objetos eficiente.

### 2. Manejo de Errores y Excepciones
Se implementó un manejo de errores estructurado para evitar caídas del sistema:
* **Excepciones Personalizadas**: Validación rigurosa de datos de entrada en la interfaz.
* **Logs de Actividad**: Registro automático de operaciones y errores de conexión a la base de datos.

### 3. Persistencia de Datos
* **SQLite**: Almacenamiento seguro y persistente de la base de clientes.
* **Exportación**: Generación de reportes en formatos JSON y CSV para interoperabilidad.

## 📸 Demostración de Ejecución
Aquí se visualiza la interfaz gráfica y la validación de identidad mediante servicios externos:

![Menú Principal](./screenshots/main_menu.png)
*Interfaz principal del sistema GIC Pro.*

![Validación de Datos](./screenshots/validation_error.png)
*Manejo de errores y validaciones avanzadas.*

## 🧪 Pruebas Unitarias
Para asegurar la fiabilidad del software, se implementó una suite de unit testing:
```bash
python tests.py