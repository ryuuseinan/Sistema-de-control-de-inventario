from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.database import Usuario, Persona, Rol, db_session
import bcrypt, arrow
from sqlalchemy.exc import IntegrityError
from datetime import datetime

usuario_controller = Blueprint('usuario_controller', __name__)
def create_usuario_blueprint():
    # Crear el objeto Blueprint
    usuario_blueprint = Blueprint('usuario', __name__)

    # Definir las rutas y las funciones controladoras
    @usuario_blueprint.route('/usuarios')
    def listar():
        rol = db_session.query(Rol).filter(Rol.activo == True).all()
        usuarios = db_session.query(Usuario).filter(Usuario.activo == True).all()
        for usuario in usuarios:
            fecha_creacion = arrow.get(usuario.fecha_creacion).to('America/Santiago').format('DD-MM-YYYY HH:mm') if usuario.fecha_creacion else None
            ultima_modificacion = arrow.get(usuario.ultima_modificacion).to('America/Santiago').format('DD-MM-YYYY HH:mm') if usuario.ultima_modificacion else None
        return render_template('usuario/listar.html', usuarios=usuarios, rol=rol)

    @usuario_blueprint.route('/usuario/nuevo', methods=['GET', 'POST'])
    def nuevo():
        error = None
        rol = db_session.query(Rol).filter(Rol.activo == True).all()

        if request.method == 'POST':
            nombre_usuario = request.form['nombre_usuario']
            correo = request.form['correo']
            contrasena = request.form['contrasena']
            confirmar_contrasena = request.form['confirmar_contrasena']
            rol_id = request.form['rol_id']
            rut = request.form['rut']
            nombre = request.form['nombre']
            apellido_paterno = request.form['apellido_paterno']
            apellido_materno = request.form['apellido_materno']
            celular = request.form['celular']

            if contrasena != confirmar_contrasena:
                error = "Las contraseñas no coinciden"
            else:
                contrasena_hash = bcrypt.hashpw(contrasena.encode(), bcrypt.gensalt())

                # Verificar si el RUT ya existe en la base de datos
                persona_existente = db_session.query(Persona).filter_by(rut=rut).first()

                if persona_existente:
                    error = 'El RUT ya existe en la base de datos.'
                else:
                    usuario = Usuario(nombre_usuario=nombre_usuario, correo=correo, contrasena=contrasena_hash, rol_id=rol_id)
                    try:
                        db_session.add(usuario)
                        db_session.commit()

                        # Asignar el ID del usuario creado a persona.usuario_id
                        nueva_persona = Persona(usuario_id=usuario.id, rut=rut, nombre=nombre, apellido_paterno=apellido_paterno,
                                                apellido_materno=apellido_materno, celular=celular)
                        db_session.add(nueva_persona)
                        db_session.commit()

                        flash('El usuario ha sido creado exitosamente.', 'success')
                        return redirect(url_for('usuario.listar'))
                    except IntegrityError:
                        db_session.rollback()
                        error = "El nombre de usuario o correo electrónico ya están en uso"

        return render_template('usuario/nuevo.html', error=error, rol=rol)
        
    @usuario_blueprint.route('/usuarios/papelera')
    def papelera():
        rol = db_session.query(Rol).filter(Rol.activo == True).all()
        # Obtenemos todos los usuarios de la base de datos
        usuarios = db_session.query(Usuario).filter(Usuario.activo == False).all()
        return render_template('usuario/papelera.html', usuarios=usuarios)

    @usuario_blueprint.route('/usuario/restaurar/<int:id>', methods=['GET', 'POST'])
    def restaurar(id):
        rol = db_session.query(Rol).filter(Rol.activo == True).all()
        usuario = db_session.query(Usuario).filter_by(id=id).one()
        if request.method == 'POST':
            usuario.activo = True
            db_session.commit()
            return redirect(url_for('usuario.listar'))
        else:
            return render_template('usuario/restaurar.html', usuario=usuario)

    @usuario_blueprint.route('/usuario/editar/<int:id>', methods=['GET', 'POST'])
    def editar(id):
        rol = db_session.query(Rol).filter(Rol.activo == True).all()
        usuario = db_session.query(Usuario).get(id)
        persona = db_session.query(Persona).filter(Persona.usuario_id == usuario.id).one()
        
        if usuario is None:
            flash('El usuario no existe', 'error')
            return redirect(url_for('usuario.listar'))

        if request.method == 'POST':
            nombre_usuario = request.form['nombre_usuario']
            correo = request.form['correo']
            contrasena = request.form['contrasena']
            confirmar_contrasena = request.form['confirmar_contrasena']
            rol_id = request.form['rol_id']
            rut = request.form['rut']
            nombre = request.form['nombre']
            apellido_paterno = request.form['apellido_paterno']
            apellido_materno = request.form['apellido_materno']
            celular = request.form['celular']
            
            # Validar formulario
            if not nombre_usuario:
                flash('El nombre de usuario es requerido', 'error')
            elif not correo:
                flash('El correo electrónico es requerido', 'error')
            elif contrasena != confirmar_contrasena:
                flash('Las contraseñas no coinciden', 'error')
            else:
                # Actualizar usuario
                usuario.nombre_usuario = nombre_usuario
                usuario.correo = correo
                usuario.rol_id = rol_id
                
                # Si se proporciona una nueva contraseña, se actualiza
                if contrasena:
                    contrasena_hash = bcrypt.hashpw(contrasena.encode(), bcrypt.gensalt())
                    usuario.contrasena = contrasena_hash
                    
                usuario.ultima_modificacion = datetime.now()                
                db_session.commit()
                
                # Actualizar los datos de la persona asociada al usuario
                if persona:
                    persona.rut = rut
                    persona.nombre = nombre
                    persona.apellido_paterno = apellido_paterno
                    persona.apellido_materno = apellido_materno
                    persona.celular = celular
                    persona.ultima_modificacion = datetime.now()             
                db_session.commit()
                
                flash('Usuario actualizado exitosamente', 'success')
                return redirect(url_for('usuario.listar'))
        
        return render_template('usuario/editar.html', usuario=usuario, rol=rol, persona=persona)


    @usuario_blueprint.route('/usuario/eliminar/<int:id>', methods=['GET', 'POST'])
    def eliminar(id):
        usuario = db_session.query(Usuario).filter_by(id=id).one()
        if request.method == 'POST':
            usuario.activo = False
            db_session.commit()
            return redirect(url_for('usuario.listar'))
        else:
            return render_template('usuario/eliminar.html', usuario=usuario)

    # Devolver el blueprint
    return usuario_blueprint