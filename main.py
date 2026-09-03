from database.conexion import conectar, crear_tablas
from models.categorias import crear_categorias, listar_categorias
from models.productos import crear_productos, listar_productos_por_categoria
from models.pedidos import crear_pedido_completo, StockInsuficiente, obtener_pedido_completo

crear_tablas()

crear_categorias("Electrónica", "Dispositivos electrónicos y gadgets")

print("Tablas creadas y categoría insertada correctamente.")

crear_productos("iPhone 13", "Smartphone de última generación", 650990, 10, 1, 1)
crear_productos("Cargador USB-C", "Cargador rápido", 15990, 20, 1, 1)

print("Productos insertados correctamente.")

try:
    pedido_id = crear_pedido_completo("Juan Pérez", [
        {"producto_id": 1, "cantidad": 2},
        {"producto_id": 2, "cantidad": 1},
    ])
    print(f"Pedido creado con id: {pedido_id}")
    print(obtener_pedido_completo(pedido_id))
except StockInsuficiente as e:
    print(f"No se pudo crear el pedido: {e}")
except ValueError as e:
    print(f"Datos inválidos: {e}")

conexion = conectar()
print("Conexión a la base de datos establecida correctamente.")
conexion.close()