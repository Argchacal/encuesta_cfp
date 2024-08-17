import tkinter as tk
from tkinter import messagebox, ttk
from MODELO.conexion import ConexionDB
from MODELO.registros import crear_tabla, borrar_tabla, Persona1, listar, editar, guardar, eliminar

def barramenu(app):
    barra_menu = tk.Menu(app)
    app.config(menu=barra_menu, width=300, height=300)

    menu_inicio = tk.Menu(barra_menu, tearoff=0)
    barra_menu.add_cascade(label='Inicio', menu=menu_inicio)

    menu_inicio.add_command(label='Ver Registros', command=app.show_registros)
    menu_inicio.add_command(label='Eliminar BD', command=borrar_tabla)
    menu_inicio.add_command(label='Salir', command=app.destroy)

    barra_menu.add_cascade(label='Ayuda')

class MainFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, width=800, height=600)
        self.parent = parent
        self.pack(fill=tk.BOTH, expand=True)
        self.config(bg='black')

        self.campos()
        self.boton()
        self.deshabilitar_campos()  # Inicialmente deshabilitar campos
        
        # Crear la tabla de registros
        self.create_table()

    def campos(self):
        self.label_Nombre = tk.Label(self, text='Nombre:')
        self.label_Nombre.config(font=('Arial', 12, 'bold'), bg='grey')
        self.label_Nombre.grid(row=0, column=0, padx=10, pady=10)           
    
        self.label_Telefono = tk.Label(self, text='Telefono:')
        self.label_Telefono.config(font=('Arial', 12, 'bold'), bg='grey')
        self.label_Telefono.grid(row=1, column=0, padx=10, pady=10)

        self.label_RedSocial = tk.Label(self, text='Red Social:')
        self.label_RedSocial.config(font=('Arial', 12, 'bold'), bg='grey')
        self.label_RedSocial.grid(row=2, column=0, padx=10, pady=10)

        self.mi_Nombre = tk.StringVar()
        self.entry_Nombre = tk.Entry(self, textvariable=self.mi_Nombre)
        self.entry_Nombre.config(width=50)
        self.entry_Nombre.grid(row=0, column=1, padx=10, pady=10, columnspan=2)

        self.mi_Telefono = tk.StringVar()
        self.entry_Telefono = tk.Entry(self, textvariable=self.mi_Telefono)
        self.entry_Telefono.config(width=50)
        self.entry_Telefono.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

        self.mi_RedSocial = tk.StringVar()
        self.entry_RedSocial = tk.Entry(self, textvariable=self.mi_RedSocial)
        self.entry_RedSocial.config(width=50)
        self.entry_RedSocial.grid(row=2, column=1, padx=10, pady=10, columnspan=2)

    def boton(self):
        self.boton_Nuevo = tk.Button(self, text='Nuevo', command=self.habilitar_campos)
        self.boton_Nuevo.config(width=20, font=('Arial', 12, 'bold'), fg='white', bg='blue')
        self.boton_Nuevo.grid(row=3, column=0, padx=10, pady=10)

        self.boton_Guardar = tk.Button(self, text='Guardar', command=self.guardar_datos)
        self.boton_Guardar.config(width=20, font=('Arial', 12, 'bold'), fg='white', bg='blue')
        self.boton_Guardar.grid(row=3, column=1, padx=10, pady=10)

        self.boton_Cancelar = tk.Button(self, text='Cancelar', command=self.deshabilitar_campos)
        self.boton_Cancelar.config(width=20, font=('Arial', 12, 'bold'), fg='white', bg='blue')
        self.boton_Cancelar.grid(row=3, column=2, padx=10, pady=10)

    def habilitar_campos(self):
        self.entry_Nombre.config(state='normal')
        self.entry_Telefono.config(state='normal')
        self.entry_RedSocial.config(state='normal')
        
        self.boton_Guardar.config(state='normal')
        self.boton_Cancelar.config(state='normal')

    def deshabilitar_campos(self):
        self.mi_Nombre.set('')
        self.mi_Telefono.set('')
        self.mi_RedSocial.set('')
        
        self.entry_Nombre.config(state='disabled')
        self.entry_Telefono.config(state='disabled')
        self.entry_RedSocial.config(state='disabled')
        
        self.boton_Guardar.config(state='disabled')
        self.boton_Cancelar.config(state='disabled')

    def guardar_datos(self):
        persona = Persona1(
            self.mi_Nombre.get(), 
            self.mi_Telefono.get(),
            self.mi_RedSocial.get(),
        )
        if persona:
            guardar(persona)
            self.update_table()
        else:
            messagebox.showwarning("Guardar Registro", "Por favor completa todos los campos.")
        self.deshabilitar_campos()

    def create_table(self):
        if hasattr(self, 'tabla'):
            self.tabla.destroy()
        
        self.tabla = ttk.Treeview(self, columns=('Nombre', 'Telefono', 'RedSocial'), show='headings')
        self.tabla.grid(row=4, column=0, columnspan=3, sticky='nse')
        
        self.scroll = ttk.Scrollbar(self, orient='vertical', command=self.tabla.yview)
        self.scroll.grid(row=4, column=3, sticky='ns')
        self.tabla.configure(yscrollcommand=self.scroll.set)
        
        self.tabla.heading('#1', text='Nombre', anchor=tk.CENTER)
        self.tabla.heading('#2', text='Telefono', anchor=tk.CENTER)
        self.tabla.heading('#3', text='Red Social', anchor=tk.CENTER)
        
        self.tabla.column('#1', width=150, anchor=tk.CENTER)
        self.tabla.column('#2', width=150, anchor=tk.CENTER)
        self.tabla.column('#3', width=150, anchor=tk.CENTER)
        
        # Botón Editar
        self.boton_Editar = tk.Button(self, text='Editar', command=self.editar_datos)
        self.boton_Editar.config(width=20, font=('Arial', 12, 'bold'), fg='white', bg='blue')
        self.boton_Editar.grid(row=5, column=0, padx=10, pady=10)

        # Botón Eliminar
        self.boton_Eliminar = tk.Button(self, text='Eliminar', command=self.eliminar_datos)
        self.boton_Eliminar.config(width=20, font=('Arial', 12, 'bold'), fg='white', bg='orange')
        self.boton_Eliminar.grid(row=5, column=1, padx=10, pady=10)

        self.update_table()

    def update_table(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        lista_personas = listar()
        for p in lista_personas:
            self.tabla.insert('', 'end', values=(p[0], p[1], p[2]))

    def editar_datos(self):
        self.habilitar_campos()
        
        try:
            selected_item = self.tabla.selection()[0]
            selected_values = self.tabla.item(selected_item, 'values')
            
            if selected_values:
                self.mi_Nombre.set(selected_values[0])
                self.mi_Telefono.set(selected_values[1])
                self.mi_RedSocial.set(selected_values[2])
                
                self.boton_Guardar.config(command=lambda: self.editar(selected_item))
            else:
                messagebox.showerror("Editar Datos", "No ha seleccionado ningún registro.")
            
        except IndexError:
            messagebox.showerror("Editar Datos", "Ha ocurrido un error al intentar editar un registro.")
    
    def editar(self, item):
        persona = Persona1(
            self.mi_Nombre.get(), 
            self.mi_Telefono.get(),
            self.mi_RedSocial.get(),
        )
        if persona:
            editar(persona)
            self.update_table()
        else:
            messagebox.showwarning("Editar Registro", "Por favor completa todos los campos.")

    def eliminar_datos(self):
        try:
            selected_item = self.tabla.selection()[0]
            selected_values = self.tabla.item(selected_item, 'values')
            
            if selected_values:
                nombre = selected_values[0]
                eliminar(nombre)
                self.update_table()
            else:
                messagebox.showerror("Eliminar Datos", "No ha seleccionado ningún registro.")
        except IndexError:
            messagebox.showerror("Eliminar Datos", "Ha ocurrido un error al intentar eliminar un registro.")

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplicación de Registros")
        self.geometry("800x600")
        self.main_frame = MainFrame(self)
        barramenu(self)
    
    def show_registros(self):
        self.main_frame.update_table()