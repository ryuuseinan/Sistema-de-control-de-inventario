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

    # Definir las rutas y las funciones controladoras
    @pedido_blueprint.route('/pedidos')
    def listar():
        persona = db_session.query(Usuario).all()
        usuario = db_session.query(Usuario).all()
        pedidos = db_session.query(Pedido).all()
        estado_pedido = db_session.query(PedidoEstado).all()
        
        return render_template('pedido/listar.html', pedidos=pedidos, usuario=usuario, estado_pedido=estado_pedido)

    @pedido_blueprint.route('/nuevo', methods=['GET', 'POST'])
    def nuevo():
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
        
        pedido = Pedido(usuario_id=1)
        db_session.add(pedido)
        db_session.commit()

        return render_template('pedido/nuevo.html', productos=productos, producto_busqueda=producto_busqueda)
    
    @pedido_blueprint.route('/agregar_producto/<int:id>', methods=['GET', 'POST'])
    def agregar_producto(id):
        
        usuario = db_session.query(Usuario).filter_by(id=id).one()

        if not db_session.query(Pedido).filter_by(id=id).first():
            pedido = Pedido(id=id, usuario_id=id)
            db_session.add(pedido)
            db_session.commit()
        else:
            pedido = db_session.query(Pedido).filter_by(id=id).one()
        
        pedido_detalles = pedido.detalles  # Obtener todos los detalles de la pedido

        if not producto:
            flash('El producto no existe', 'error')
            return redirect(url_for('pedido.listar'))

        if request.method == 'POST':
            # Obtener los producto y cantidades desde el formulario
            producto = request.form.getlist('producto')
            cantidades = request.form.getlist('cantidad')

            # Agregar los producto y cantidades a la pedido
            for producto_id, cantidad in zip(producto, cantidades):
                if producto_id and cantidad:
                    pedido_detalle = PedidoDetalle(producto_id=producto_id, cantidad=cantidad)
                    pedido.detalles.append(pedido_detalle)

            db_session.commit()

            flash('Ingrediente agregado al producto exitosamente', 'success')
            return redirect(url_for('pedido.listar', id=producto.id))

        return render_template('pedido/listar.html', producto=producto, usuario=usuario, pedido=pedido, pedido_detalles=pedido_detalles)


    @pedido_blueprint.route('/pedidos/papelera')
    def papelera():
        rol = db_session.query(Rol).filter(Rol.activo == True).all()
        pedidos = db_session.query(pedido).filter(pedido.activo == False).all()
        return render_template('pedido/papelera.html', pedidos=pedidos)

    @pedido_blueprint.route('/pedido/restaurar/<int:id>', methods=['GET', 'POST'])
    def restaurar(id):
        rol = db_session.query(Rol).filter(Rol.activo == True).all()
        pedido = db_session.query(pedido).filter_by(id=id).one()
        if request.method == 'POST':
            pedido.activo = True
            db_session.commit()
            return redirect(url_for('pedido.listar'))
        else:
            return render_template('pedido/restaurar.html', pedido=pedido)

    @pedido_blueprint.route('/pedido/editar/<int:id>', methods=['GET', 'POST'])
    def editar(id):
        rol = db_session.query(Rol).filter(Rol.activo == True).all()
        pedido = db_session.query(pedido).get(id)

        if not pedido:
            flash('El pedido no existe', 'error')
            return redirect(url_for('pedido.listar'))

        if request.method == 'POST':
            nombre_pedido = request.form['nombre_pedido']
            correo = request.form['correo']
            contrasena = request.form['contrasena']
            confirmar_contrasena = request.form['confirmar_contrasena']
            rol_id = request.form['rol_id']
            
            # Validar formulario
            if not nombre_pedido:
                flash('El nombre de pedido es requerido', 'error')
            elif not correo:
                flash('El correo electrónico es requerido', 'error')
            elif contrasena != confirmar_contrasena:
                flash('Las contraseñas no coinciden', 'error')
            else:
                # Actualizar pedido
                pedido.nombre_pedido = nombre_pedido
                pedido.correo = correo
                pedido.rol_id = rol_id
                if contrasena:
                    contrasena_hash = bcrypt.hashpw(contrasena.encode(), bcrypt.gensalt())
                    pedido.contrasena = contrasena_hash
                pedido.ultima_modificacion = datetime.now()
                db_session.commit()
                
                flash('pedido actualizado exitosamente', 'success')
                return redirect(url_for('pedido.listar'))
        return render_template('pedido/editar.html', pedido=pedido, rol=rol)

    @pedido_blueprint.route('/pedido/eliminar/<int:id>', methods=['GET', 'POST'])
    def eliminar(id):
        pedido = db_session.query(pedido).filter_by(id=id).one()
        if request.method == 'POST':
            pedido.activo = False
            db_session.commit()
            return redirect(url_for('pedido.listar'))
        else:
            return render_template('pedido/eliminar.html', pedido=pedido)
        
    
    # Devolver el blueprint
    return pedido_blueprint