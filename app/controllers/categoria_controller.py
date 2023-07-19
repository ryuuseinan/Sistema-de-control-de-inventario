from flask import Blueprint, render_template, request, redirect, url_for
from models.database import Categoria, db_session
from datetime import datetime
from sqlalchemy import asc

categoria_controller = Blueprint('categoria_controller', __name__)
def create_categoria_blueprint():
    # Crear el objeto Blueprint
    categoria_blueprint = Blueprint('categoria', __name__)

    # Definir las rutas y las funciones controladoras
    @categoria_blueprint.route('/categorias')
    def listar():
        try:
            # Obtenemos todas las categorías de la base de datos
            categorias = db_session.query(Categoria).filter(Categoria.activo == True).order_by(asc(Categoria.nombre)).all()
            return render_template('categoria/listar.html', categorias=categorias)
        except:
            print("ERROR DESCONOCIDO: informe con el desarrollador sobre este problema.")
            db_session.rollback()
            return redirect(request.path)

    @categoria_blueprint.route('/categoria/nueva', methods=['GET', 'POST'])
    def nueva():
        try:
            if request.method == 'POST':
                # Obtener los datos del formulario
                nombre = request.form['nombre']

                # Crear una nueva categoría
                nueva_categoria = Categoria(nombre=nombre)

                # Guardar la nueva categoría en la base de datos
                db_session.add(nueva_categoria)
                db_session.commit()

                return redirect(url_for('categoria.listar'))
            return render_template('categoria/nueva.html')
        except:
            print("ERROR DESCONOCIDO: informe con el desarrollador sobre este problema.")
            db_session.rollback()
            return redirect(request.path)

    @categoria_blueprint.route('/categoria/editar/<int:id>', methods=['GET', 'POST'])
    def editar(id):
        try:
            categoria = db_session.query(Categoria).filter_by(id=id).one()
            if request.method == 'POST':
                nombre = request.form['nombre']
                categoria.ultima_modificacion = datetime.now()
                categoria.nombre = nombre
                db_session.commit()
                return redirect(url_for('categoria.listar'))
            else:
                return render_template('categoria/editar.html', categoria=categoria)
        except:
            print("ERROR DESCONOCIDO: informe con el desarrollador sobre este problema.")
            db_session.rollback()
            return redirect(request.path)

    @categoria_blueprint.route('/categoria/eliminar/<int:id>', methods=['GET', 'POST'])
    def eliminar(id):
        try:
            categoria = db_session.query(Categoria).filter_by(id=id).one()
            if request.method == 'POST':
                categoria.activo = False
                db_session.commit()
                return redirect(url_for('categoria.listar'))
            else:
                return render_template('categoria/eliminar.html', categoria=categoria)
        except:
            print("ERROR DESCONOCIDO: informe con el desarrollador sobre este problema.")
            db_session.rollback()
            return redirect(request.path)

    @categoria_blueprint.route('/categorias/papelera')
    def papelera():
        try:
            # Obtenemos todas los categorias de la base de datos
            categorias = db_session.query(Categoria).filter(Categoria.activo == False).order_by(asc(Categoria.nombre)).all()
            return render_template('categoria/papelera.html', categorias=categorias)
        except:
            print("ERROR DESCONOCIDO: informe con el desarrollador sobre este problema.")
            db_session.rollback()
            return redirect(request.path)

    @categoria_blueprint.route('/categoria/restaurar/<int:id>', methods=['GET', 'POST'])
    def restaurar(id):
        try:
            categoria = db_session.query(Categoria).filter_by(id=id).one()
            if request.method == 'POST':
                categoria.activo = True
                db_session.commit()
                return redirect(url_for('categoria.listar'))
            else:
                return render_template('categoria/restaurar.html', categoria=categoria)
        except:
            print("ERROR DESCONOCIDO: informe con el desarrollador sobre este problema.")
            db_session.rollback()
            return redirect(request.path)
    
    # Devolver el blueprint
    return categoria_blueprint
