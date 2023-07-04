from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.database import Pedido, PedidoEstado, Producto, Categoria, Receta, RecetaDetalle, PedidoDetalle, PedidoDetalleIngrediente, Ingrediente, db_session
from sqlalchemy import or_, func, and_


reporte_controller = Blueprint('reporte_controller', __name__)
def create_reporte_blueprint():
    # Crear el objeto Blueprint
    reporte_blueprint = Blueprint('reporte', __name__)

    # Definir las rutas y las funciones controladoras
    @reporte_blueprint.route('/reporte')
    def inventario():
        productos = db_session.query(Producto).filter(Producto.activo == True).all()
        for producto in productos:
            receta = db_session.query(Receta).filter_by(producto_id=producto.id).first()
            if receta:
                receta_detalles = db_session.query(RecetaDetalle).filter_by(receta_id=receta.id).all()
                ingredientes = [detalle.ingrediente for detalle in receta_detalles]
                producto.receta = receta
                producto.receta_detalles = receta_detalles
                producto.ingredientes = ingredientes
                producto.stock_disponible = (
                    producto.stock if not producto.tiene_receta else min(
                        [ingrediente.cantidad // detalle.cantidad for ingrediente, detalle in
                         zip(ingredientes, receta_detalles)])
                )
            else:
                producto.receta = None
                producto.receta_detalles = []
                producto.ingredientes = []
                producto.stock_disponible = producto.stock

        ingredientes = db_session.query(Ingrediente).filter(Ingrediente.activo == True).order_by(Ingrediente.nombre).all()
        total_ingredientes = db_session.query(func.count()).filter(Ingrediente.activo == True).scalar()

        total_productos = db_session.query(func.count()).filter(Producto.activo == True).scalar()
        
        ingrediente_alerta_stock = db_session.query(func.count()).filter(Ingrediente.cantidad <= Ingrediente.alerta_stock, Ingrediente.activo == True).order_by(Ingrediente.nombre).scalar()
        print(ingrediente_alerta_stock)

        ingredientes_criticos = db_session.query(Ingrediente).filter(Ingrediente.cantidad <= Ingrediente.alerta_stock, Ingrediente.activo == True).order_by(Ingrediente.nombre).all()
        print(ingredientes_criticos)

        productos_criticos = [producto for producto in productos if producto.stock_disponible is not None and producto.stock_disponible <= producto.alerta_stock]
        producto_alerta_stock = len(productos_criticos)
        
        umbral_proporcional = 1.50  # Ajusta el valor proporcional según tus necesidades

        productos_cerca_alerta = [producto for producto in productos if producto.stock_disponible is not None and producto.stock_disponible <= producto.alerta_stock * (1 + umbral_proporcional) and producto.stock_disponible > producto.alerta_stock]
    
        ingredientes_cerca_alerta = db_session.query(Ingrediente).filter(
            Ingrediente.cantidad <= Ingrediente.alerta_stock * (1 + umbral_proporcional),
            Ingrediente.cantidad > Ingrediente.alerta_stock,
            Ingrediente.activo == True
        ).order_by(Ingrediente.nombre).all()

        return render_template('reporte/inventario.html', 
                               ingrediente_alerta_stock=ingrediente_alerta_stock, 
                               ingredientes_criticos=ingredientes_criticos,
                               total_ingredientes=total_ingredientes,
                               ingredientes=ingredientes,
                               ingredientes_cerca_alerta=ingredientes_cerca_alerta,
                               total_productos=total_productos,
                               producto_alerta_stock=producto_alerta_stock,
                               productos_cerca_alerta=productos_cerca_alerta,
                               productos_criticos=productos_criticos,
                               productos=productos)

    # Devolver el blueprint
    return reporte_blueprint