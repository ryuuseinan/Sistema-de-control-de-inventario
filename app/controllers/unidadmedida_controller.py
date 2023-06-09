from flask import Blueprint, render_template, request, redirect, url_for
from models.database import UnidadMedida, db_session
from datetime import datetime

unidadmedida_controller = Blueprint('unidadmedida_controller', __name__)
def create_unidadmedida_blueprint():
    # Crear el objeto Blueprint
    unidadmedida_blueprint = Blueprint('unidadmedida', __name__)

    # Definir las rutas y las funciones controladoras
    @unidadmedida_blueprint.route('/unidadmedidas')
    def listar():
        # Obtenemos todas los unidadmedidas de la base de datos
        unidadmedidas = db_session.query(UnidadMedida).filter(UnidadMedida.activo == True).all()
        return render_template('unidadmedida/listar.html', unidadmedidas=unidadmedidas)

    @unidadmedida_blueprint.route('/unidadmedida_papelera')
    def papelera():
        # Obtenemos todas los unidadmedidas de la base de datos
        unidadmedidas = db_session.query(UnidadMedida).filter(UnidadMedida.activo == False).all()
        return render_template('unidadmedida/papelera.html', unidadmedidas=unidadmedidas)

    @unidadmedida_blueprint.route('/unidadmedida_nuevo', methods=['GET', 'POST'])
    def nuevo():
        if request.method == 'POST':
            # Obtener los datos del formulario
            nombre = request.form['nombre']
            # Crear una nueva instancia de Producto con los datos del formulario
            nueva_unidadmedida = UnidadMedida(nombre=nombre, 
                                    fecha_creacion=datetime.now(),
                                    ultima_modificacion=datetime.now())
            
            # Agregar el producto a la base de datos
            db_session.add(nueva_unidadmedida)
            db_session.commit()
            
            # Redireccionar al listado de productos
            return redirect(url_for('unidadmedida.listar'))
        
        # Renderizar la plantilla unidadmedida
        return render_template('unidadmedida/nuevo.html')

    @unidadmedida_blueprint.route('/unidadmedida_editar/<int:id>', methods=['GET', 'POST'])
    def editar(id):
        # Obtener el unidadmedida a editar de la base de datos
        unidadmedida = db_session.query(UnidadMedida).filter_by(id=id).one()

        if request.method == 'POST':
            # Obtener los datos del formulario
            nombre = request.form['nombre']

            # Actualizar los datos del unidadmedida con los nuevos datos del formulario
            if nombre:
                unidadmedida.nombre = nombre

            # Registrar última modificación
            unidadmedida.ultima_modificacion = datetime.now()

            # Guardar los cambios en la base de datos
            db_session.commit()

            # Redireccionar al listado de unidadmedidas
            return redirect(url_for('unidadmedida.listar'))

        # Renderizar la plantilla de edición de unidadmedida
        return render_template('unidadmedida/editar.html', unidadmedida=unidadmedida)

    @unidadmedida_blueprint.route('/unidadmedida_eliminar/<int:id>', methods=['GET', 'POST'])
    def eliminar(id):
        unidadmedida = db_session.query(UnidadMedida).filter_by(id=id).one()

        if request.method == 'POST':
            # Eliminar el unidadmedida estableciendo el campo "activo" en False
            unidadmedida.activo = False
            db_session.commit()

            # Redireccionar al listado de unidadmedidas
            return redirect(url_for('unidadmedida.listar'))

        # Renderizar la plantilla de confirmación de eliminación de unidadmedida
        return render_template('unidadmedida/eliminar.html', unidadmedida=unidadmedida)

    @unidadmedida_blueprint.route('/unidadmedida/restaurar/<int:id>', methods=['GET', 'POST'])
    def restaurar(id):
        unidadmedida = db_session.query(unidadmedida).filter_by(id=id).one()
        if request.method == 'POST':
            unidadmedida.activo = True
            db_session.commit()
            return redirect(url_for('unidadmedida.listar'))
        else:
            return render_template('unidadmedida/restaurar.html', unidadmedida=unidadmedida)
    # Devolver el blueprint
    return unidadmedida_blueprint