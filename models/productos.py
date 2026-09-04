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

def actualizar_stock(producto_id, nuevo_stock):
    if nuevo_stock < 0:
        raise ValueError("El stock no puede ser negativo")

    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE productos SET stock = ? WHERE id = ?",
        (nuevo_stock, producto_id)
    )

    if cursor.rowcount == 0:
        conexion.close()
        raise ValueError(f"El producto con id {producto_id} no existe")

    conexion.commit()
    conexion.close()


def actualizar_disponibilidad(producto_id, disponible):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE productos SET disponible = ? WHERE id = ?",
        (disponible, producto_id)
    )

    if cursor.rowcount == 0:
        conexion.close()
        raise ValueError(f"El producto con id {producto_id} no existe")

    conexion.commit()
    conexion.close()


def actualizar_precio(producto_id, nuevo_precio):
    if nuevo_precio <= 0:
        raise ValueError("El precio debe ser mayor a 0")

    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE productos SET precio = ? WHERE id = ?",
        (nuevo_precio, producto_id)
    )

    if cursor.rowcount == 0:
        conexion.close()
        raise ValueError(f"El producto con id {producto_id} no existe")

    conexion.commit()
    conexion.close()