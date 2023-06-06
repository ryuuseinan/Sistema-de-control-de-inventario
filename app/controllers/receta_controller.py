from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.database import Producto, Receta, RecetaDetalle, Ingrediente, db_session
import bcrypt, arrow
from sqlalchemy.exc import IntegrityError
from datetime import datetime

receta_controller = Blueprint('receta_controller', __name__)
def create_receta_blueprint():
    # Crear el objeto Blueprint
    receta_blueprint = Blueprint('receta', __name__)

    # Definir las rutas y las funciones controladoras
    @receta_blueprint.route('/configurar/<int:id>', methods=['GET', 'POST'])
    def configurar(id):
        producto = db_session.query(Producto).filter_by(id=id).one()
        receta = db_session.query(Receta).filter_by(id=id).one()
        receta_detalles = receta.detalles  # Obtener todos los detalles de la receta

        # Crear la receta si no existe
        if not receta:
            receta = Receta(producto_id=producto.id)
            db_session.add(receta)

        if not producto:
            flash('El producto no existe', 'error')
            return redirect(url_for('vender'))

        if request.method == 'POST':
            # Obtener los ingrediente y cantidades desde el formulario
            ingrediente = request.form.getlist('ingrediente')
            cantidades = request.form.getlist('cantidad')

            # Agregar los ingrediente y cantidades a la receta
            for ingrediente_id, cantidad in zip(ingrediente, cantidades):
                if ingrediente_id and cantidad:
                    receta_detalle = RecetaDetalle(ingrediente_id=ingrediente_id, cantidad=cantidad)
                    receta.detalles.append(receta_detalle)

            db_session.commit()

            flash('Ingrediente agregado al producto exitosamente', 'success')
            return redirect(url_for('receta.configurar', id=producto.id))

        ingrediente = db_session.query(Ingrediente).all()

        return render_template('receta/configurar.html', producto=producto, receta=receta, ingrediente=ingrediente, receta_detalles=receta_detalles)

    @receta_blueprint.route('/ingrediente_receta_eliminar/<int:id>', methods=['GET', 'POST'])
    def eliminar_ingrediente(id):
        receta_detalle = db_session.query(RecetaDetalle).filter_by(id=id).one()
        if not receta_detalle:
            flash('El ingrediente de la receta no existe', 'error')
            return redirect(url_for('receta.configurar', id=receta_detalle.receta_id))

        # Eliminar el ingrediente de la receta
        db_session.delete(receta_detalle)
        db_session.commit()

        flash('Ingrediente eliminado de la receta exitosamente', 'success')
        return redirect(url_for('receta.configurar', id=receta_detalle.receta_id))

    # Devolver el blueprint
    return receta_blueprint