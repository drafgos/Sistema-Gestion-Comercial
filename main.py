from database import conectar, crear_tablas

crear_tablas()

conexion = conectar()

print("Conexión a la base de datos establecida correctamente.")

conexion.close()