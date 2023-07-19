from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.database import Producto, Receta, RecetaDetalle, Ingrediente, db_session
from sqlalchemy import asc

receta_controller = Blueprint('receta_controller', __name__)
def create_receta_blueprint():
    # Crear el objeto Blueprint
    receta_blueprint = Blueprint('receta', __name__)

    # Definir las rutas y las funciones controladoras
    @receta_blueprint.route('/configurar/<int:id>', methods=['GET', 'POST'])
    def configurar(id):
        try:
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

            ingrediente_busqueda = request.form.get('ingrediente_busqueda')

            if request.method == 'POST' and ingrediente_busqueda:
                ingrediente = db_session.query(Ingrediente).filter(Ingrediente.nombre.ilike(f'%{ingrediente_busqueda}%'), Ingrediente.activo == True).all()
                if not ingrediente:
                    flash("No se encontraron ingredientes con ese criterio de búsqueda", "error")
                    ingrediente = db_session.query(Ingrediente).filter(Ingrediente.activo == True).order_by(Ingrediente.nombre).all()

            elif request.method == 'POST' and not ingrediente_busqueda:
                flash("Por favor, ingrese el nombre de un ingrediente", "error")
                ingrediente = db_session.query(Ingrediente).filter(Ingrediente.activo == True).order_by(Ingrediente.nombre).all()
            else:
                ingrediente = db_session.query(Ingrediente).filter(Ingrediente.activo == True).order_by(Ingrediente.nombre).all()
        except:
            print("ERROR DESCONOCIDO: informe con el desarrollador sobre este problema.")
            db_session.rollback()
            return redirect(request.path)

        return render_template('receta/configurar.html', producto=producto, receta=receta, ingrediente=ingrediente, receta_detalles=receta_detalles)
    
    @receta_blueprint.route('/configurar/agregar_ingrediente/<int:id>', methods=['GET', 'POST'])
    def agregar_ingrediente(id):
        try:
            receta = db_session.query(Receta).filter_by(id=id).one()

            if request.method == 'POST':
                # Obtener los ingredientes y cantidades desde el formulario
                ingrediente_id = request.form.get('ingrediente')
                cantidad = request.form.get('cantidad')

                if ingrediente_id and cantidad:
                    ingrediente_existente = db_session.query(RecetaDetalle).filter_by(receta_id=receta.id, ingrediente_id=ingrediente_id).all()
                    if ingrediente_existente:
                        flash(f'El ingrediente {ingrediente_id} ya existe en la receta', 'error')
                    else:
                        receta_detalle = RecetaDetalle(ingrediente_id=ingrediente_id, cantidad=cantidad)
                        receta.detalles.append(receta_detalle)
                        db_session.commit()
                        flash('Ingrediente agregado al producto exitosamente', 'success')

                return redirect(url_for('receta.configurar', id=receta.producto_id))

            ingrediente = db_session.query(Ingrediente).filter(Ingrediente.activo == True).order_by(asc(Ingrediente.nombre)).all()

            return render_template('receta/agregar_ingrediente.html', receta=receta, ingrediente=ingrediente)
        except:
            print("ERROR DESCONOCIDO: informe con el desarrollador sobre este problema.")
            db_session.rollback()
            return redirect(request.path)

    @receta_blueprint.route('/ingrediente_receta_eliminar/<int:id>', methods=['GET', 'POST'])
    def eliminar_ingrediente(id):
        try:
            receta_detalle = db_session.query(RecetaDetalle).filter_by(id=id).one()
            
            if not receta_detalle:
                flash('El ingrediente de la receta no existe', 'error')
                return redirect(url_for('receta.configurar', id=receta_detalle.receta_id))

            # Eliminar el ingrediente de la receta
            db_session.delete(receta_detalle)
            db_session.commit()

            flash('Ingrediente eliminado de la receta exitosamente', 'success')
            return redirect(url_for('receta.configurar', id=receta_detalle.receta_id))
        except:
            print("ERROR DESCONOCIDO: informe con el desarrollador sobre este problema.")
            db_session.rollback()
            return redirect(request.path)

    # Devolver el blueprint
    return receta_blueprint
