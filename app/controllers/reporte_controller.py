from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.database import Producto, Categoria, Pedido, PedidoEstado, db_session
from sqlalchemy import or_

reporte_controller = Blueprint('reporte_controller', __name__)
def create_reporte_blueprint():
    # Crear el objeto Blueprint
    reporte_blueprint = Blueprint('reporte', __name__)

    # Definir las rutas y las funciones controladoras
    @reporte_blueprint.route('/reporte')
    def inventario():

        return render_template('reporte/inventario.html')

    # Devolver el blueprint
    return reporte_blueprint