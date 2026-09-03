from database.conexion import conectar

def crear_productos(nombre, descripcion, precio, stock, disponible, categoria_id):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO productos (nombre, descripcion, precio, stock, disponible, categoria_id) VALUES (?, ?, ?, ?, ?, ?)
    ''', (nombre, descripcion, precio, stock, disponible, categoria_id))
    conexion.commit()
    conexion.close()


def listar_productos_por_categoria(categoria_id):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        SELECT id, nombre, descripcion, precio, stock, disponible
        FROM productos
        WHERE categoria_id = ?
    ''', (categoria_id,))
    filas = cursor.fetchall()
    conexion.close()
    return [
        {"id": f[0], "nombre": f[1], "descripcion": f[2],
         "precio": f[3], "stock": f[4], "disponible": bool(f[5])}
        for f in filas
    ]


def obtener_producto(producto_id):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        SELECT id, nombre, descripcion, precio, stock, disponible, categoria_id
        FROM productos WHERE id = ?
    ''', (producto_id,))
    f = cursor.fetchone()
    conexion.close()
    if f is None:
        return None
    return {"id": f[0], "nombre": f[1], "descripcion": f[2], "precio": f[3],
            "stock": f[4], "disponible": bool(f[5]), "categoria_id": f[6]}


def buscar_productos(texto):
    conexion = conectar()
    cursor = conexion.cursor()
    patron = f"%{texto}%"
    cursor.execute('''
        SELECT id, nombre, descripcion, precio, stock, disponible
        FROM productos
        WHERE nombre LIKE ? OR descripcion LIKE ?
    ''', (patron, patron))
    filas = cursor.fetchall()
    conexion.close()
    return [
        {"id": f[0], "nombre": f[1], "descripcion": f[2],
         "precio": f[3], "stock": f[4], "disponible": bool(f[5])}
        for f in filas
    ]