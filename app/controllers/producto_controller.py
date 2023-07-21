from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.database import Producto, Categoria, db_session
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc
from PIL import Image

producto_controller = Blueprint('producto_controller', __name__)
def create_producto_blueprint():
    # Crear el objeto Blueprint
    producto_blueprint = Blueprint('producto', __name__)

    # Definir las rutas y las funciones controladoras
    @producto_blueprint.route('/productos')
    #@login_required
    def listar():
        try:
            # Obtenemos todas los productos de la base de datos
            productos = db_session.query(Producto).filter(Producto.activo == True).order_by(asc(Producto.nombre)).all()
            return render_template('producto/listar.html', productos=productos)
        except:
            print("ERROR DESCONOCIDO: informe con el desarrollador sobre este problema.")
            db_session.rollback()
            return redirect(request.path)

    @producto_blueprint.route('/productos/papelera')
    def papelera():
        try:
            # Obtenemos todas los productos de la base de datos
            productos = db_session.query(Producto).filter(Producto.activo == False).order_by(asc(Producto.nombre)).all()
            return render_template('producto/papelera.html', productos=productos)
        except:
            print("ERROR DESCONOCIDO: informe con el desarrollador sobre este problema.")
            db_session.rollback()
            return redirect(request.path)

    #@roles_required('Administrdor')
    @producto_blueprint.route('/producto/nuevo', methods=['GET', 'POST'])
    def nuevo():

        # Obtener las categorías para mostrarlas en el formulario
        categorias = db_session.query(Categoria).filter(Categoria.activo == True).all()

        if request.method == 'POST':
            # Obtener los datos del formulario
            imagen = request.files['imagen']
            codigo_barra = request.form['codigo_barra']
            nombre = request.form['nombre']
            descripcion = request.form['descripcion']
            categoria_id = request.form['categoria_id']
            precio = request.form['precio']
            alerta_stock = request.form['alerta_stock'] 
            tiene_receta = True if request.form['tiene_receta'] == "True" else False
            
            if not codigo_barra:
                codigo_barra = None

            # Crear una nueva instancia de Producto con los datos del formulario
    
                # Crear una nueva instancia de Producto con los datos del formulario
                nuevo_producto = Producto(codigo_barra=codigo_barra, 
                                        nombre=nombre, 
                                        descripcion=descripcion, 
                                        categoria_id=categoria_id, 
                                        precio=precio,
                                        tiene_receta=tiene_receta,
                                        alerta_stock=alerta_stock,
                                        fecha_creacion=datetime.now())
                                            
                # Resto del código para guardar el producto en la base de datos
                if imagen and imagen.filename:
                    # Cambiar el nombre del archivo de la imagen al nombre del producto con extensión ".webp"
                    filename = secure_filename(f"{nombre}.webp")
                    image_path = os.path.join('app', 'static', 'img', 'productos', filename)
                    imagen.save(image_path)
                    
                    # Redimensionar y guardar la imagen en formato WebP
                    with Image.open(image_path) as img:
                        img.thumbnail((128, 128))
                        img.save(image_path, format='WEBP')

                    nuevo_producto.imagen = '/productos/' + filename
                else:
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
        try:
            producto = db_session.query(Producto).filter_by(id=id).one()
            if request.method == 'POST':
                producto.activo = True
                db_session.commit()
                return redirect(url_for('producto.listar'))
            else:
                return render_template('producto/restaurar.html', producto=producto)
        except:
            print("ERROR DESCONOCIDO: informe con el desarrollador sobre este problema.")
            db_session.rollback()
            return redirect(request.path)

    @producto_blueprint.route('/producto/editar/<int:id>', methods=['GET', 'POST'])
    def editar(id):
        try:
            # Obtener el producto a editar de la base de datos
            producto = db_session.query(Producto).filter_by(id=id).one()
            categoria = db_session.query(Categoria).filter(Categoria.activo == True).all()
            if request.method == 'POST':
                # Obtener los datos del formulario
                codigo_barra = request.form['codigo_barra']
                nombre = request.form['nombre']
                stock = request.form['stock']
                categoria_id = request.form['categoria_id']
                descripcion = request.form['descripcion']
                precio = request.form['precio']
                alerta_stock = request.form['alerta_stock'] 
                tiene_receta = True if request.form['tiene_receta'] == "True" else False

                # Actualizar los datos del producto con los nuevos datos del formulario
                if codigo_barra:
                    producto.codigo_barra = codigo_barra
                if nombre:
                    producto.nombre = nombre
                if stock:
                    producto.stock = stock
                if categoria_id:
                    producto.categoria_id = categoria_id
                if descripcion:
                    producto.descripcion = descripcion
                if precio:
                    producto.precio = precio
                if alerta_stock:
                    producto.alerta_stock = alerta_stock
                    
                producto.tiene_receta = tiene_receta

                # Actualizar la imagen del producto si se ha enviado una nueva
                imagen = request.files['imagen']

                if imagen and imagen.filename:
                # Cambiar el nombre del archivo de la imagen al nombre del producto con extensión ".webp"
                    filename = secure_filename(f"{nombre}.webp")
                    image_path = os.path.join('app', 'static', 'img', 'productos', filename)
                    
                    # Guardar la imagen original en el servidor
                    imagen.save(image_path)
                    
                    # Redimensionar y guardar la imagen en formato WebP
                    with Image.open(image_path) as img:
                        img.thumbnail((128, 128))
                        img.save(image_path, format='WEBP')

                producto.imagen = '/productos/' + filename

                # Registrar ultima modificación
                producto.ultima_modificacion = datetime.now()
                
                # Guardar los cambios en la base de datos
                db_session.commit()

                # Redireccionar al listado de productos
                return redirect(url_for('producto.listar'))
        except:
            print("ERROR DESCONOCIDO: informe con el desarrollador sobre este problema.")
            db_session.rollback()
            return redirect(request.path)

        # Renderizar la plantilla de edición de productos
        return render_template('producto/editar.html', producto=producto, categoria=categoria)
    
    @producto_blueprint.route('/producto/duplicar/<int:id>', methods=['GET', 'POST'])
    def duplicar(id):
        try:
            # Obtener el producto original de la base de datos
            producto_original = db_session.query(Producto).filter_by(id=id).one()
            categoria = db_session.query(Categoria).filter(Categoria.activo == True).all()

            if request.method == 'POST':
                # Crear una instancia de Producto con los datos del formulario
                nuevo_producto = Producto()
                nuevo_producto.codigo_barra = request.form['codigo_barra']
                nuevo_producto.nombre = request.form['nombre']
                nuevo_producto.stock = request.form['stock']
                nuevo_producto.categoria_id = request.form['categoria_id']
                nuevo_producto.descripcion = request.form['descripcion']
                nuevo_producto.precio = request.form['precio']
                nuevo_producto.alerta_stock = request.form['alerta_stock']
                nuevo_producto.tiene_receta = True if request.form['tiene_receta'] == "True" else False
                nuevo_producto.imagen = producto_original.imagen

                producto_existente = db_session.query(Producto).filter_by(codigo_barra=nuevo_producto.codigo_barra).first()
                if producto_existente:
                    flash('El código de barras ya está en uso. Por favor, elija otro.', 'error')
                    return render_template('producto/duplicar.html', producto=producto_original, categoria=categoria)

                imagen = request.files['imagen']
                
                if imagen and imagen.filename:
                    # Cambiar el nombre del archivo de la imagen al nombre del producto con extensión ".webp"
                    filename = secure_filename(f"{nombre}.webp")
                    image_path = os.path.join('app', 'static', 'img', 'productos', filename)
                    
                    # Guardar la imagen original en el servidor
                    imagen.save(image_path)
                    
                    # Redimensionar y guardar la imagen en formato WebP
                    with Image.open(image_path) as img:
                        img.thumbnail((128, 128))
                        img.save(image_path, format='WEBP')

                    producto.imagen = '/productos/' + filename
                    
                # Registrar fecha de creación
                nuevo_producto.fecha_creacion = datetime.now()

                # Guardar el nuevo producto en la base de datos
                db_session.add(nuevo_producto)
                db_session.commit()

                # Redireccionar al listado de productos
                return redirect(url_for('producto.listar'))
        except:
            print("ERROR DESCONOCIDO: informe con el desarrollador sobre este problema.")
            db_session.rollback()
            return redirect(request.path)

        # Renderizar la plantilla de duplicación de productos
        return render_template('producto/duplicar.html', producto=producto_original, categoria=categoria)

    @producto_blueprint.route('/producto/ingresar_stock/<int:id>', methods=['GET', 'POST'])
    def ingresar_stock(id):
        try:
            # Obtener el producto a editar de la base de datos
            producto = db_session.query(Producto).filter_by(id=id).one()
            if request.method == 'POST':
                # Obtener los datos del formulario
                cantidad = request.form['cantidad']

                # Actualizar los datos del producto con los nuevos datos del formulario
                if cantidad:
                    producto.stock = producto.stock + int(cantidad)
                    
                # Registrar ultima modificación
                producto.ultima_modificacion = datetime.now()
                
                # Guardar los cambios en la base de datos
                db_session.commit()

                # Redireccionar al listado de productos
                return redirect(url_for('producto.listar'))
        except:
            print("ERROR DESCONOCIDO: informe con el desarrollador sobre este problema.")
            db_session.rollback()
            return redirect(request.path)

        # Renderizar la plantilla de edición de productos
        else:
            return render_template('producto/ingresar_stock.html', producto=producto)
        
    @producto_blueprint.route('/reporte/ingresar_stock/<int:id>', methods=['GET', 'POST'])
    def ingresar_stock_reporte(id):
        try:
            # Obtener el producto a editar de la base de datos
            producto = db_session.query(Producto).filter_by(id=id).one()
            if request.method == 'POST':
                # Obtener los datos del formulario
                cantidad = request.form['cantidad']

                # Actualizar los datos del producto con los nuevos datos del formulario
                if cantidad:
                    producto.stock = producto.stock + int(cantidad)
                    
                # Registrar ultima modificación
                producto.ultima_modificacion = datetime.now()
                
                # Guardar los cambios en la base de datos
                db_session.commit()

                # Redireccionar al listado de productos
                return redirect(url_for('reporte.inventario'))
        except:
            print("ERROR DESCONOCIDO: informe con el desarrollador sobre este problema.")
            db_session.rollback()
            return redirect(request.path)

        # Renderizar la plantilla de edición de productos
        else:
            return render_template('producto/ingresar_stock_reporte.html', producto=producto)

    @producto_blueprint.route('/producto/eliminar/<int:id>', methods=['GET', 'POST'])
    def eliminar(id):
        try:
            producto = db_session.query(Producto).filter_by(id=id).one()
            if request.method == 'POST':
                producto.activo = False
                db_session.commit()
                return redirect(url_for('producto.listar'))
            else:
                return render_template('producto/eliminar.html', producto=producto)
        except:
            print("ERROR DESCONOCIDO: informe con el desarrollador sobre este problema.")
            db_session.rollback()
            return redirect(request.path)

    # Devolver el blueprint
    return producto_blueprint
