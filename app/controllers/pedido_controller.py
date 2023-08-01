from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.database import Pedido, PedidoEstado, Producto, Categoria, Receta, RecetaDetalle, PedidoDetalle, PedidoDetalleIngrediente, Ingrediente, MetodoPago, Venta, db_session
from datetime import datetime
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
import arrow

pedido_controller = Blueprint('pedido_controller', __name__)
def create_pedido_blueprint():
    # Crear el objeto Blueprint
    pedido_blueprint = Blueprint('pedido', __name__)

    def calcular_total_pedido(pedido):
        total_pedido = 0
        for pedido_detalle in pedido.detalles:
            total_pedido += pedido_detalle.cantidad * pedido_detalle.producto.precio

        # Sumar el precio de los ingredientes adicionales
        pedido_detalle_ingredientes = db_session.query(PedidoDetalleIngrediente).join(PedidoDetalle).join(Pedido).filter(
            PedidoDetalle.pedido_id == pedido.id).all()
        
        for detalle_ingrediente in pedido_detalle_ingredientes:
            #total_pedido += detalle_ingrediente.ingrediente.precio # Calcular apartir de la tabla Ingredientes
            total_pedido += detalle_ingrediente.precio # Calcular apartir de la tabla PedidoDetalleIngrediente del producto

        return total_pedido

    # Definir las rutas y las funciones controladoras
    @pedido_blueprint.route('/pedidos')
    def listar():
        try:
            pedidos = db_session.query(Pedido).filter(Pedido.estado_id == 1).order_by(Pedido.id).limit(25).all()
            estado_pedido = db_session.query(PedidoEstado).all()
            pedido_detalle_ingredientes = db_session.query(PedidoDetalleIngrediente).join(PedidoDetalle).join(Pedido).filter(Pedido.estado_id == 2).all()

            for pedido in pedidos:
                pedido.total_pedido = calcular_total_pedido(pedido)
        
        except:
            print("ERROR DESCONOCIDO: informe con el desarrollador sobre este problema.")
            db_session.rollback()
            return redirect(request.path)

        return render_template('pedido/listar.html', pedidos=pedidos, 
                               estado_pedido=estado_pedido, 
                               pedido_detalle_ingredientes=pedido_detalle_ingredientes)

    @pedido_blueprint.route('/finalizados')
    def finalizados():
        try:
            pedidos = db_session.query(Pedido).filter(Pedido.estado_id == 2).order_by(Pedido.id.desc()).limit(25).all()
            estado_pedido = db_session.query(PedidoEstado).all()
            pedido_detalle_ingredientes = db_session.query(PedidoDetalleIngrediente).join(PedidoDetalle).join(Pedido).filter(Pedido.estado_id == 2).all()

            for pedido in pedidos:
                pedido.total_pedido = calcular_total_pedido(pedido)
        
        except:
            print("ERROR DESCONOCIDO: informe con el desarrollador sobre este problema.")
            db_session.rollback()
            return redirect(request.path)

        return render_template('pedido/finalizados.html', pedidos=pedidos, estado_pedido=estado_pedido, pedido_detalle_ingredientes=pedido_detalle_ingredientes)

    @pedido_blueprint.route('/anulados')
    def anulados():
        try:
            pedidos = db_session.query(Pedido).filter(Pedido.estado_id == 3).order_by(Pedido.id.desc()).limit(25).all()
            estado_pedido = db_session.query(PedidoEstado).all()
            pedido_detalle_ingredientes = db_session.query(PedidoDetalleIngrediente).join(PedidoDetalle).join(Pedido).filter(Pedido.estado_id == 3).all()

            for pedido in pedidos:
                pedido.total_pedido = calcular_total_pedido(pedido)
        
        except:
            print("ERROR DESCONOCIDO: informe con el desarrollador sobre este problema.")
            db_session.rollback()
            return redirect(request.path)

        return render_template('pedido/anulados.html', pedidos=pedidos, estado_pedido=estado_pedido, pedido_detalle_ingredientes=pedido_detalle_ingredientes)

    @pedido_blueprint.route('/nuevo', methods=['GET', 'POST'])
    def nuevo():
        try:
            if 'id' not in session:
                flash("ERROR: Debes haber iniciado sesión para esta función.")
                return redirect(url_for('sesion.login'))
            
            else:
                pedido = Pedido(persona_id=session['id'])
                db_session.add(pedido)
                db_session.commit()
                return redirect(url_for('pedido.editar', id=pedido.id))
        
        except:
            db_session.rollback()
            flash("ERROR: Ocurrió un error al procesar la solicitud.")
            return redirect(url_for('sesion.login'))

    @pedido_blueprint.route('/pedido/actualizar_datos/<int:id>', methods=['GET', 'POST'])
    def actualizar_datos(id):
        pedido = db_session.query(Pedido).filter_by(id=id).one()
        try:
            pedido = db_session.query(Pedido).filter_by(id=id).one()
            nombre_cliente = request.form['nombre_cliente']
            delivery = True if request.form['delivery'] == "True" else False
            metodopago_id = request.form['metodopago_id']
            metodopago = db_session.query(MetodoPago).filter_by(id=metodopago_id).first()
            if metodopago_id:
                pedido.metodopago = metodopago
            if nombre_cliente:
                pedido.nombre_cliente = nombre_cliente
            pedido.delivery = delivery
            db_session.commit()
            flash('Se han actualizado los datos del pedido de forma exitosa.')
        except:
            flash('Hubo un error en actualizar los datos del pedido, vuelva a intentarlo.')
        return redirect(url_for('pedido.editar', id=pedido.id))
            
    @pedido_blueprint.route('/pedido/editar/<int:id>', methods=['GET', 'POST'])
    def editar(id):
        pedido = db_session.query(Pedido).filter_by(id=id).one()
        producto_busqueda = request.form.get('producto_busqueda')

        metodopago = db_session.query(MetodoPago).filter(MetodoPago.activo == True).all()
        if request.method == 'POST' and producto_busqueda:
            productos = db_session.query(Producto).join(Categoria).filter(
                or_(Producto.nombre.ilike(f'%{producto_busqueda}%'),
                    Categoria.nombre.ilike(f'%{producto_busqueda}%')),
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
                        [ingrediente.cantidad // detalle.cantidad for ingrediente, detalle in zip(ingredientes, receta_detalles)],
                        default=0
                    )
                )

            else:
                producto.receta = None
                producto.receta_detalles = []
                producto.ingredientes = []
                producto.stock_disponible = producto.stock

        pedido.total_pedido = calcular_total_pedido(pedido)

        pedido_detalle_ingredientes = db_session.query(PedidoDetalleIngrediente).join(PedidoDetalle).join(Pedido).all()
        detalle_pedido = db_session.query(PedidoDetalle).filter_by(pedido_id=pedido.id).first()

        if detalle_pedido is not None:
            detalle_ingredientes_producto = db_session.query(PedidoDetalleIngrediente).filter_by(
                pedido_detalle_id=detalle_pedido.id).all()
        else:
            detalle_ingredientes_producto = []
            
        return render_template('pedido/editar.html', productos=productos, metodopago=metodopago,
                            producto_busqueda=producto_busqueda, pedido=pedido,
                            pedido_detalle_ingredientes=pedido_detalle_ingredientes, 
                            detalle_ingredientes_producto=detalle_ingredientes_producto)

    @pedido_blueprint.route('/agregar_producto/<int:id>', methods=['POST'])
    def agregar_producto(id):
        pedido = db_session.query(Pedido).filter_by(id=id).one()
        producto_id = request.form.getlist('producto_id')  # Obtener una lista de los IDs de productos
        cantidades = request.form.getlist('cantidad')  # Obtener una lista de cantidades
        unidades_preparables = request.form.getlist('unidades_preparables')
        print(request.form)
        print(f'Preparables: {unidades_preparables} - {cantidades}')
        test = int(unidades_preparables[0]) - int(cantidades[0])

        print(f'Preparables: {unidades_preparables} - {cantidades} = {test}')
        producto = db_session.query(Producto).filter_by(id=producto_id).first()

        if unidades_preparables >= cantidades or unidades_preparables <= cantidades:
            for producto_id, cantidad in zip(producto_id, cantidades):
                producto_existente = db_session.query(PedidoDetalle).filter_by(pedido_id=pedido.id,
                                                                                producto_id=producto.id).all()

                if producto_existente and producto.tiene_receta is False:
                    flash(f'El producto "{producto.nombre} ({producto.categoria.nombre})" ya existe en la pedido, por lo que se ha(n) añadido {int(cantidades[0])} unidad(es) adicional(es).', 'error')
                    for pedido_detalle in producto_existente:
                        pedido_detalle.cantidad += int(cantidad)

                else:
                    pedido_detalle = PedidoDetalle(pedido_id=pedido.id, producto_id=producto_id,
                                                    cantidad=int(cantidad))

                    if producto.tiene_receta:
                        receta = db_session.query(Receta).filter_by(producto_id=producto.id).first()
                        if receta is not None:
                            receta_detalles = db_session.query(RecetaDetalle).filter_by(receta_id=receta.id).all()
                            for detalle in receta_detalles:
                                ingrediente = detalle.ingrediente
                                cantidad_necesaria = detalle.cantidad * int(cantidad)
                                ingrediente.cantidad -= cantidad_necesaria
                        else:
                            flash(f'El producto "{producto.nombre} ({producto.categoria.nombre})" no tiene una receta asociada.', 'warning')
                            return redirect(url_for('pedido.editar', id=pedido.id))
                    else:
                        producto.stock -= int(cantidad)

                    db_session.add(pedido_detalle)
                    db_session.commit()
                    flash(f'Se ha añadido una unidad de "{producto.nombre} ({producto.categoria.nombre})" al pedido.', 'error')
        else:
            flash(f'No hay stock suficiente para agregar { producto.nombre } al pedido.', 'error')
        
        return redirect(url_for('pedido.editar', id=pedido.id))

    @pedido_blueprint.route('/quitar_producto/<int:id>', methods=['POST'])
    def quitar_producto(id):

        pedido = db_session.query(Pedido).filter_by(id=id).one()
        producto_id = request.form.getlist('producto_id')  # Obtener una lista de los IDs de productos
        cantidades = request.form.getlist('cantidad')  # Obtener una lista de cantidades

        print(f'Eliminar: {cantidades}')
        producto = db_session.query(Producto).filter_by(id=producto_id).first()

        for producto_id, cantidad in zip(producto_id, cantidades):
            pedido_detalle = db_session.query(PedidoDetalle).filter_by(pedido_id=pedido.id, producto_id=producto_id).first()
            cantidad = int(cantidad)
            if pedido_detalle is None or pedido_detalle.cantidad is None:
                flash(f'No existe el producto "{ producto.nombre }" en el pedido.', 'error')
                return redirect(url_for('pedido.editar', id=pedido.id))

            if pedido_detalle.cantidad is not None and cantidad >= pedido_detalle.cantidad:
                detalles_ingrediente = db_session.query(PedidoDetalleIngrediente).filter_by(pedido_detalle_id=pedido_detalle.id).all()
                db_session.query(PedidoDetalleIngrediente).filter_by(pedido_detalle_id=pedido_detalle.id).delete()

                for detalle_ingrediente in detalles_ingrediente:
                    ingrediente = detalle_ingrediente.ingrediente
                    cantidad_eliminada = detalle_ingrediente.cantidad
                    ingrediente.cantidad += cantidad_eliminada

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
        return redirect(url_for('pedido.editar', id=pedido.id))

    @pedido_blueprint.route('/pedido/editar_extra/<int:id>', methods=['GET', 'POST'])
    def editar_extra(id):
        try:
            pedido_detalle = db_session.query(PedidoDetalle).filter_by(id=id).one()
            pedido_detalle_ingrediente = db_session.query(PedidoDetalleIngrediente).filter_by(pedido_detalle_id=id).all()
            total_pedido = pedido_detalle.producto.precio
            ingrediente_busqueda = request.form.get('ingrediente_busqueda')
            
            if request.method == 'POST' and ingrediente_busqueda:
                ingrediente = db_session.query(Ingrediente).filter(Ingrediente.nombre.ilike(f'%{ingrediente_busqueda}%'), Ingrediente.activo == True).all()
                if not ingrediente:
                    flash("No se encontraron ingredientes con ese criterio de búsqueda", "error")
                    ingrediente = db_session.query(Ingrediente).filter(Ingrediente.activo == True, Ingrediente.precio > 0).order_by(Ingrediente.nombre).all()

            elif request.method == 'POST' and not ingrediente_busqueda:
                flash("Por favor, ingrese el nombre de un ingrediente", "error")
                ingrediente = db_session.query(Ingrediente).filter(Ingrediente.activo == True, Ingrediente.precio > 0).order_by(Ingrediente.nombre).all()
            else:
                ingrediente = db_session.query(Ingrediente).filter(Ingrediente.activo == True, Ingrediente.precio > 0).order_by(Ingrediente.nombre).all()

            for detalle_ingrediente in pedido_detalle_ingrediente:
                total_pedido += detalle_ingrediente.precio
                print(total_pedido)
        
        except:
            print("ERROR DESCONOCIDO: informe con el desarrollador sobre este problema.")
            db_session.rollback()
            return redirect(request.path)
            
        return render_template('pedido/editar_extra.html', ingrediente=ingrediente, pedido_detalle=pedido_detalle, pedido_detalle_ingrediente=pedido_detalle_ingrediente, total_pedido=total_pedido, ingrediente_busqueda=ingrediente_busqueda)

    @pedido_blueprint.route('/pedido/agregar_extra/<int:id>', methods=['GET', 'POST'])
    def agregar_extra(id):
        try:
            pedido_detalle_ingrediente = db_session.query(PedidoDetalleIngrediente).filter_by(id=id).first()
            pedido_detalle = db_session.query(PedidoDetalle).filter_by(id=id).one()
            extra_mediana = request.form.get('extra_mediana')
            extra_familiar = request.form.get('extra_familiar')
            precio = request.form.get('precio')
            ingrediente_id = request.form.getlist('ingrediente_id')

            ingrediente = db_session.query(Ingrediente).filter_by(id=ingrediente_id).first()
            print(ingrediente)

            if extra_mediana is None:
                extra_mediana = 0
            else:
                extra = extra_mediana

            if extra_familiar is None:
                extra_familiar = 0
            else:
                extra = extra_familiar
                
            extra_mediana = int(extra_mediana)
            extra_familiar = int(extra_familiar)
            print(extra_mediana)
            print(extra_familiar)
            print(extra)

            if int(extra) >= 1 and int(extra) <= ingrediente.cantidad:
                nuevo_pedido_detalle_ingrediente = PedidoDetalleIngrediente(
                    pedido_detalle_id=pedido_detalle.id,
                    ingrediente_id=ingrediente_id,
                    cantidad=extra,
                    precio=precio)
                print(ingrediente_id)
                ingrediente_id = int(ingrediente_id[0])
                print(ingrediente_id)
                ingrediente.cantidad -= int(extra)
                db_session.add(nuevo_pedido_detalle_ingrediente)
                db_session.commit()
                flash(f'Se ha(n) añadido {extra} {ingrediente.unidadmedida.nombre} de "{ingrediente.nombre}" al producto.', 'error')

            else:
                flash(f'No hay stock suficiente.', 'error')

            return redirect(url_for('pedido.editar_extra', id=id))
        
        except:
            print("ERROR DESCONOCIDO: informe con el desarrollador sobre este problema.")
            db_session.rollback()
            return redirect(request.path)
            
        return redirect(url_for('pedido.editar', id=pedido_detalle.pedido_id))

    @pedido_blueprint.route('/pedido/eliminar_extra/<int:id>', methods=['GET', 'POST'])
    def eliminar_extra(id):
        try:
            pedido_detalle_ingrediente = db_session.query(PedidoDetalleIngrediente).filter_by(id=id).first()

            if pedido_detalle_ingrediente:
                cantidad_eliminar = pedido_detalle_ingrediente.cantidad
                ingrediente = db_session.query(Ingrediente).filter_by(id=pedido_detalle_ingrediente.ingrediente_id).first()

                if ingrediente:
                    db_session.delete(pedido_detalle_ingrediente)
                    ingrediente.cantidad += cantidad_eliminar
                    db_session.commit()
                    flash('El registro se eliminó correctamente.', 'success')
                else:
                    flash('No se encontró el ingrediente asociado al registro.', 'error')
            else:
                flash('No se encontró el registro en el detalle.', 'error')
        
        except:
            print("ERROR DESCONOCIDO: informe con el desarrollador sobre este problema.")
            db_session.rollback()
            return redirect(request.path)

        return redirect(url_for('pedido.editar_extra', id=pedido_detalle_ingrediente.pedido_detalle_id))

    @pedido_blueprint.route('/restaurar_finalizado/<int:id>', methods=['GET', 'POST'])
    def restaurar_finalizado(id):
        try:
            pedido = db_session.query(Pedido).filter_by(id=id).one()

            if pedido.estado_id == 2:  # Verificar si el pedido está finalizado
                venta_existente = db_session.query(Venta).filter_by(id=id).first()
                
                if venta_existente:
                    venta_existente.activo = False

                pedido.estado_id = 1  
                pedido.notificacion = True
                db_session.commit()
                flash(f'El pedido {id} se ha marcado como "en progreso" correctamente.', 'success')
            else:
                flash(f'El pedido {id} no se encuentra finalizado.', 'error')
        
        except:
            print("ERROR DESCONOCIDO: informe con el desarrollador sobre este problema.")
            db_session.rollback()
            return redirect(request.path)
            
        pagina = request.form.get('pagina')
        if pagina == 'notificaciones':
            return redirect(url_for('pedido.notificaciones'))
        else:
            return redirect(url_for('pedido.finalizados'))

    @pedido_blueprint.route('/restaurar/<int:id>', methods=['GET', 'POST'])
    def restaurar(id):
        try:
            pedido = db_session.query(Pedido).filter_by(id=id).one()

            if pedido.estado_id == 3:  # Verificar si el pedido está anulado previamente
                pedido.estado_id = 1  # Actualizar el estado del pedido a "En proceso"
                pedido.notificacion = True
                # Descontar ingredientes nuevamente basándose en la receta de cada producto en el pedido
                for detalle in pedido.detalles:
                    producto = detalle.producto

                    if producto.tiene_receta:
                        receta = db_session.query(Receta).filter_by(producto_id=producto.id).first()
                        receta_detalles = db_session.query(RecetaDetalle).filter_by(receta_id=receta.id).all()

                        for detalle_receta in receta_detalles:
                            ingrediente = detalle_receta.ingrediente
                            cantidad_necesaria = detalle_receta.cantidad * detalle.cantidad

                            # Descontar la cantidad de ingredientes en base a la receta
                            ingrediente.cantidad -= cantidad_necesaria

                            # Sumar los ingredientes de pedido_detalle_ingrediente

                pedido_detalle_ingredientes = db_session.query(PedidoDetalleIngrediente).join(PedidoDetalle).join(Pedido).filter(
                    PedidoDetalle.pedido_id == pedido.id).all()

                for detalle_ingrediente in pedido_detalle_ingredientes:
                    ingrediente = detalle_ingrediente.ingrediente
                    cantidad = detalle_ingrediente.cantidad

                    # Sumar la cantidad de ingredientes
                    ingrediente.cantidad -= cantidad

                db_session.commit()
                flash(f'El pedido {id} se ha restaurado correctamente.', 'success')
            else:
                flash(f'El pedido {id} no se encuentra anulado.', 'error')
        
        except:
            print("ERROR DESCONOCIDO: informe con el desarrollador sobre este problema.")
            db_session.rollback()
            return redirect(request.path)

        return redirect(url_for('pedido.anulados'))

    @pedido_blueprint.route('/finalizar/<int:id>', methods=['GET', 'POST'])
    def finalizar(id):
        try:
            pedido = db_session.query(Pedido).filter_by(id=id).one()
            pedido.estado_id = 2  # Actualizar el estado del pedido a "Finalizado"
            pedido.notificacion = False

            # Descontar ingredientes basándose en la receta de cada producto en el pedido
            for detalle in pedido.detalles:
                producto = detalle.producto

                if producto.tiene_receta:
                    receta = db_session.query(Receta).filter_by(producto_id=producto.id).first()
                    receta_detalles = db_session.query(RecetaDetalle).filter_by(receta_id=receta.id).all()

                    for detalle_receta in receta_detalles:
                        ingrediente = detalle_receta.ingrediente
                        cantidad_necesaria = detalle_receta.cantidad * detalle.cantidad

                        # Descontar la cantidad de ingredientes en base a la receta
                        ingrediente.cantidad -= cantidad_necesaria

                        # Sumar los ingredientes de pedido_detalle_ingrediente

            pedido_detalle_ingredientes = db_session.query(PedidoDetalleIngrediente).join(PedidoDetalle).join(Pedido).filter(
                PedidoDetalle.pedido_id == pedido.id).all()

            for detalle_ingrediente in pedido_detalle_ingredientes:
                ingrediente = detalle_ingrediente.ingrediente
                cantidad = detalle_ingrediente.cantidad

                # Sumar la cantidad de ingredientes
                ingrediente.cantidad -= cantidad

            venta_existente = db_session.query(Venta).filter_by(id=id).first()

            pedido.total_pedido = calcular_total_pedido(pedido)
            
            if venta_existente:
                venta_existente.total = pedido.total_pedido
                venta_existente.activo = True

            else:
                nueva_venta = Venta(id=id,
                                    pedido_id=id, 
                                    total=pedido.total_pedido)
                db_session.add(nueva_venta)

            db_session.commit()
            flash(f'El pedido {id} se ha finalizado correctamente.', 'success')
        
        except:
            print("ERROR DESCONOCIDO: informe con el desarrollador sobre este problema.")
            db_session.rollback()
            return redirect(request.path)

        pagina = request.form.get('pagina')
        if pagina == 'notificaciones':
            return redirect(url_for('pedido.notificaciones'))
        else:
            return redirect(url_for('pedido.listar'))

    @pedido_blueprint.route('/anular/<int:id>', methods=['GET', 'POST'])
    def anular(id):
        try:
            pedido = db_session.query(Pedido).filter_by(id=id).one()
            pedido.estado_id = 3  # Actualizar el estado del pedido a "Anulado"
            pedido.notificacion = False
            # Sumar ingredientes basándose en la receta de cada producto en el pedido
            for detalle in pedido.detalles:
                producto = detalle.producto

                if producto.tiene_receta:
                    receta = db_session.query(Receta).filter_by(producto_id=producto.id).first()
                    receta_detalles = db_session.query(RecetaDetalle).filter_by(receta_id=receta.id).all()

                    for detalle_receta in receta_detalles:
                        ingrediente = detalle_receta.ingrediente
                        cantidad_necesaria = detalle_receta.cantidad * detalle.cantidad

                        # Sumar la cantidad de ingredientes en base a la receta
                        ingrediente.cantidad += cantidad_necesaria

                        # Restar los ingredientes de pedido_detalle_ingrediente

            pedido_detalle_ingredientes = db_session.query(PedidoDetalleIngrediente).join(PedidoDetalle).join(Pedido).filter(
                PedidoDetalle.pedido_id == pedido.id).all()

            for detalle_ingrediente in pedido_detalle_ingredientes:
                ingrediente = detalle_ingrediente.ingrediente
                cantidad = detalle_ingrediente.cantidad

                # Restar la cantidad de ingredientes
                ingrediente.cantidad += cantidad

            venta_existente = db_session.query(Venta).filter_by(id=id).first()

            pedido.total_pedido = calcular_total_pedido(pedido)

            if venta_existente:
                venta_existente.total = pedido.total_pedido
                venta_existente.activo = False

            db_session.commit()
            flash(f'El pedido {id} se ha anulado correctamente.', 'success')
        
        except:
            print("ERROR DESCONOCIDO: informe con el desarrollador sobre este problema.")
            db_session.rollback()
            return redirect(request.path)

        pagina = request.form.get('pagina')
        if pagina == 'notificaciones':
            return redirect(url_for('pedido.notificaciones'))
        else:
            return redirect(url_for('pedido.listar'))
    
    @pedido_blueprint.route('/notificaciones')
    def notificaciones():
        try:
            pedidos = db_session.query(Pedido).filter(Pedido.notificacion == True).all()
            estado_pedido = db_session.query(PedidoEstado).all()
            pedido_detalle_ingredientes = db_session.query(PedidoDetalleIngrediente).join(PedidoDetalle).join(Pedido).filter(Pedido.estado_id == 1).all()
            
            detalle_pedido = None
            detalle_ingredientes_producto = []
            
            if pedidos and pedidos[0].detalles:
                detalle_pedido = pedidos[0].detalles[0]
                detalle_ingredientes_producto = db_session.query(PedidoDetalleIngrediente).filter_by(pedido_detalle_id=detalle_pedido.id).all()

        except SQLAlchemyError as e:
            # Revertir la transacción en caso de error
            db_session.rollback()
            print(f"Error al obtener los pedidos: {e}")
            # Manejar el error de alguna manera, como mostrar un mensaje de error al usuario
            return render_template('error.html', error_message="Error al obtener los pedidos")

        return render_template('notificaciones.html', pedidos=pedidos, 
                               estado_pedido=estado_pedido, 
                               pedido_detalle_ingredientes=pedido_detalle_ingredientes, 
                               detalle_ingredientes_producto=detalle_ingredientes_producto)
    
    @pedido_blueprint.route('/notificaciones_papelera')
    def notificaciones_papelera():
        try:
            pedidos = db_session.query(Pedido).filter(Pedido.notificacion == False).order_by(-Pedido.id).all()
            
            estado_pedido = db_session.query(PedidoEstado).all()
            pedido_detalle_ingredientes = db_session.query(PedidoDetalleIngrediente).join(PedidoDetalle).join(Pedido).filter(Pedido.estado_id == 1).all()
            
            detalle_pedido = None
            detalle_ingredientes_producto = []
            
            if pedidos and pedidos[0].detalles:
                detalle_pedido = pedidos[0].detalles[0]
                detalle_ingredientes_producto = db_session.query(PedidoDetalleIngrediente).filter_by(pedido_detalle_id=detalle_pedido.id).all()

        except:
            print("ERROR DESCONOCIDO: informe con el desarrollador sobre este problema.")
            db_session.rollback()
            return redirect(request.path)
        
        return render_template('notificaciones_papelera.html', pedidos=pedidos, 
                               estado_pedido=estado_pedido, 
                               pedido_detalle_ingredientes=pedido_detalle_ingredientes, 
                               detalle_ingredientes_producto=detalle_ingredientes_producto)
    
    @pedido_blueprint.route('/notificar/<int:id>', methods=['GET', 'POST'])
    def notificar(id):
        try:
            pedido = db_session.query(Pedido).filter_by(id=id).one()
            pedido.notificacion = True
            db_session.commit()
            return redirect(url_for('pedido.listar'))
        
        except:
            print("ERROR DESCONOCIDO: informe con el desarrollador sobre este problema.")
            db_session.rollback()
            return redirect(request.path)
        
    return pedido_blueprint
