from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.database import Producto, Categoria, db_session
from sqlalchemy import or_

vender_controller = Blueprint('vender_controller', __name__)
def create_vender_blueprint():
    # Crear el objeto Blueprint
    vender_blueprint = Blueprint('vender', __name__)

    # Definir las rutas y las funciones controladoras
    @vender_blueprint.route('/vender', methods=['GET', 'POST'])
    def vender():
        producto_busqueda = request.form.get('producto_busqueda')
        if request.method == 'POST' and producto_busqueda:
            productos = db_session.query(Producto).join(Categoria).filter(or_(Producto.nombre.ilike(f'%{producto_busqueda}%'),
                                                                    Categoria.nombre.ilike(f'%{producto_busqueda}%'),
                                                                    Producto.codigo_barra == producto_busqueda),
                                                                Producto.activo == True).all()
            if not productos:
                flash("No se encontraron productos con ese criterio de búsqueda", "error")
                productos = db_session.query(Producto).filter(Producto.activo == True).all()
        elif request.method == 'POST' and not producto_busqueda:
            flash("Por favor, ingrese el nombre o código de barras de un producto", "error")
            productos = db_session.query(Producto).filter(Producto.activo == True).all()
        else:
            productos = db_session.query(Producto).filter(Producto.activo == True).all()

        return render_template('vender/vender.html', productos=productos, producto_busqueda=producto_busqueda)

    # Devolver el blueprint
    return vender_blueprint