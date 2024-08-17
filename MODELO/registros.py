
import sqlite3
from tkinter import messagebox
from MODELO.conexion import ConexionDB

def crear_tabla():
    conexion = ConexionDB()
    
    sql = '''CREATE TABLE PERSONAS (
        Nombre TEXT NOT NULL,
        Telefono TEXT NOT NULL,
        RedSocial TEXT NOT NULL
    )'''
    
    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()
        messagebox.showinfo("Crear Registro", "Se creó la tabla en la base de datos.")
    except sqlite3.OperationalError:
        messagebox.showwarning("Crear Registro", "La tabla ya está creada.")

def borrar_tabla():
    conexion = ConexionDB()   
    sql = 'DROP TABLE IF EXISTS PERSONAS'
    
    try:
        conexion.cursor.execute(sql)  
        conexion.cerrar()
        messagebox.showinfo("Borrar Registro", "La tabla en la base de datos se borró con éxito.")
    except sqlite3.Error:
        messagebox.showerror("Borrar Registro", "No se pudo borrar la tabla.")

class Persona1:
    def __init__(self, Nombre, Telefono, RedSocial):
        self.Nombre = Nombre
        self.Telefono = Telefono
        self.RedSocial = RedSocial

def guardar(persona):
    conexion = ConexionDB()
    sql = '''INSERT INTO PERSONAS (Nombre, Telefono, RedSocial)
        VALUES (?, ?, ?)'''
    
    try:    
        conexion.cursor.execute(sql, (persona.Nombre, persona.Telefono, persona.RedSocial))
        conexion.cerrar()
    except sqlite3.Error:
        messagebox.showerror("Guardar Registro", "No se pudo guardar el registro.")

def listar():
    conexion = ConexionDB()
    sql = 'SELECT * FROM PERSONAS'
    
    try:
        conexion.cursor.execute(sql)
        lista_personas = conexion.cursor.fetchall()
        conexion.cerrar()
        return lista_personas
    except sqlite3.Error as e:
        if "no such table" in str(e).lower():
            crear_tabla()
            return listar()
        else:
            messagebox.showerror("Consultar Registros", "Ocurrió un error al consultar registros: " + str(e))
            return []

def editar(persona):
    conexion = ConexionDB()
    sql = '''UPDATE PERSONAS
        SET Telefono = ?, RedSocial = ?
        WHERE Nombre = ?'''
    
    try:
        conexion.cursor.execute(sql, (persona.Telefono, persona.RedSocial, persona.Nombre))
        conexion.cerrar()
        messagebox.showinfo("Editar Registro", "Registro editado con éxito.")
    except sqlite3.Error as e:
        messagebox.showerror("Editar Registro", "No se pudo editar el registro: " + str(e))

def eliminar(nombre):
    conexion = ConexionDB()
    sql = 'DELETE FROM PERSONAS WHERE Nombre = ?'
    
    try:
        conexion.cursor.execute(sql, (nombre,))
        conexion.cerrar()
        messagebox.showinfo("Eliminar Registro", "Registro eliminado con éxito.")
    except sqlite3.Error as e:
        messagebox.showerror("Eliminar Registro", "No se pudo eliminar el registro: " + str(e))