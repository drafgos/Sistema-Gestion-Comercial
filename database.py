import sqlite3

def conectar():
    conexion = sqlite3.connect("database/business.db")
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion

def crear_tablas():
    conexion = conectar()
    cursor = conexion.cursor()

def crear_categorias(nombre, descripcion):
    conexion = conectar()
    cursor = conexion.cursor()

def crear_productos(nombre, descripcion, precio, stock, disponible, categoria_id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            precio INTEGER NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0,
            disponible BOOLEAN NOT NULL DEFAULT 1,
            categoria_id INTEGER NOT NULL,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        )
    ''')

    conexion.commit()
    conexion.close()