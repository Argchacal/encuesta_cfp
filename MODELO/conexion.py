import sqlite3
import os

class ConexionDB:
    def __init__(self):
        self.base_datos = 'database/centro.db'
        carpeta = os.path.dirname(self.base_datos)
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
        self.conexion = sqlite3.connect(self.base_datos)
        self.cursor = self.conexion.cursor()
        
    def cerrar(self):
        self.conexion.commit()
        self.conexion.close()

