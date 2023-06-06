from flask import Blueprint, render_template, request, redirect, url_for
from models.database import Ingrediente, UnidadMedida, db_session
from datetime import datetime

ingrediente_controller = Blueprint('ingrediente_controller', __name__)
def create_ingrediente_blueprint():
    # Crear el objeto Blueprint
    ingrediente_blueprint = Blueprint('ingrediente', __name__)

    # Definir las rutas y las funciones controladoras
    @ingrediente_blueprint.route('/ingredientes')
    def listar():
        # Obtenemos todas los ingredientes de la base de datos
        ingredientes = db_session.query(Ingrediente).filter(Ingrediente.activo == True).all()
        return render_template('ingrediente/listar.html', ingredientes=ingredientes)

    @ingrediente_blueprint.route('/ingrediente_papelera')
    def papelera():
        # Obtenemos todas los ingredientes de la base de datos
        ingredientes = db_session.query(Ingrediente).filter(Ingrediente.activo == False).all()
        return render_template('ingrediente/papelera.html', ingredientes=ingredientes)

    @ingrediente_blueprint.route('/ingrediente_nuevo', methods=['GET', 'POST'])
    def nuevo():
        # Obtener las categorías para mostrarlas en el formulario
        unidadmedida = db_session.query(UnidadMedida).filter(UnidadMedida.activo == True).all()
        if request.method == 'POST':
            # Obtener los datos del formulario
            nombre = request.form['nombre']
            cantidad = request.form['cantidad']
            unidadmedida_id = request.form['unidadmedida_id']
            # Crear una nueva instancia de Producto con los datos del formulario
            nuevo_ingrediente = Ingrediente(nombre=nombre, 
                                    cantidad=cantidad, 
                                    unidadmedida_id=unidadmedida_id,
                                    fecha_creacion=datetime.now(),
                                    ultima_modificacion=datetime.now())
            
            # Agregar el producto a la base de datos
            db_session.add(nuevo_ingrediente)
            db_session.commit()
            
            # Redireccionar al listado de productos
            return redirect(url_for('ingrediente.listar'))
        
        # Renderizar la plantilla ingrediente
        return render_template('ingrediente/nuevo.html', unidadmedida=unidadmedida)

    @ingrediente_blueprint.route('/ingrediente_editar/<int:id>', methods=['GET', 'POST'])
    def editar(id):
        # Obtener el ingrediente a editar de la base de datos
        ingrediente = db_session.query(Ingrediente).filter_by(id=id).one()
        unidadmedida = db_session.query(UnidadMedida).filter(UnidadMedida.activo == True).all()

        if request.method == 'POST':
            # Obtener los datos del formulario
            nombre = request.form['nombre']
            cantidad = request.form['cantidad']
            unidadmedida_id = request.form['unidadmedida_id']

            # Actualizar los datos del ingrediente con los nuevos datos del formulario
            if nombre:
                ingrediente.nombre = nombre
            if cantidad:
                ingrediente.cantidad = cantidad
            if unidadmedida_id:
                ingrediente.unidadmedida_id = unidadmedida_id

            # Registrar última modificación
            ingrediente.ultima_modificacion = datetime.now()

            # Guardar los cambios en la base de datos
            db_session.commit()

            # Redireccionar al listado de ingredientes
            return redirect(url_for('ingrediente.listar'))

        # Renderizar la plantilla de edición de ingrediente
        return render_template('ingrediente/editar.html', ingrediente=ingrediente, unidadmedida=unidadmedida)

    @ingrediente_blueprint.route('/ingrediente_eliminar/<int:id>', methods=['GET', 'POST'])
    def eliminar(id):
        ingrediente = db_session.query(Ingrediente).filter_by(id=id).one()

        if request.method == 'POST':
            # Eliminar el ingrediente estableciendo el campo "activo" en 0
            ingrediente.activo = 0
            db_session.commit()

            # Redireccionar al listado de ingredientes
            return redirect(url_for('ingrediente.listar'))

        # Renderizar la plantilla de confirmación de eliminación de ingrediente
        return render_template('ingrediente/eliminar.html', ingrediente=ingrediente)

    @ingrediente_blueprint.route('/ingrediente/restaurar/<int:id>', methods=['GET', 'POST'])
    def restaurar(id):
        ingrediente = db_session.query(Ingrediente).filter_by(id=id).one()
        if request.method == 'POST':
            ingrediente.activo = 1
            db_session.commit()
            return redirect(url_for('ingrediente.listar'))
        else:
            return render_template('ingrediente/restaurar.html', ingrediente=ingrediente)
    # Devolver el blueprint
    return ingrediente_blueprint