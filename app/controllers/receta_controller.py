from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.database import Producto, Receta, RecetaDetalle, Ingrediente, db_session
import arrow
from datetime import datetime
from sqlalchemy.orm import joinedload

receta_controller = Blueprint('receta_controller', __name__)
def create_receta_blueprint():
    # Crear el objeto Blueprint
    receta_blueprint = Blueprint('receta', __name__)

    # Definir las rutas y las funciones controladoras

    @receta_blueprint.route('/buscar_ingrediente/', methods=['GET', 'POST'])
    def buscar_ingrediente():
        ingrediente_busqueda = request.form.get('ingrediente_busqueda')

        if request.method == 'POST' and ingrediente_busqueda:
            ingredientes = db_session.query(Ingrediente).filter(Ingrediente.nombre.ilike(f'%{ingrediente_busqueda}%'),
                Ingrediente.activo == True
            ).all()
            if not ingredientes:
                flash("No se encontraron ingredientes con ese criterio de búsqueda", "error")
                ingredientes = db_session.query(Ingrediente).filter(Ingrediente.activo == True).all()
        elif request.method == 'POST' and not ingrediente_busqueda:
            flash("Por favor, ingrese el nombre o código de barras de un ingrediente", "error")
            ingredientes = db_session.query(Ingrediente).filter(Ingrediente.activo == True).all()
        else:
            ingredientes = db_session.query(Ingrediente).filter(Ingrediente.activo == True).all()

        return redirect(url_for('receta.configurar', ingrediente_busqueda=ingrediente_busqueda))


    @receta_blueprint.route('/configurar/<int:id>', methods=['GET', 'POST'])
    def configurar(id):
        producto = db_session.query(Producto).filter_by(id=id).one()

        if not db_session.query(Receta).filter_by(id=id).first():
            receta = Receta(id=id, producto_id=id)
            db_session.add(receta)
            db_session.commit()
        else:
            receta = db_session.query(Receta).filter_by(id=id).one()
        
        receta_detalles = receta.detalles  # Obtener todos los detalles de la receta

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
                    ingrediente_existente = db_session.query(RecetaDetalle).filter_by(receta_id=receta.id, ingrediente_id=ingrediente_id).all()
                    if ingrediente_existente:
                        flash(f'El ingrediente {ingrediente_id} ya existe en la receta', 'error')
                        return redirect(url_for('receta.configurar', id=producto.id))
                    
                    receta_detalle = RecetaDetalle(ingrediente_id=ingrediente_id, cantidad=cantidad)
                    receta.detalles.append(receta_detalle)

            db_session.commit()

            flash('Ingrediente agregado al producto exitosamente', 'success')
            return redirect(url_for('receta.configurar', id=producto.id))

        ingrediente = db_session.query(Ingrediente).filter(Ingrediente.activo == True).all()

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