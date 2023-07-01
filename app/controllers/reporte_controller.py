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
        ingredientes = db_session.query(Ingrediente).filter(Ingrediente.activo == True).order_by(Ingrediente.nombre).all()
        total_ingredientes = db_session.query(func.count()).filter(Ingrediente.activo == True).scalar()
        
        alerta_stock = db_session.query(func.count()).filter(Ingrediente.cantidad <= Ingrediente.alerta_stock, Ingrediente.activo == True).order_by(Ingrediente.nombre).scalar()
        print(alerta_stock)
        
        ingredientes_criticos = db_session.query(Ingrediente).filter(Ingrediente.cantidad <= Ingrediente.alerta_stock, Ingrediente.activo == True).order_by(Ingrediente.nombre).all()
        print(ingredientes_criticos)

        umbral_proporcional = 1.50  # Ajusta el valor proporcional según tus necesidades
    
        ingredientes_cerca_alerta = db_session.query(Ingrediente).filter(
            Ingrediente.cantidad <= Ingrediente.alerta_stock * (1 + umbral_proporcional),
            Ingrediente.cantidad > Ingrediente.alerta_stock,
            Ingrediente.activo == True
        ).order_by(Ingrediente.nombre).all()

        return render_template('reporte/inventario.html', 
                               alerta_stock=alerta_stock, 
                               ingredientes_criticos=ingredientes_criticos,
                               total_ingredientes=total_ingredientes,
                               ingredientes=ingredientes,
                               ingredientes_cerca_alerta=ingredientes_cerca_alerta)

    # Devolver el blueprint
    return reporte_blueprint