# Importamos las librerías necesarias
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exists
from database import User, Product, Category, db, usuario, contrasena, host, puerto, nombre_base_datos, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
import os
from db_init import init_db
from datetime import datetime

# Configurar la aplicación
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{usuario}:{contrasena}@{host}:{puerto}/{nombre_base_datos}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = os.urandom(24)
# Forzar eliminación de caché
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

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

@app.route('/vender')
def vender():
    return render_template("vender.html")

@app.route('/ventas')
def ventas():
    return render_template('ventas.html')

@app.route('/caja')
def caja():
    return render_template('caja.html')

@app.route('/categorias')
def categorias():
    # Obtenemos todas las categorías de la base de datos
    categorias = session.query(Category).all()
    
    # Verificamos si hay al menos una categoría activa
    hay_activas = any(categoria.activo for categoria in categorias)
    
    i = 0
    for categoria in categorias:
        if categoria.activo:
            i=i+1
    if i>=1:
        hay_activas = True
    if i == 0:
        hay_activas = False

    # Renderizamos el template correspondiente
    return render_template('categorias.html', categorias=categorias, hay_activas=hay_activas)
    
@app.route('/categoria/nueva', methods=['GET', 'POST'])
def categoria_nueva():
    if request.method == 'POST':
        # Obtener los datos del formulario
        name = request.form['name']

        # Crear una nueva categoría
        nueva_categoria = Category(name=name)

        # Guardar la nueva categoría en la base de datos
        db.session.add(nueva_categoria)
        db.session.commit()

        return redirect(url_for('categorias'))
    return render_template('categoria/nueva.html')


@app.route('/categoria/editar/<int:id>', methods=['GET', 'POST'])
def categoria_editar(id):
    categoria = session.query(Category).filter_by(id=id).one()
    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria.name = nombre
        session.commit()
        return redirect(url_for('categorias'))
    else:
        return render_template('categoria/editar.html', categoria=categoria)

@app.route('/categoria/eliminar/<int:id>', methods=['GET', 'POST'])
def categoria_eliminar(id):
    categoria = session.query(Category).filter_by(id=id).one()
    if request.method == 'POST':
        categoria.activo = 0
        session.commit()
        return redirect(url_for('categorias'))
    else:
        return render_template('categoria/eliminar.html', categoria=categoria)


@app.route('/clientes')
def clientes():
    return render_template('clientes.html')

@app.route('/proveedores')
def proveedores():
    return render_template('proveedores.html')

@app.route('/usuarios')
def usuarios():
    return render_template('usuarios.html')

@app.route('/reportes')
def reportes():
    return render_template('reportes.html')

@app.route('/configuracion')
def configuracion():
    return render_template('configuracion.html')

@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtener datos del formulario
        username = request.form['username']
        password = request.form['password']

        # Verificar si las credenciales son válidas
        db_session = session

        user = db_session.query(User).filter_by(username=username).first()
        
        if user is not None and user.password == password:
            # Iniciar sesión y redirigir a la página de inicio
            db.session['logged_in'] = True
            db.session['user_id'] = user.id
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('index'))
        
        flash('Credenciales inválidas. Por favor, intente de nuevo.', 'danger')

    # Renderizar la plantilla del formulario de inicio de sesión
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():

    error = None
    '''if request.method == 'POST':
        # Obtener datos del formulario
        email = request.form['email']
        password = request.form['password']
        
        try:
            # Verificar si el correo electrónico ya está registrado
            db_session = Session()
            email_exists = db_session.query(exists().where(Gestor.email == email)).scalar()
            if email_exists:
                error = 'El correo electrónico ya está registrado. Intente con otro.'
                return render_template('register.html', error=error)

            # Crear nueva instancia de Gestor con los datos del formulario
            nuevo_gestor = Gestor(email=email, password=password)
            
            # Guardar nuevo_gestor en la base de datos
            db_session.add(nuevo_gestor)
            db_session.commit()
            
            flash('Registro exitoso. Inicie sesión para continuar.')
            return redirect(url_for('login'))
            
        except Exception as e:
            # Mostrar mensaje de error si ocurre algún problema con la base de datos
            flash('Ocurrió un error al procesar la solicitud. Inténtelo de nuevo.')
            print(str(e))
        
        finally:
            # Cerrar la sesión de la base de datos
            db_session.close()
    
    # Renderizar la plantilla del formulario de registro'''
    return render_template('register.html', error=error)

@app.route('/productos')
def productos():
    # Obtenemos todas los productos de la base de datos
    productos = session.query(Product).all()
    
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

    return render_template('productos.html', productos=productos, hay_activas=hay_activas)

@app.route('/producto/nuevo', methods=['GET', 'POST'])
def producto_nuevo():
    # Obtener las categorías para mostrarlas en el formulario
    categorias = session.query(Category).all()
    
    if request.method == 'POST':
        # Obtener los datos del formulario
        image = request.files['image']
        barcode = request.form['barcode']
        name = request.form['name']
        category_id = request.form['category_id']
        description = request.form['description']
        price_in = request.form['price_in']
        price_out = request.form['price_out']

        # Crear una nueva instancia de Producto con los datos del formulario
        nuevo_producto = Product(barcode=barcode, name=name, description=description, category_id=category_id, price_in=price_in, price_out=price_out, created_at=datetime.now())
        # Ruta de las imágenes
        app.config['UPLOAD_FOLDER'] = 'app\static\img\productos'

        if image and image.filename:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            nuevo_producto.image = '/productos/' + filename
        else:
            filename = None
            nuevo_producto.image = None
        
        # Agregar el producto a la base de datos
        session.add(nuevo_producto)
        session.commit()
        
        # Redireccionar al listado de productos
        return redirect(url_for('productos'))
    
    # Renderizar la plantilla de nuevo producto
    return render_template('producto/nuevo.html', categorias=categorias)


@app.route('/producto/reporte')
def producto_reporte():
    return render_template('producto/reporte.html')

@app.route('/producto/editar/<int:id>', methods=['GET', 'POST'])
def producto_editar(id):
    producto = session.query(Product).filter_by(id=id).one()
    if request.method == 'POST':
        nombre = request.form['nombre']
        producto.name = nombre
        session.commit()
        return redirect(url_for('productos'))
    else:
        return render_template('producto/editar.html', producto=producto)
    
@app.route('/producto/eliminar/<int:id>', methods=['GET', 'POST'])
def producto_eliminar(id):
    producto = session.query(Product).filter_by(id=id).one()
    if request.method == 'POST':
        nombre = request.form['nombre']
        producto.name = nombre
        session.commit()
        return redirect(url_for('productos'))
    else:
        return render_template('producto/eliminar.html', producto=producto)

if __name__ == '__main__':
    app.debug = True
    app.run()