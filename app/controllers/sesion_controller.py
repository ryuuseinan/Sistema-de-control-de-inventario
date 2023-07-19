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
        try:
            # Cerrar sesión asignando False a la sesión 
            session['logged_in'] = False
            # Agregar mensaje de "Has cerrado sesión"
            flash('Has cerrado sesión', 'success')
            # Redirecciona al usuario a la página de inicio de sesión después de cerrar sesión
            return redirect(url_for('sesion.login'))
        except:
            print("ERROR DESCONOCIDO: informe con el desarrollador sobre este problema.")
            db_session.rollback()
            return redirect(request.path)

    @sesion_blueprint.route('/login', methods=['GET', 'POST'])
    def login():
        try:
            if request.method == 'POST':
                nombre_usuario = request.form['nombre_usuario']
                contrasena = request.form['contrasena']

                # Verificar si el nombre_usuario y la contraseña coinciden con un usuario en la base de datos
                usuario = db_session.query(Usuario).filter(Usuario.nombre_usuario == nombre_usuario, Usuario.activo == True).first()

                if usuario and bcrypt.checkpw(contrasena.encode(), usuario.contrasena.encode()):
                    # Establecer la sesión del usuario como iniciada
                    persona = db_session.query(Persona).filter_by(usuario_id=usuario.id).first()
                    session['logged_in'] = True
                    session['id'] = usuario.id
                    session['rol'] = usuario.rol.id
                    session['rol_nombre'] = usuario.rol.nombre
                    session['nombre'] = persona.nombre
                    session['apellido'] = persona.apellido_paterno  # Guardar el nombre de usuario en la sesión

                    flash('Sesión iniciada correctamente', 'success')
                    return redirect(url_for('index'))
                
                elif usuario is None:
                    flash('Su usuario actualmente se encuentra inhabilitado, contacte con el administrador si considera que se trata de un error', 'error')
                    return redirect(url_for('sesion.login'))

                else:
                    flash('Credenciales inválidas', 'error')
                    return redirect(url_for('sesion.login'))

            return render_template('sesion/login.html')
        except:
            print("ERROR DESCONOCIDO: informe con el desarrollador sobre este problema.")
            db_session.rollback()
            return redirect(request.path)

    # Devolver el blueprint
    return sesion_blueprint
