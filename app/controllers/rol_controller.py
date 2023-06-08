from flask import Blueprint, render_template, request, redirect, url_for
from models.database import Rol, db_session
from datetime import datetime

rol_controller = Blueprint('rol_controller', __name__)
def create_rol_blueprint():
    # Crear el objeto Blueprint
    rol_blueprint = Blueprint('rol', __name__)

    # Definir las rutas y las funciones controladoras
    @rol_blueprint.route('/roles')
    def listar():
        # Obtenemos todas los roles de la base de datos
        roles = db_session.query(Rol).filter(Rol.activo == True).all()
        return render_template('rol/listar.html', roles=roles)

    @rol_blueprint.route('/rol_papelera')
    def papelera():
        # Obtenemos todas los roles de la base de datos
        roles = db_session.query(Rol).filter(Rol.activo == False).all()
        return render_template('rol/papelera.html', roles=roles)

    @rol_blueprint.route('/rol_nuevo', methods=['GET', 'POST'])
    def nuevo():
        if request.method == 'POST':
            # Obtener los datos del formulario
            nombre = request.form['nombre']
            # Crear una nueva instancia de Producto con los datos del formulario
            nuevo_rol = Rol(nombre=nombre, 
                                    fecha_creacion=datetime.now(),
                                    ultima_modificacion=datetime.now())
            
            # Agregar el producto a la base de datos
            db_session.add(nuevo_rol)
            db_session.commit()
            
            # Redireccionar al listado de productos
            return redirect(url_for('rol.listar'))
        
        # Renderizar la plantilla rol
        return render_template('rol/nuevo.html')

    @rol_blueprint.route('/rol_editar/<int:id>', methods=['GET', 'POST'])
    def editar(id):
        # Obtener el rol a editar de la base de datos
        rol = db_session.query(Rol).filter_by(id=id).one()

        if request.method == 'POST':
            # Obtener los datos del formulario
            nombre = request.form['nombre']

            # Actualizar los datos del rol con los nuevos datos del formulario
            if nombre:
                rol.nombre = nombre

            # Registrar última modificación
            rol.ultima_modificacion = datetime.now()

            # Guardar los cambios en la base de datos
            db_session.commit()

            # Redireccionar al listado de roles
            return redirect(url_for('rol.listar'))

        # Renderizar la plantilla de edición de rol
        return render_template('rol/editar.html', rol=rol)

    @rol_blueprint.route('/rol_eliminar/<int:id>', methods=['GET', 'POST'])
    def eliminar(id):
        rol = db_session.query(Rol).filter_by(id=id).one()

        if request.method == 'POST':
            # Eliminar el rol estableciendo el campo "activo" en False
            rol.activo = False
            db_session.commit()

            # Redireccionar al listado de roles
            return redirect(url_for('rol.listar'))

        # Renderizar la plantilla de confirmación de eliminación de rol
        return render_template('rol/eliminar.html', rol=rol)

    @rol_blueprint.route('/rol/restaurar/<int:id>', methods=['GET', 'POST'])
    def restaurar(id):
        rol = db_session.query(Rol).filter_by(id=id).one()
        if request.method == 'POST':
            rol.activo = True
            db_session.commit()
            return redirect(url_for('rol.listar'))
        else:
            return render_template('rol/restaurar.html', rol=rol)
    # Devolver el blueprint
    return rol_blueprint