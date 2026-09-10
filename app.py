from flask import Flask, render_template, request, redirect, url_for
from database.conexion import crear_tablas
from models.categorias import listar_categorias
from models.productos import (
    listar_productos_por_categoria, listar_todos_los_productos,
    listar_productos_disponibles, actualizar_stock, actualizar_disponibilidad
)
from models.pedidos import listar_pedidos_por_estado, actualizar_estado_pedido

app = Flask(__name__)
crear_tablas()

ESTADOS = ["tomado", "preparando", "enviado", "entregado"]

@app.route("/")
def inicio():
    return "Servidor Flask funcionando correctamente"

@app.route("/cliente")
def cliente_inicio():
    productos = listar_productos_disponibles()
    return render_template("cliente/inicio.html", productos=productos)

@app.route("/cliente/categorias")
def cliente_categorias():
    categorias = listar_categorias()
    return render_template("cliente/categorias.html", categorias=categorias)

@app.route("/cliente/categoria/<int:categoria_id>")
def cliente_productos(categoria_id):
    productos = listar_productos_por_categoria(categoria_id)
    return render_template("cliente/productos.html", productos=productos)

@app.route("/trabajador")
def trabajador_pedidos():
    pedidos_por_estado = {estado: listar_pedidos_por_estado(estado) for estado in ESTADOS}
    return render_template("trabajador/pedidos.html", pedidos_por_estado=pedidos_por_estado, estados=ESTADOS)

@app.route("/trabajador/pedido/<int:pedido_id>/estado", methods=["POST"])
def trabajador_actualizar_estado(pedido_id):
    nuevo_estado = request.form.get("nuevo_estado")
    if nuevo_estado in ESTADOS:
        actualizar_estado_pedido(pedido_id, nuevo_estado)
    return redirect(url_for("trabajador_pedidos"))

@app.route("/trabajador/productos")
def trabajador_productos():
    productos = listar_todos_los_productos()
    return render_template("trabajador/productos.html", productos=productos)

@app.route("/trabajador/producto/<int:producto_id>/stock", methods=["POST"])
def trabajador_actualizar_stock(producto_id):
    nuevo_stock = request.form.get("nuevo_stock", type=int)
    if nuevo_stock is not None and nuevo_stock >= 0:
        actualizar_stock(producto_id, nuevo_stock)
    return redirect(url_for("trabajador_productos"))

@app.route("/trabajador/producto/<int:producto_id>/disponibilidad", methods=["POST"])
def trabajador_actualizar_disponibilidad(producto_id):
    disponible = request.form.get("disponible", type=int)
    if disponible in (0, 1):
        actualizar_disponibilidad(producto_id, disponible)
    return redirect(url_for("trabajador_productos"))

if __name__ == "__main__":
    app.run(debug=True)