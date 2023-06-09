from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.database import Usuario, Pedido, PedidoEstado, Persona, db_session
import bcrypt, arrow
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
        for pedido in pedidos:
            fecha_creacion = arrow.get(usuario.fecha_creacion).to('America/Santiago').format('DD-MM-YYYY HH:mm') if usuario.fecha_creacion else None
            ultima_modificacion = arrow.get(usuario.ultima_modificacion).to('America/Santiago').format('DD-MM-YYYY HH:mm') if usuario.ultima_modificacion else None
        return render_template('pedido/listar.html', pedidos=pedidos, usuario=usuario, estado_pedido=estado_pedido)

    @pedido_blueprint.route('/pedido/nuevo', methods=['GET', 'POST'])
    def nueva():
        error = None
        usuario = db_session.query(Usuario).all()
        rol = db_session.query(Rol).filter(Rol.activo == True).all()
        if request.method == 'POST':
            nombre_pedido = request.form['nombre_pedido']
            correo = request.form['correo']
            contrasena = request.form['contrasena']
            confirmar_contrasena = request.form['confirmar_contrasena']
            rol_id = request.form['rol_id']

            if contrasena != confirmar_contrasena:
                error = "Las contraseñas no coinciden"
            else:
                contrasena_hash = bcrypt.hashpw(contrasena.encode(), bcrypt.gensalt())
                pedido = pedido(nombre_pedido=nombre_pedido, correo=correo, contrasena=contrasena_hash, rol_id=rol_id)
                try:
                    db_session.add(pedido)
                    db_session.commit()
                    flash('El pedido ha sido creado exitosamente.', 'success')
                    return redirect(url_for('pedido.listar'))
                except IntegrityError:
                    db_session.rollback()
                    error = "El nombre de pedido o correo electrónico ya están en uso"
        return render_template('pedido/nuevo.html', error=error, rol=rol)
        
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