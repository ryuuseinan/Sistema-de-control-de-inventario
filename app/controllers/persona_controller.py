from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.database import Usuario, Persona, Rol, db_session
import bcrypt, arrow
from sqlalchemy.exc import IntegrityError
from datetime import datetime

persona_controller = Blueprint('persona_controller', __name__)
def create_persona_blueprint():
    # Crear el objeto Blueprint
    persona_blueprint = Blueprint('persona', __name__)

    # Definir las rutas y las funciones controladoras
    @persona_blueprint.route('/personas')
    def listar():
        usuario = db_session.query(Usuario).all()
        personas = db_session.query(Persona).all()
        for usuario in personas:
            fecha_creacion = arrow.get(usuario.fecha_creacion).to('America/Santiago').format('DD-MM-YYYY HH:mm') if usuario.fecha_creacion else None
            ultima_modificacion = arrow.get(usuario.ultima_modificacion).to('America/Santiago').format('DD-MM-YYYY HH:mm') if usuario.ultima_modificacion else None
        return render_template('persona/listar.html', personas=personas, usuario=usuario)

    @persona_blueprint.route('/persona/nuevo', methods=['GET', 'POST'])
    def nueva():
        error = None
        usuario = db_session.query(Usuario).all()
        rol = db_session.query(Rol).all()
        if request.method == 'POST':
            nombre_persona = request.form['nombre_persona']
            correo = request.form['correo']
            contrasena = request.form['contrasena']
            confirmar_contrasena = request.form['confirmar_contrasena']
            rol_id = request.form['rol_id']

            if contrasena != confirmar_contrasena:
                error = "Las contraseñas no coinciden"
            else:
                contrasena_hash = bcrypt.hashpw(contrasena.encode(), bcrypt.gensalt())
                persona = persona(nombre_persona=nombre_persona, correo=correo, contrasena=contrasena_hash, rol_id=rol_id)
                try:
                    db_session.add(persona)
                    db_session.commit()
                    flash('El persona ha sido creado exitosamente.', 'success')
                    return redirect(url_for('listar'))
                except IntegrityError:
                    db_session.rollback()
                    error = "El nombre de persona o correo electrónico ya están en uso"
        return render_template('persona/nuevo.html', error=error, rol=rol)
        
    @persona_blueprint.route('/personas/papelera')
    def papelera():
        rol = db_session.query(Rol).all()
        # Obtenemos todos los personas de la base de datos
        personas = db_session.query(persona).all()

        # Verificamos si hay al menos un persona no activo
        hay_activos = any(persona.activo for persona in personas)
        i = 0
        for persona in personas:
            if not persona.activo:
                i=i+1
        if i>=1:
            hay_activos = True
        if i == 0:
            hay_activos = False

        return render_template('persona/papelera.html', personas=personas, hay_activos=hay_activos)

    @persona_blueprint.route('/persona/restaurar/<int:id>', methods=['GET', 'POST'])
    def restaurar(id):
        rol = db_session.query(Rol).all()
        persona = db_session.query(persona).filter_by(id=id).one()
        if request.method == 'POST':
            persona.activo = 1
            db_session.commit()
            return redirect(url_for('producto.listar'))
        else:
            return render_template('persona/restaurar.html', persona=persona)

    @persona_blueprint.route('/persona/editar/<int:id>', methods=['GET', 'POST'])
    def editar(id):
        rol = db_session.query(Rol).all()
        persona = db_session.query(persona).get(id)

        if not persona:
            flash('El persona no existe', 'error')
            return redirect(url_for('personas'))

        if request.method == 'POST':
            nombre_persona = request.form['nombre_persona']
            correo = request.form['correo']
            contrasena = request.form['contrasena']
            confirmar_contrasena = request.form['confirmar_contrasena']
            rol_id = request.form['rol_id']
            
            # Validar formulario
            if not nombre_persona:
                flash('El nombre de persona es requerido', 'error')
            elif not correo:
                flash('El correo electrónico es requerido', 'error')
            elif contrasena != confirmar_contrasena:
                flash('Las contraseñas no coinciden', 'error')
            else:
                # Actualizar persona
                persona.nombre_persona = nombre_persona
                persona.correo = correo
                persona.rol_id = rol_id
                if contrasena:
                    contrasena_hash = bcrypt.hashpw(contrasena.encode(), bcrypt.gensalt())
                    persona.contrasena = contrasena_hash
                persona.ultima_modificacion = datetime.now()
                db_session.commit()
                
                flash('persona actualizado exitosamente', 'success')
                return redirect(url_for('producto.listar'))
        return render_template('persona/editar.html', persona=persona, rol=rol)

    @persona_blueprint.route('/persona/eliminar/<int:id>', methods=['GET', 'POST'])
    def eliminar(id):
        persona = db_session.query(persona).filter_by(id=id).one()
        if request.method == 'POST':
            persona.activo = 0
            db_session.commit()
            return redirect(url_for('personas'))
        else:
            return render_template('persona/eliminar.html', persona=persona)
    # Devolver el blueprint
    return persona_blueprint