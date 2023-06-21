from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.database import Usuario, Pedido, PedidoEstado, Persona, Producto, Categoria, Receta, RecetaDetalle, PedidoDetalle, PedidoDetalleIngrediente, Ingrediente, db_session
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

    def actualizar_stock(producto, cantidad):
        receta = db_session.query(Receta).filter_by(producto_id=producto.id).first()
        receta_detalles = db_session.query(RecetaDetalle).filter_by(receta_id=receta.id).all()
        if producto.tiene_receta:
            receta = producto.receta
            receta_detalles = producto.receta_detalles
            for detalle in receta_detalles:
                ingrediente = detalle.ingrediente
                cantidad_necesaria = detalle.cantidad * cantidad
                ingrediente.cantidad -= cantidad_necesaria
        else:
            producto.stock -= cantidad

    # Definir las rutas y las funciones controladoras
    @pedido_blueprint.route('/pedidos')
    def listar():
        try:
            pedidos = db_session.query(Pedido).filter(Pedido.estado_id == 1).all()
            estado_pedido = db_session.query(PedidoEstado).all()

            for pedido in pedidos:
                pedido.total_pedido = calcular_total_pedido(pedido)
        except:
            db_session.rollback()

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
            productos = db_session.query(Producto).join(Categoria).filter(
                or_(Producto.nombre.ilike(f'%{producto_busqueda}%'),
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

        pedido.total_pedido = calcular_total_pedido(pedido)

        return render_template('pedido/editar.html', productos=productos, producto_busqueda=producto_busqueda, pedido=pedido)

    @pedido_blueprint.route('/actualizar_pedido/<int:id>', methods=['GET', 'POST'])
    def actualizar_pedido(id):
        pedido = db_session.query(Pedido).filter_by(id=id).one()

        if request.method == 'POST':
            producto_id = request.form.getlist('producto_id')  # Obtener una lista de los IDs de productos
            cantidades = request.form.getlist('cantidad')  # Obtener una lista de cantidades
            #stock = request.form.getlist('stock')
            unidades_preparables = request.form.getlist('unidades_preparables')
            action = request.form.get('action')
            test = int(unidades_preparables[0]) - int(cantidades[0])

            print(f'Preparables: {unidades_preparables} - {cantidades} = {test}')
            producto = db_session.query(Producto).filter_by(id=producto_id).first()

            if unidades_preparables >= cantidades or unidades_preparables <= cantidades:
                for producto_id, cantidad in zip(producto_id, cantidades):
                    if action == 'agregar':
                        producto_existente = db_session.query(PedidoDetalle).filter_by(pedido_id=pedido.id,
                                                                                        producto_id=producto.id).all()
                        
                        if producto_existente and producto.tiene_receta is False:
                            flash(f'El producto "{producto.nombre} ({producto.categoria.nombre})" ya existe en la pedido, por lo que se ha(n) añadido {int(cantidades[0])} unidad(es) adicional(es).', 'error')
                            for pedido_detalle in producto_existente:
                                pedido_detalle.cantidad += int(cantidad)
                                if producto.tiene_receta:
                                    receta = db_session.query(Receta).filter_by(producto_id=producto.id).first()
                                    receta_detalles = db_session.query(RecetaDetalle).filter_by(receta_id=receta.id).all()
                                    for detalle in receta_detalles:
                                        ingrediente = detalle.ingrediente
                                        cantidad_necesaria = detalle.cantidad * int(cantidad)
                                        ingrediente.cantidad -= cantidad_necesaria
                                else:
                                    producto.stock -= int(cantidad)
                        else:
                            flash(f'Se ha añadido una unidad de "{producto.nombre} ({producto.categoria.nombre})" al pedido.', 'error')
                            pedido_detalle = PedidoDetalle(pedido_id=pedido.id, producto_id=producto_id,
                                                        cantidad=int(cantidad))

                            if producto.tiene_receta:
                                receta = db_session.query(Receta).filter_by(producto_id=producto.id).first()
                                receta_detalles = db_session.query(RecetaDetalle).filter_by(receta_id=receta.id).all()
                                for detalle in receta_detalles:
                                    ingrediente = detalle.ingrediente
                                    cantidad_necesaria = detalle.cantidad * int(cantidad)
                                    ingrediente.cantidad -= cantidad_necesaria
                            else:
                                producto.stock -= int(cantidad)

                            db_session.add(pedido_detalle)
                            return redirect(url_for('pedido.editar', id=pedido.id))
                    
                    if action == 'quitar':
                        pedido_detalle = db_session.query(PedidoDetalle).filter_by(pedido_id=pedido.id, producto_id=producto_id).first()
                        cantidad = int(cantidad)
                        if pedido_detalle is None or pedido_detalle.cantidad is None:
                            flash(f'No existe el producto "{ producto.nombre }" en el pedido.', 'error')
                            return redirect(url_for('pedido.editar', id=pedido.id))

                        if pedido_detalle.cantidad is not None and cantidad >= pedido_detalle.cantidad:
                            db_session.delete(pedido_detalle)
                            if producto.tiene_receta:
                                receta = db_session.query(Receta).filter_by(producto_id=producto.id).first()
                                receta_detalles = db_session.query(RecetaDetalle).filter_by(receta_id=receta.id).all()
                                for detalle in receta_detalles:
                                    ingrediente = detalle.ingrediente
                                    cantidad_necesaria = detalle.cantidad * pedido_detalle.cantidad
                                    ingrediente.cantidad += cantidad_necesaria
                            else:
                                producto.stock += pedido_detalle.cantidad
                        else:
                            pedido_detalle.cantidad -= cantidad
                            if producto.tiene_receta:
                                receta = db_session.query(Receta).filter_by(producto_id=producto.id).first()
                                receta_detalles = db_session.query(RecetaDetalle).filter_by(receta_id=receta.id).all()
                                for detalle in receta_detalles:
                                    ingrediente = detalle.ingrediente
                                    cantidad_necesaria = detalle.cantidad * cantidad
                                    ingrediente.cantidad += cantidad_necesaria
                            else:
                                producto.stock += cantidad

                db_session.commit()

            else:
                flash(f'No hay stock suficiente para agregar { producto.nombre } al pedido.', 'error')

            return redirect(url_for('pedido.editar', id=pedido.id))

        return redirect(url_for('pedido.editar', id=pedido.id))
    
    @pedido_blueprint.route('/pedido/editar_extra/<int:id>', methods=['GET', 'POST'])
    def editar_extra(id):
        detalle_pedido = db_session.query(PedidoDetalle).filter_by(id=id).one()
        ingrediente = db_session.query(Ingrediente).filter(Ingrediente.activo == True).all()

        if request.method == 'POST':
            action = request.form.get('action')
            cantidad = request.form.getlist('cantidad')

        return render_template('pedido/editar_extra.html', detalle_pedido=detalle_pedido, ingrediente=ingrediente)
    
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