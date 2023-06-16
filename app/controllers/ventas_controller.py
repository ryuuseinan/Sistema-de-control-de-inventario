from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.database import Producto, Categoria, Pedido, PedidoEstado, db_session
from sqlalchemy import or_

ventas_controller = Blueprint('ventas_controller', __name__)
def create_ventas_blueprint():
    # Crear el objeto Blueprint
    ventas_blueprint = Blueprint('ventas', __name__)

    def calcular_total_pedido(pedido):
        total_pedido = 0
        for pedido_detalle in pedido.detalles:
            total_pedido += pedido_detalle.cantidad * pedido_detalle.producto.precio
        return total_pedido

    # Definir las rutas y las funciones controladoras
    @ventas_blueprint.route('/ventas')
    def listar():
        pedidos = db_session.query(Pedido).filter(Pedido.estado_id == 2).all()
        estado_pedido = db_session.query(PedidoEstado).all()

        for pedido in pedidos:
            pedido.total_pedido = calcular_total_pedido(pedido)
        
        return render_template('ventas/listar.html', pedidos=pedidos, estado_pedido=estado_pedido)

    # Devolver el blueprint
    return ventas_blueprint