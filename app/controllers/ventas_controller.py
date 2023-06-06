from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.database import Producto, Categoria, db_session
from sqlalchemy import or_

ventas_controller = Blueprint('ventas_controller', __name__)
def create_ventas_blueprint():
    # Crear el objeto Blueprint
    ventas_blueprint = Blueprint('ventas', __name__)

    # Definir las rutas y las funciones controladoras
    @ventas_blueprint.route('/ventas')
    def listar():
        return render_template('ventas/listar.html')

    # Devolver el blueprint
    return ventas_blueprint