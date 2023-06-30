from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.database import Usuario, Persona, db_session
import bcrypt

sesion_controller = Blueprint('sesion_controller', __name__)
def create_sesion_blueprint():
    # Crear el objeto Blueprint
    sesion_blueprint = Blueprint('sesion', __name__)

    # Definir las rutas y las funciones controladoras
    @sesion_blueprint.route('/logout')
    def logout():
        # Cerrar sesión asignando False a la sesión 
        session['logged_in'] = False
        # Agregar mensaje de "Has cerrado sesión"
        flash('Has cerrado sesión', 'success')
        # Redirecciona al usuario a la página de inicio de sesión después de cerrar sesión
        return redirect(url_for('sesion.login'))

    @sesion_blueprint.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            nombre_usuario = request.form['nombre_usuario']
            contrasena = request.form['contrasena']

            # Verificar si el nombre_usuario y la contraseña coinciden con un usuario en la base de datos
            usuario = db_session.query(Usuario).filter_by(nombre_usuario=nombre_usuario).first()

            if usuario and bcrypt.checkpw(contrasena.encode(), usuario.contrasena.encode()):
                # Establecer la sesión del usuario como iniciada
                persona = db_session.query(Persona).filter_by(usuario_id=usuario.id).first()
                session['logged_in'] = True
                session['user_id'] = usuario.id
                session['user_nombre'] = persona.nombre
                session['user_apellido'] = persona.apellido_paterno  # Guardar el nombre de usuario en la sesión

                flash('Sesión iniciada correctamente', 'success')
                return redirect(url_for('index'))
            else:
                flash('Credenciales inválidas', 'error')
                return redirect(url_for('sesion.login'))

        return render_template('sesion/login.html')

    # Devolver el blueprint
    return sesion_blueprint