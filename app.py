from flask import Flask, render_template
from database.conexion import crear_tablas
from models.categorias import listar_categorias
from models.productos import listar_productos_por_categoria

app = Flask(__name__)
crear_tablas()

@app.route("/")
def inicio():
    return "Servidor Flask funcionando correctamente"

@app.route("/cliente")
def cliente_categorias():
    categorias = listar_categorias()
    return render_template("cliente/categorias.html", categorias=categorias)

@app.route("/cliente/categoria/<int:categoria_id>")
def cliente_productos(categoria_id):
    productos = listar_productos_por_categoria(categoria_id)
    return render_template("cliente/productos.html", productos=productos)

if __name__ == "__main__":
    app.run(debug=True)