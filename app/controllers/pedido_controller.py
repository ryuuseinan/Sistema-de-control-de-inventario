from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.database import Usuario, Pedido, PedidoEstado, Persona, Producto, Categoria, Receta, RecetaDetalle, PedidoDetalle, db_session
import bcrypt, arrow
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from datetime import datetime

pedido_controller = Blueprint('pedido_controller', __name__)
def create_pedido_blueprint():
    # Crear el objeto Blueprint
    pedido_blueprint = Blueprint('pedido', __name__)

    def calcular_total_pedido(pedido):
        total_pedido = 0
        for pedido_detalle in pedido.detalles:
            total_pedido += pedido_detalle.cantidad * pedido_detalle.producto.precio
        return total_pedido

    # Definir las rutas y las funciones controladoras
    @pedido_blueprint.route('/pedidos')
    def listar():
        pedidos = db_session.query(Pedido).filter(Pedido.estado_id == 1).all()
        estado_pedido = db_session.query(PedidoEstado).all()

        for pedido in pedidos:
            pedido.total_pedido = calcular_total_pedido(pedido)

        return render_template('pedido/listar.html', pedidos=pedidos, estado_pedido=estado_pedido)

    @pedido_blueprint.route('/finalizados')
    def finalizados():
        pedidos = db_session.query(Pedido).filter(Pedido.estado_id == 2).all()
        estado_pedido = db_session.query(PedidoEstado).all()

        for pedido in pedidos:
            pedido.total_pedido = calcular_total_pedido(pedido)
        
        return render_template('pedido/finalizados.html', pedidos=pedidos, estado_pedido=estado_pedido)
    
    @pedido_blueprint.route('/anulados')
    def anulados():
        pedidos = db_session.query(Pedido).filter(Pedido.estado_id == 3).all()
        estado_pedido = db_session.query(PedidoEstado).all()

        for pedido in pedidos:
            pedido.total_pedido = calcular_total_pedido(pedido)

        return render_template('pedido/anulados.html', pedidos=pedidos, estado_pedido=estado_pedido)
    
    @pedido_blueprint.route('/nuevo', methods=['GET', 'POST'])
    def nuevo():
        pedido = Pedido(persona_id=1)
        db_session.add(pedido)
        db_session.commit()
        return redirect(url_for('pedido.editar', id=pedido.id))

    @pedido_blueprint.route('/pedido/editar/<int:id>', methods=['GET', 'POST'])
    def editar(id):
        pedido = db_session.query(Pedido).filter_by(id=id).one()
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
        
        for producto in productos:
            receta = db_session.query(Receta).filter_by(producto_id=producto.id).first()
            if receta:
                receta_detalles = db_session.query(RecetaDetalle).filter_by(receta_id=receta.id).all()
                ingredientes = [detalle.ingrediente for detalle in receta_detalles]
                producto.receta = receta
                producto.receta_detalles = receta_detalles
                producto.ingredientes = ingredientes
                producto.stock_disponible = producto.stock if not producto.tiene_receta else min([ingrediente.cantidad // detalle.cantidad for ingrediente, detalle in zip(ingredientes, receta_detalles)])
            else:
                producto.receta = None
                producto.receta_detalles = []
                producto.ingredientes = []
                producto.stock_disponible = producto.stock
        
        #if session['logged_in']:
        #    pedido = Pedido(persona_id=session['user_id'])
        #else:
        #    pedido = Pedido(persona_id=1)

        return render_template('pedido/editar.html', productos=productos, producto_busqueda=producto_busqueda, pedido=pedido)
    
    @pedido_blueprint.route('/agregar_producto/<int:id>', methods=['GET', 'POST'])
    def agregar_producto(id):
        pedido = db_session.query(Pedido).filter_by(id=id).one()
        
        if request.method == 'POST':
            producto_id = request.form.getlist('producto_id')  # Obtener una lista de los IDs de productos
            cantidades = request.form.getlist('cantidad')  # Obtener una lista de cantidades

            for producto_id, cantidad in zip(producto_id, cantidades):
                if producto_id and cantidad:
                    producto = db_session.query(Producto).filter_by(id=producto_id).first()  # Obtener el producto correspondiente

                    if not producto:
                        flash('El producto no existe', 'error')
                        return redirect(url_for('pedido.listar'))

                    producto_existente = db_session.query(PedidoDetalle).filter_by(pedido_id=pedido.id, producto_id=producto_id).all()
                    if producto_existente:
                        flash(f'El producto {producto.nombre} ya existe en la pedido, por lo que se han añadido {cantidades} unidades adicionales.', 'error')
                        producto_existente[0].cantidad += int(cantidad)
                        db_session.commit()
                        return redirect(url_for('pedido.editar', id=pedido.id))
                    
                    pedido_detalle = PedidoDetalle(pedido_id=id, producto_id=producto_id, cantidad=cantidad)
                    pedido.detalles.append(pedido_detalle)

            db_session.commit()

            flash('Producto agregado al pedido exitosamente', 'success')
            return redirect(url_for('pedido.editar', id=pedido.id))

        pedido_detalles = pedido.detalles  # Obtener todos los detalles del pedido
        return render_template('pedido/editar.html', pedido=pedido, pedido_detalles=pedido_detalles)
    
    @pedido_blueprint.route('/pedido/listar/<int:id>', methods=['POST'])
    def restaurar(id):
        pedido = db_session.query(Pedido).filter_by(id=id).one()
        pedido.estado_id = 1
        db_session.commit()
        return redirect(url_for('pedido.listar'))

    @pedido_blueprint.route('/pedido/finalizar/<int:id>', methods=['GET', 'POST'])
    def finalizar(id):
        pedido = db_session.query(Pedido).filter_by(id=id).one()
        if request.method == 'POST':
            pedido.estado_id = 2
            db_session.commit()
            return redirect(url_for('pedido.listar'))
        else:
            return render_template('pedido/finalizar.html', pedido=pedido)

    @pedido_blueprint.route('/pedido/anular/<int:id>', methods=['GET', 'POST'])
    def anular(id):
        pedido = db_session.query(Pedido).filter_by(id=id).one()
        if request.method == 'POST':
            pedido.estado_id = 3
            db_session.commit()
            return redirect(url_for('pedido.listar'))
        else:
            return render_template('pedido/anular.html', pedido=pedido)

    # Devolver el blueprint
    return pedido_blueprint