from database import conectar, crear_tablas, crear_categorias, crear_productos

crear_tablas()

crear_categorias("Electrónica", "Dispositivos electrónicos y gadgets")

print("Tablas creadas y categoría insertada correctamente.")

crear_productos("iPhone 13", "Smartphone de última generación", 650.990, 10, 1, 1)

print("Producto insertado correctamente.")

conexion = conectar()

print("Conexión a la base de datos establecida correctamente.")

conexion.close()    