from database import conectar, crear_tablas, crear_categorias

crear_tablas()

crear_categorias("Electrónica", "Dispositivos electrónicos y gadgets")

print("Tablas creadas y categoría insertada correctamente.")

conexion = conectar()

print("Conexión a la base de datos establecida correctamente.")

conexion.close()    