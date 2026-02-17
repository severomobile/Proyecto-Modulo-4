# Modelo UML - Proyecto GIC

```mermaid
classDiagram
    class Cliente {
        -String __email
        -String __telefono
        +String id_cliente
        +String nombre
        +email (property)
        +telefono (property)
        +obtener_beneficio()
        +__str__()
        +__eq__(otro)
    }

    class ClienteRegular {
        +obtener_beneficio()
    }

    class ClientePremium {
        +Int descuento
        +obtener_beneficio()
    }

    class ClienteCorporativo {
        +String empresa
        +obtener_beneficio()
    }

    class DatabaseManager {
        +String db_name
        +crear_tabla()
        +guardar_cliente(cliente)
        +obtener_todos()
        +actualizar_cliente(cliente)
        +eliminar_cliente_db(id_cliente)
        +exportar_datos()
    }

    class Services {
        <<module>>
        +validar_identidad_api(id_cliente)
        +enviar_notificacion_bienvenida(cliente)
    }

    class Logger {
        <<module>>
        +registrar_evento(mensaje)
        +registrar_error(mensaje)
    }

    class GIC_App {
        +db: DatabaseManager
        +ejecutar_registro()
        +ejecutar_actualizacion()
        +eliminar_cliente()
        +cargar_para_editar()
    }

    %% Relaciones de Herencia
    Cliente <|-- ClienteRegular
    Cliente <|-- ClientePremium
    Cliente <|-- ClienteCorporativo

    %% Relaciones de Uso y Dependencia
    GIC_App o-- DatabaseManager : Agregación
    GIC_App ..> Services : Consulta
    GIC_App ..> Cliente : Manipula
    DatabaseManager ..> Cliente : Persiste
    DatabaseManager ..> Logger : Registra
    Services ..> Logger : Registra