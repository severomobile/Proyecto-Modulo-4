import tkinter as tk
from tkinter import messagebox, ttk
from models import ClienteRegular, ClientePremium, ClienteCorporativo
from database import DatabaseManager
from services import validar_identidad_api, enviar_notificacion_bienvenida

class GIC_App:
    """Clase principal que gestiona la Interfaz Gráfica de Usuario (GUI)."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Solution Tech - Sistema GIC Pro")
        # Instancia del gestor de persistencia
        self.db = DatabaseManager()

        # --- Sección de Formulario de Entrada ---
        frame_form = tk.LabelFrame(root, text=" Registro de Cliente ", padx=10, pady=10)
        frame_form.pack(padx=10, pady=5, fill="x")

        # Configuración de etiquetas y campos de texto (Entry)
        tk.Label(frame_form, text="ID:").grid(row=0, column=0, sticky="w")
        self.ent_id = tk.Entry(frame_form)
        self.ent_id.grid(row=0, column=1, pady=2, padx=5)

        tk.Label(frame_form, text="Nombre:").grid(row=1, column=0, sticky="w")
        self.ent_nombre = tk.Entry(frame_form)
        self.ent_nombre.grid(row=1, column=1, pady=2, padx=5)

        tk.Label(frame_form, text="Email:").grid(row=2, column=0, sticky="w")
        self.ent_email = tk.Entry(frame_form)
        self.ent_email.grid(row=2, column=1, pady=2, padx=5)

        tk.Label(frame_form, text="Teléfono:").grid(row=3, column=0, sticky="w")
        self.ent_tel = tk.Entry(frame_form)
        self.ent_tel.grid(row=3, column=1, pady=2, padx=5)

        # Selector de tipo de cliente mediante Combobox
        tk.Label(frame_form, text="Tipo:").grid(row=4, column=0, sticky="w")
        self.combo_tipo = ttk.Combobox(frame_form, values=["Regular", "Premium", "Corporativo"], state="readonly")
        self.combo_tipo.current(0)
        self.combo_tipo.grid(row=4, column=1, pady=2, padx=5)

        # --- Panel de Botones de Acción ---
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        # Botones con sus respectivos comandos y estilos visuales
        tk.Button(btn_frame, text="Registrar", bg="#4CAF50", fg="white", command=self.ejecutar_registro).pack(side=tk.LEFT, padx=5)
        
        # Funciones para el flujo de edición (Update)
        tk.Button(btn_frame, text="Cargar para Editar", bg="#2196F3", fg="white", command=self.cargar_para_editar).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Guardar Cambios", bg="#FF9800", fg="white", command=self.ejecutar_actualizacion).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Eliminar Seleccionado", bg="#f44336", fg="white", command=self.eliminar_cliente).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Exportar Backup", command=self.exportar).pack(side=tk.LEFT, padx=5)

        # --- Tabla de Visualización de Datos (Treeview) ---
        self.tree = ttk.Treeview(root, columns=("ID", "Nombre", "Email", "Telefono", "Tipo", "Detalle"), show='headings')
        self.tree.heading("ID", text="ID"); self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Email", text="Email"); self.tree.heading("Telefono", text="Teléfono")
        self.tree.heading("Tipo", text="Categoría"); self.tree.heading("Detalle", text="Beneficio/Empresa")
        
        self.tree.column("ID", width=50); self.tree.column("Telefono", width=100); self.tree.column("Detalle", width=150)
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Carga inicial de datos desde la BD
        self.cargar_datos()

    def cargar_para_editar(self):
        """Pasa la información de la fila seleccionada a los campos de texto para su edición."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atención", "Seleccione un cliente de la tabla para editar.")
            return
        
        datos = self.tree.item(selected)['values']
        self.limpiar_campos()
        
        # Poblar formulario y bloquear ID para mantener integridad referencial
        self.ent_id.insert(0, datos[0])
        self.ent_id.config(state='disabled') 
        self.ent_nombre.insert(0, datos[1])
        self.ent_email.insert(0, datos[2])
        self.ent_tel.insert(0, datos[3])
        self.combo_tipo.set(datos[4])

    def ejecutar_actualizacion(self):
        """Procesa la modificación de datos del cliente en la base de datos."""
        try:
            cid, nom, eml, tel = self.ent_id.get(), self.ent_nombre.get(), self.ent_email.get(), self.ent_tel.get()
            tipo = self.combo_tipo.get()

            if not all([cid, nom, eml, tel]):
                raise ValueError("Todos los campos son obligatorios.")

            # Instanciación polimórfica para la actualización
            if tipo == "Regular": nuevo = ClienteRegular(cid, nom, eml, tel)
            elif tipo == "Premium": nuevo = ClientePremium(cid, nom, eml, tel)
            else: nuevo = ClienteCorporativo(cid, nom, eml, tel, "Empresa Editada")

            # Ejecución del Update en persistencia
            if self.db.actualizar_cliente(nuevo):
                messagebox.showinfo("Éxito", "Datos actualizados correctamente.")
                self.ent_id.config(state='normal') 
                self.limpiar_campos()
                self.cargar_datos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar: {e}")

    def ejecutar_registro(self):
        """Gestiona el flujo de alta de clientes: validación API, creación y guardado."""
        try:
            cid, nom, eml, tel = self.ent_id.get(), self.ent_nombre.get(), self.ent_email.get(), self.ent_tel.get()
            tipo = self.combo_tipo.get()
            
            if not all([cid, nom, eml, tel]): raise ValueError("Todos los campos son obligatorios.")
            # Integración con servicio externo de validación
            if not validar_identidad_api(cid): raise ValueError("Error de identidad.")

            # Selección de clase según categoría
            if tipo == "Regular": nuevo = ClienteRegular(cid, nom, eml, tel)
            elif tipo == "Premium": nuevo = ClientePremium(cid, nom, eml, tel)
            else: nuevo = ClienteCorporativo(cid, nom, eml, tel, "Empresa Genérica")

            # Persistencia y notificación automática
            self.db.guardar_cliente(nuevo)
            enviar_notificacion_bienvenida(nuevo)
            messagebox.showinfo("Éxito", f"Cliente {nom} registrado.")
            self.limpiar_campos(); self.cargar_datos()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar_cliente(self):
        """Elimina el registro seleccionado tras confirmación del usuario."""
        selected = self.tree.selection()
        if not selected: return
        id_cliente = self.tree.item(selected)['values'][0]
        if messagebox.askyesno("Confirmar", f"¿Eliminar ID {id_cliente}?"):
            if self.db.eliminar_cliente_db(id_cliente):
                self.cargar_datos()

    def cargar_datos(self):
        """Refresca la tabla visual con los datos actuales de la base de datos."""
        for item in self.tree.get_children(): self.tree.delete(item)
        for row in self.db.obtener_todos():
            self.tree.insert("", tk.END, values=row)

    def limpiar_campos(self):
        """Restablece los campos de entrada del formulario."""
        self.ent_id.config(state='normal')
        for entry in [self.ent_id, self.ent_nombre, self.ent_email, self.ent_tel]:
            entry.delete(0, tk.END)

    def exportar(self):
        """Activa la generación de backups en formatos externos."""
        self.db.exportar_datos()
        messagebox.showinfo("Exportación", "Backups generados.")