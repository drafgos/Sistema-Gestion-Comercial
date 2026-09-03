import sqlite3

def conectar():
    conexion = sqlite3.connect("database/business.db")
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion

def crear_tablas():
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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_nombre TEXT NOT NULL,
            estado TEXT NOT NULL DEFAULT 'tomado',
            fecha_creacion TEXT NOT NULL DEFAULT (datetime('now')),
            CHECK (estado IN ('tomado','preparando', 'enviado', 'entregado'))
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS detalle_pedido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER NOT NULL,
            producto_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            precio_unitario INTEGER NOT NULL,
            FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        )
    ''')

    conexion.commit()
    conexion.close()