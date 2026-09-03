from database.conexion import conectar

class StockInsuficiente(Exception):
    pass


def crear_pedido_completo(cliente_nombre, items):
    """
    items: lista de diccionarios, ej:
    [{"producto_id": 1, "cantidad": 2}, {"producto_id": 3, "cantidad": 1}]
    """
    conexion = conectar()
    cursor = conexion.cursor()
    try:
        for item in items:
            cursor.execute(
                "SELECT stock, precio, disponible FROM productos WHERE id = ?",
                (item["producto_id"],)
            )
            fila = cursor.fetchone()
            if fila is None:
                raise ValueError(f"El producto con id {item['producto_id']} no existe")
            stock_actual, precio, disponible = fila
            if not disponible:
                raise StockInsuficiente(f"El producto {item['producto_id']} no esta disponible")
            if item["cantidad"] <= 0:
                raise ValueError("La cantidad debe ser mayor a 0")
            if stock_actual < item["cantidad"]:
                raise StockInsuficiente(
                    f"Stock insuficiente para el producto {item['producto_id']} "
                    f"(disponible: {stock_actual}, pedido: {item['cantidad']})"
                )
            item["precio_unitario"] = precio

        cursor.execute("INSERT INTO pedidos (cliente_nombre) VALUES (?)", (cliente_nombre,))
        pedido_id = cursor.lastrowid

        for item in items:
            cursor.execute('''
                INSERT INTO detalle_pedido (pedido_id, producto_id, cantidad, precio_unitario)
                VALUES (?, ?, ?, ?)
            ''', (pedido_id, item["producto_id"], item["cantidad"], item["precio_unitario"]))
            cursor.execute('UPDATE productos SET stock = stock - ? WHERE id = ?',
                            (item["cantidad"], item["producto_id"]))

        conexion.commit()
        return pedido_id
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()


def actualizar_estado_pedido(pedido_id, nuevo_estado):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('UPDATE pedidos SET estado = ? WHERE id = ?', (nuevo_estado, pedido_id))
    conexion.commit()
    conexion.close()


def listar_pedidos_por_estado(estado):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        SELECT id, cliente_nombre, estado, fecha_creacion
        FROM pedidos WHERE estado = ?
        ORDER BY fecha_creacion
    ''', (estado,))
    filas = cursor.fetchall()
    conexion.close()
    return [{"id": f[0], "cliente_nombre": f[1], "estado": f[2], "fecha_creacion": f[3]} for f in filas]


def obtener_pedido_completo(pedido_id):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        SELECT id, cliente_nombre, estado, fecha_creacion
        FROM pedidos WHERE id = ?
    ''', (pedido_id,))
    cabecera = cursor.fetchone()
    if cabecera is None:
        conexion.close()
        return None
    cursor.execute('''
        SELECT p.nombre, dp.cantidad, dp.precio_unitario
        FROM detalle_pedido dp
        JOIN productos p ON p.id = dp.producto_id
        WHERE dp.pedido_id = ?
    ''', (pedido_id,))
    items = cursor.fetchall()
    conexion.close()
    return {
        "id": cabecera[0], "cliente_nombre": cabecera[1],
        "estado": cabecera[2], "fecha_creacion": cabecera[3],
        "items": [{"producto": i[0], "cantidad": i[1], "precio_unitario": i[2]} for i in items],
        "total": sum(i[1] * i[2] for i in items)
    }