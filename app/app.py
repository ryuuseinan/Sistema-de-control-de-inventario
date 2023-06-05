from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from models.database import Usuario, Producto, Categoria, Ingrediente, UnidadMedida, Rol, Persona, Receta, RecetaDetalle, db, db_session
from db_init import init_db
from datetime import datetime
import arrow
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from config import *

from controllers.categoria_controller import create_categoria_blueprint
from controllers.producto_controller import create_producto_blueprint
from controllers.ingrediente_controller import create_ingrediente_blueprint
from controllers.sesion_controller import create_sesion_blueprint
from controllers.persona_controller import create_persona_blueprint
from controllers.usuario_controller import create_usuario_blueprint

# Configurar la aplicación
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{usuario_db}:{contrasena_db}@{host_db}:{puerto_db}/{nombre_base_datos_db}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = SECRET_KEY
 
# Importar y registrar los controladores
categoria_blueprint = create_categoria_blueprint()
app.register_blueprint(categoria_blueprint)

producto_blueprint = create_producto_blueprint()
app.register_blueprint(producto_blueprint)

ingrediente_blueprint = create_ingrediente_blueprint()
app.register_blueprint(ingrediente_blueprint)

sesion_blueprint = create_sesion_blueprint()
app.register_blueprint(sesion_blueprint)

persona_blueprint = create_persona_blueprint()
app.register_blueprint(persona_blueprint)

usuario_blueprint = create_usuario_blueprint()
app.register_blueprint(usuario_blueprint)

# Forzar eliminación de caché
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.add_template_global(arrow, 'arrow')

# Configurar la base de datos
db.init_app(app)

# Inicializar la aplicación y la base de datos
with app.app_context():
    init_db()

# Creamos la ruta para la página principal
@app.route('/')
def index():
    # Renderizamos el archivo index.html
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

# Vista para la búsqueda de productos
@app.route('/vender', methods=['GET', 'POST'])
def vender():
    producto_busqueda = request.form.get('producto_busqueda')
    if request.method == 'POST' and producto_busqueda:
        productos = db_session.query(Producto).join(Categoria).filter(or_(Producto.nombre.ilike(f'%{producto_busqueda}%'),
                                                                  Categoria.nombre.ilike(f'%{producto_busqueda}%'),
                                                                  Producto.codigo_barra == producto_busqueda),
                                                             Producto.activo == True).all()
        if not productos:
            flash("No se encontraron productos con ese criterio de búsqueda", "error")
            productos = db_session.query(Producto).filter(Producto.activo == True).all()
    elif request.method == 'POST' and not producto_busqueda:
        flash("Por favor, ingrese el nombre o código de barras de un producto", "error")
        productos = db_session.query(Producto).filter(Producto.activo == True).all()
    else:
        productos = db_session.query(Producto).filter(Producto.activo == True).all()

    return render_template('vender/vender.html', productos=productos, producto_busqueda=producto_busqueda)

@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    return redirect(url_for('vender'))

@app.route('/ventas')
def ventas():
    return render_template('ventas.html')

@app.route('/reportes')
def reportes():
    return render_template('reportes.html')

@app.errorhandler(404)
def page_not_found(error):
    # Renderiza el template de error 404
    return render_template("404.html"), 404

# Función para agregar una receta a un producto
@app.route('/agregar_receta/<int:id>', methods=['GET', 'POST'])
def agregar_receta(id):
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
        return redirect(url_for('agregar_receta', id=producto.id))

    ingrediente = db_session.query(Ingrediente).all()

    return render_template('receta/agregar_receta.html', producto=producto, receta=receta, ingrediente=ingrediente, receta_detalles=receta_detalles)

@app.route('/ingrediente_receta_eliminar/<int:id>', methods=['GET', 'POST'])
def ingrediente_receta_eliminar(id):
    receta_detalle = db_session.query(RecetaDetalle).filter_by(id=id).one()
    if not receta_detalle:
        flash('El ingrediente de la receta no existe', 'error')
        return redirect(url_for('agregar_receta', id=receta_detalle.receta_id))

    # Eliminar el ingrediente de la receta
    db_session.delete(receta_detalle)
    db_session.commit()

    flash('Ingrediente eliminado de la receta exitosamente', 'success')
    return redirect(url_for('agregar_receta', id=receta_detalle.receta_id))

if __name__ == '__main__':
    app.debug = True
    app.run()
    #app.run(host='192.168.187.187')