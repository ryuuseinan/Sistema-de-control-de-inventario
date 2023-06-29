from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.database import Pedido, PedidoEstado, Producto, Categoria, Receta, RecetaDetalle, PedidoDetalle, PedidoDetalleIngrediente, Ingrediente, db_session
from sqlalchemy import or_, func

reporte_controller = Blueprint('reporte_controller', __name__)
def create_reporte_blueprint():
    # Crear el objeto Blueprint
    reporte_blueprint = Blueprint('reporte', __name__)

    # Definir las rutas y las funciones controladoras
    @reporte_blueprint.route('/reporte')
    def inventario():

        total_ingredientes = db_session.query(func.count()).filter(Ingrediente.activo == True).scalar()
        
        alerta_stock = db_session.query(func.count()).filter(Ingrediente.cantidad <= Ingrediente.alerta_stock, Ingrediente.activo == True).scalar()
        print(alerta_stock)
        ingredientes_criticos = db_session.query(Ingrediente).filter(Ingrediente.cantidad <= Ingrediente.alerta_stock, Ingrediente.activo == True).all()
        print(ingredientes_criticos)
        return render_template('reporte/inventario.html', 
                               alerta_stock=alerta_stock, 
                               ingredientes_criticos=ingredientes_criticos,
                               total_ingredientes=total_ingredientes)

    # Devolver el blueprint
    return reporte_blueprint