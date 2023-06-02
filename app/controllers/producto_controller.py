from flask import Blueprint, render_template, request, redirect, url_for
from models.database import Producto, Categoria, db_session
from datetime import datetime
from werkzeug.utils import secure_filename
import os

producto_controller = Blueprint('producto_controller', __name__)
def create_producto_blueprint():
    # Crear el objeto Blueprint
    producto_blueprint = Blueprint('producto', __name__)

    # Definir las rutas y las funciones controladoras
    @producto_blueprint.route('/productos')
    def listar():
        # Obtenemos todas los productos de la base de datos
        productos = db_session.query(Producto).all()
        # Verificamos si hay al menos un producto activo
        hay_activas = any(producto.activo for producto in productos)
        i = 0
        for producto in productos:
            if producto.activo:
                i=i+1
        if i>=1:
            hay_activas = True
        if i == 0:
            hay_activas = False
        return render_template('producto/listar.html', productos=productos, hay_activas=hay_activas)

    @producto_blueprint.route('/productos/papelera')
    def papelera():
        # Obtenemos todas los productos de la base de datos
        productos = db_session.query(Producto).all()
        
        # Verificamos si hay al menos un producto no activo
        hay_activas = any(producto.activo for producto in productos)
        i = 0
        for producto in productos:
            if not producto.activo:
                i=i+1
        if i>=1:
            hay_activas = True
        if i == 0:
            hay_activas = False
        return render_template('producto/papelera.html', productos=productos, hay_activas=hay_activas)

    @producto_blueprint.route('/producto/nuevo', methods=['GET', 'POST'])
    def nuevo():
        # Obtener las categorías para mostrarlas en el formulario
        categorias = db_session.query(Categoria).all()
        
        if request.method == 'POST':
            # Obtener los datos del formulario
            imagen = request.files['imagen']
            codigo_barra = request.form['codigo_barra']
            nombre = request.form['nombre']
            descripcion = request.form['descripcion']
            categoria_id = request.form['categoria_id']
            precio = request.form['precio']
            # Crear una nueva instancia de Producto con los datos del formulario
            nuevo_producto = Producto(codigo_barra=codigo_barra, 
                                    nombre=nombre, 
                                    descripcion=descripcion, 
                                    categoria_id=categoria_id, 
                                    precio=precio, 
                                    fecha_creacion=datetime.now())

            if imagen and imagen.filename:
                filename = secure_filename(imagen.filename)
                imagen.save(os.path.join('app', 'static', 'img', 'productos', filename))
                nuevo_producto.imagen = '/productos/' + filename
            else:
                filename = None
                nuevo_producto.imagen = None
            
            # Agregar el producto a la base de datos
            db_session.add(nuevo_producto)
            db_session.commit()
            
            # Redireccionar al listado de productos
            return redirect(url_for('producto.listar'))
        
        # Renderizar la plantilla de nuevo producto
        return render_template('producto/nuevo.html', categorias=categorias)

    @producto_blueprint.route('/producto/restaurar/<int:id>', methods=['GET', 'POST'])
    def restaurar(id):
        producto = db_session.query(Producto).filter_by(id=id).one()
        if request.method == 'POST':
            producto.activo = 1
            db_session.commit()
            return redirect(url_for('producto.listar'))
        else:
            return render_template('producto/restaurar.html', producto=producto)

    @producto_blueprint.route('/producto/editar/<int:id>', methods=['GET', 'POST'])
    def editar(id):
        # Obtener el producto a editar de la base de datos
        producto = db_session.query(Producto).filter_by(id=id).one()
        categoria = db_session.query(Categoria).all()
        if request.method == 'POST':
            # Obtener los datos del formulario
            codigo_barra = request.form['codigo_barra']
            nombre = request.form['nombre']
            categoria_id = request.form['categoria_id']
            descripcion = request.form['descripcion']
            precio = request.form['precio']

            # Actualizar los datos del producto con los nuevos datos del formulario
            if codigo_barra:
                producto.codigo_barra = codigo_barra
            if nombre:
                producto.nombre = nombre
            if categoria_id:
                producto.categoria_id = categoria_id
            if descripcion:
                producto.descripcion = descripcion
            if precio:
                producto.precio = precio

            # Actualizar la imagen del producto si se ha enviado una nueva
            imagen = request.files['imagen']
            if imagen and imagen.filename:
                filename = secure_filename(imagen.filename)
                imagen.save(os.path.join('app', 'static', 'img', 'productos', filename))
                producto.imagen = '/productos/' + filename
            
            # Registrar ultima modificación
            producto.ultima_modificacion = datetime.now()
            
            # Guardar los cambios en la base de datos
            db_session.commit()

            # Redireccionar al listado de productos
            return redirect(url_for('producto.listar'))

        # Renderizar la plantilla de edición de productos
        return render_template('producto/editar.html', producto=producto, categoria=categoria)

    @producto_blueprint.route('/producto/eliminar/<int:id>', methods=['GET', 'POST'])
    def eliminar(id):
        producto = db_session.query(Producto).filter_by(id=id).one()
        if request.method == 'POST':
            producto.activo = 0
            db_session.commit()
            return redirect(url_for('producto.listar'))
        else:
            return render_template('producto/eliminar.html', producto=producto)

    # Devolver el blueprint
    return producto_blueprint