from flask import Blueprint, render_template, request, redirect, url_for
from models.database import Categoria, db_session
from datetime import datetime

categoria_controller = Blueprint('categoria_controller', __name__)
def create_categoria_blueprint():
    # Crear el objeto Blueprint
    categoria_blueprint = Blueprint('categoria', __name__)

    # Definir las rutas y las funciones controladoras
    @categoria_blueprint.route('/categorias')
    def listar():
        # Obtenemos todas las categorías de la base de datos
        categorias = db_session.query(Categoria).all()

        # Verificamos si hay al menos una categoría activa
        hay_activas = any(categoria.activo for categoria in categorias)

        i = 0
        for categoria in categorias:
            if categoria.activo:
                i = i + 1
        if i >= 1:
            hay_activas = True
        if i == 0:
            hay_activas = False

        # Renderizamos el template correspondiente
        return render_template('categoria/listar.html', categorias=categorias, hay_activas=hay_activas)

    @categoria_blueprint.route('/categoria/nueva', methods=['GET', 'POST'])
    def categoria_nueva():
        if request.method == 'POST':
            # Obtener los datos del formulario
            nombre = request.form['nombre']

            # Crear una nueva categoría
            nueva_categoria = Categoria(nombre=nombre)

            # Guardar la nueva categoría en la base de datos
            db_session.add(nueva_categoria)
            db_session.commit()

            return redirect(url_for('.categorias'))
        return render_template('categoria/nueva.html')

    @categoria_blueprint.route('/categoria/editar/<int:id>', methods=['GET', 'POST'])
    def categoria_editar(id):
        categoria = db_session.query(Categoria).filter_by(id=id).one()
        if request.method == 'POST':
            nombre = request.form['nombre']
            categoria.ultima_modificacion = datetime.now()
            categoria.nombre = nombre
            db_session.commit()
            return redirect(url_for('.categorias'))
        else:
            return render_template('categoria/editar.html', categoria=categoria)

    @categoria_blueprint.route('/categoria/eliminar/<int:id>', methods=['GET', 'POST'])
    def categoria_eliminar(id):
        categoria = db_session.query(Categoria).filter_by(id=id).one()
        if request.method == 'POST':
            categoria.activo = 0
            db_session.commit()
            return redirect(url_for('.categorias'))
        else:
            return render_template('categoria/eliminar.html', categoria=categoria)

    @categoria_blueprint.route('/categorias/papelera')
    def categoria_papelera():
        # Obtenemos todas los categorias de la base de datos
        categorias = db_session.query(Categoria).all()

        # Verificamos si hay al menos un categoria no activo
        hay_activas = any(categoria.activo for categoria in categorias)
        i = 0
        for categoria in categorias:
            if not categoria.activo:
                i = i + 1
        if i >= 1:
            hay_activas = True
        if i == 0:
            hay_activas = False

        return render_template('categoria/papelera.html', categorias=categorias, hay_activas=hay_activas)

    @categoria_blueprint.route('/categoria/restaurar/<int:id>', methods=['GET', 'POST'])
    def categoria_restaurar(id):
        categoria = db_session.query(Categoria).filter_by(id=id).one()
        if request.method == 'POST':
            categoria.activo = 1
            db_session.commit()
            return redirect(url_for('.categorias'))
        else:
            return render_template('categoria/restaurar.html', categoria=categoria)
    
    # Devolver el blueprint
    return categoria_blueprint