from database.conexion import conectar

def crear_categorias(nombre, descripcion):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO categorias (nombre, descripcion) VALUES (?, ?)
    ''', (nombre, descripcion))
    conexion.commit()
    conexion.close()


def listar_categorias():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, descripcion FROM categorias")
    filas = cursor.fetchall()
    conexion.close()
    return [{"id": f[0], "nombre": f[1], "descripcion": f[2]} for f in filas]