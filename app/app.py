# Importamos las librerías necesarias
import bcrypt
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, func
from database import Usuario, Producto, Categoria, Ingrediente, UnidadMedida, Rol, Persona, db, usuario_db, contrasena_db, host_db, puerto_db, nombre_base_datos_db, db_session
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
import os
from db_init import init_db
from datetime import datetime
import arrow
from sqlalchemy.exc import IntegrityError

# Configurar la aplicación
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{usuario_db}:{contrasena_db}@{host_db}:{puerto_db}/{nombre_base_datos_db}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = os.urandom(24)

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
    productos = []
    producto_busqueda = request.form.get('producto_busqueda')
    if request.method == 'POST':
        if producto_busqueda:
            productos = productos = db_session.query(Producto).join(Categoria).filter(or_(Producto.nombre.ilike(f'%{producto_busqueda}%'),
                                                                                       Categoria.nombre.ilike(f'%{producto_busqueda}%'),
                                                                                       Producto.codigo_barra == producto_busqueda)).all()
        else:
            mensaje = "Por favor, ingrese el nombre o código de barras de un producto"
            return render_template('vender.html', producto_busqueda=producto_busqueda, mensaje=mensaje)
        return render_template('vender/vender.html', productos=productos)
    
    return render_template('vender/vender.html', productos=productos, producto_busqueda=producto_busqueda)

@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    producto_id = request.form.get('producto_id')
    cantidad = request.form.get('cantidad')
    
    producto = Producto.query.filter_by(id=producto_id).first()
    if not producto:
        flash('El producto no existe', 'error')
        return redirect(url_for('vender'))
    
    if int(cantidad) > producto.stock:
        flash('No hay suficiente stock del producto', 'error')
        return redirect(url_for('vender'))
    
    # Crear una nueva venta o actualizar una existente en la sesión
    venta = db_session.get('venta')
    if not venta:
        venta = {'productos': {}, 'total': 0}
    
    if producto_id in venta['productos']:
        venta['productos'][producto_id]['cantidad'] += int(cantidad)
        venta['productos'][producto_id]['subtotal'] += float(producto.precio) * int(cantidad)
    else:
        venta['productos'][producto_id] = {
            'nombre': producto.nombre,
            'precio': float(producto.precio),
            'cantidad': int(cantidad),
            'subtotal': float(producto.precio) * int(cantidad)
        }
    
    venta['total'] += float(producto.precio) * int(cantidad)
    
    db_session['venta'] = venta
    
    flash('Producto agregado a la venta', 'success')
    
    return redirect(url_for('vender'))

@app.route('/ventas')
def ventas():
    return render_template('ventas.html')

@app.route('/caja')
def caja():
    return render_template('caja.html')

@app.route('/categorias')
def categorias():
    # Obtenemos todas las categorías de la base de datos
    categorias = db_session.query(Categoria).all()
    
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
    return render_template('categoria/categorias.html', categorias=categorias, hay_activas=hay_activas)
    
@app.route('/categoria/nueva', methods=['GET', 'POST'])
def categoria_nueva():
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre']

        # Crear una nueva categoría
        nueva_categoria = Categoria(nombre=nombre)

        # Guardar la nueva categoría en la base de datos
        db_session.add(nueva_categoria)
        db_session.commit()

        return redirect(url_for('categorias'))
    return render_template('categoria/nueva.html')

@app.route('/categoria/editar/<int:id>', methods=['GET', 'POST'])
def categoria_editar(id):
    categoria = db_session.query(Categoria).filter_by(id=id).one()
    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria.ultima_modificacion = datetime.now()
        categoria.nombre = nombre
        db_session.commit()
        return redirect(url_for('categorias'))
    else:
        return render_template('categoria/editar.html', categoria=categoria)

@app.route('/categoria/eliminar/<int:id>', methods=['GET', 'POST'])
def categoria_eliminar(id):
    categoria = db_session.query(Categoria).filter_by(id=id).one()
    if request.method == 'POST':
        categoria.activo = 0
        db_session.commit()
        return redirect(url_for('categorias'))
    else:
        return render_template('categoria/eliminar.html', categoria=categoria)

@app.route('/categorias/papelera')
def categoria_papelera():
    # Obtenemos todas los categorias de la base de datos
    categorias = db_session.query(Categoria).all()
    
    # Verificamos si hay al menos un categoria no activo
    hay_activas = any(categoria.activo for categoria in categorias)
    i = 0
    for categoria in categorias:
        if not categoria.activo:
            i=i+1
    if i>=1:
        hay_activas = True
    if i == 0:
        hay_activas = False

    return render_template('categoria/papelera.html', categorias=categorias, hay_activas=hay_activas)

@app.route('/categoria/restaurar/<int:id>', methods=['GET', 'POST'])
def categoria_restaurar(id):
    categoria = db_session.query(Categoria).filter_by(id=id).one()
    if request.method == 'POST':
        categoria.activo = 1
        db_session.commit()
        return redirect(url_for('categorias'))
    else:
        return render_template('categoria/restaurar.html', categoria=categoria)



@app.route('/clientes')
def clientes():
    return render_template('clientes.html')

@app.route('/personas')
def personas():
    usuario = db_session.query(Usuario).all()
    personas = db_session.query(Persona).all()
    for usuario in personas:
        fecha_creacion = arrow.get(usuario.fecha_creacion).to('America/Santiago').format('DD-MM-YYYY HH:mm') if usuario.fecha_creacion else None
        ultima_modificacion = arrow.get(usuario.ultima_modificacion).to('America/Santiago').format('DD-MM-YYYY HH:mm') if usuario.ultima_modificacion else None
    return render_template('persona/personas.html', personas=personas, usuario=usuario)

@app.route('/persona/nuevo', methods=['GET', 'POST'])
def persona_nuevo():
    error = None
    usuario = db_session.query(Usuario).all()
    if request.method == 'POST':
        nombre_persona = request.form['nombre_persona']
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        confirmar_contrasena = request.form['confirmar_contrasena']
        rol_id = request.form['rol_id']

        if contrasena != confirmar_contrasena:
            error = "Las contraseñas no coinciden"
        else:
            contrasena_hash = bcrypt.hashpw(contrasena.encode(), bcrypt.gensalt())
            persona = persona(nombre_persona=nombre_persona, correo=correo, contrasena=contrasena_hash, rol_id=rol_id)
            try:
                db_session.add(persona)
                db_session.commit()
                flash('El persona ha sido creado exitosamente.', 'success')
                return redirect(url_for('personas'))
            except IntegrityError:
                db_session.rollback()
                error = "El nombre de persona o correo electrónico ya están en uso"
    return render_template('persona/nuevo.html', error=error, rol=rol)
    
@app.route('/personas/papelera')
def persona_papelera():
    rol = db_session.query(Rol).all()
    # Obtenemos todos los personas de la base de datos
    personas = db_session.query(persona).all()

    # Verificamos si hay al menos un persona no activo
    hay_activos = any(persona.activo for persona in personas)
    i = 0
    for persona in personas:
        if not persona.activo:
            i=i+1
    if i>=1:
        hay_activos = True
    if i == 0:
        hay_activos = False

    return render_template('persona/papelera.html', personas=personas, hay_activos=hay_activos)

@app.route('/persona/restaurar/<int:id>', methods=['GET', 'POST'])
def persona_restaurar(id):
    rol = db_session.query(Rol).all()
    persona = db_session.query(persona).filter_by(id=id).one()
    if request.method == 'POST':
        persona.activo = 1
        db_session.commit()
        return redirect(url_for('personas'))
    else:
        return render_template('persona/restaurar.html', persona=persona)

@app.route('/persona/editar/<int:id>', methods=['GET', 'POST'])
def persona_editar(id):
    rol = db_session.query(Rol).all()
    persona = db_session.query(persona).get(id)

    if not persona:
        flash('El persona no existe', 'error')
        return redirect(url_for('personas'))

    if request.method == 'POST':
        nombre_persona = request.form['nombre_persona']
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        confirmar_contrasena = request.form['confirmar_contrasena']
        rol_id = request.form['rol_id']
        
        # Validar formulario
        if not nombre_persona:
            flash('El nombre de persona es requerido', 'error')
        elif not correo:
            flash('El correo electrónico es requerido', 'error')
        elif contrasena != confirmar_contrasena:
            flash('Las contraseñas no coinciden', 'error')
        else:
            # Actualizar persona
            persona.nombre_persona = nombre_persona
            persona.correo = correo
            persona.rol_id = rol_id
            if contrasena:
                contrasena_hash = bcrypt.hashpw(contrasena.encode(), bcrypt.gensalt())
                persona.contrasena = contrasena_hash
            persona.ultima_modificacion = datetime.now()
            db_session.commit()
            
            flash('persona actualizado exitosamente', 'success')
            return redirect(url_for('personas'))
    return render_template('persona/editar.html', persona=persona, rol=rol)

@app.route('/persona/eliminar/<int:id>', methods=['GET', 'POST'])
def persona_eliminar(id):
    persona = db_session.query(persona).filter_by(id=id).one()
    if request.method == 'POST':
        persona.activo = 0
        db_session.commit()
        return redirect(url_for('personas'))
    else:
        return render_template('persona/eliminar.html', persona=persona)

@app.route('/usuarios')
def usuarios():
    rol = db_session.query(Rol).all()
    usuarios = db_session.query(Usuario).all()
    for usuario in usuarios:
        fecha_creacion = arrow.get(usuario.fecha_creacion).to('America/Santiago').format('DD-MM-YYYY HH:mm') if usuario.fecha_creacion else None
        ultima_modificacion = arrow.get(usuario.ultima_modificacion).to('America/Santiago').format('DD-MM-YYYY HH:mm') if usuario.ultima_modificacion else None
    return render_template('usuario/usuarios.html', usuarios=usuarios, rol=rol)

@app.route('/usuario/nuevo', methods=['GET', 'POST'])
def usuario_nuevo():
    error = None
    rol = db_db_session.query(Rol).all()

    if request.method == 'POST':
        nombre_usuario = request.form['nombre_usuario']
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        confirmar_contrasena = request.form['confirmar_contrasena']
        rol_id = request.form['rol_id']
        rut = request.form['rut']
        nombre = request.form['nombre']
        apellido_paterno = request.form['apellido_paterno']
        apellido_materno = request.form['apellido_materno']
        celular = request.form['celular']

        if contrasena != confirmar_contrasena:
            error = "Las contraseñas no coinciden"
        else:
            contrasena_hash = bcrypt.hashpw(contrasena.encode(), bcrypt.gensalt())

            # Verificar si el RUT ya existe en la base de datos
            persona_existente = db_db_session.query(Persona).filter_by(rut=rut).first()

            if persona_existente:
                error = 'El RUT ya existe en la base de datos.'
            else:
                usuario = Usuario(nombre_usuario=nombre_usuario, correo=correo, contrasena=contrasena_hash, rol_id=rol_id)
                try:
                    db_db_session.add(usuario)
                    db_db_session.commit()

                    # Asignar el ID del usuario creado a persona.usuario_id
                    nueva_persona = Persona(usuario_id=usuario.id, rut=rut, nombre=nombre, apellido_paterno=apellido_paterno,
                                            apellido_materno=apellido_materno, celular=celular)
                    db_db_session.add(nueva_persona)
                    db_db_session.commit()

                    flash('El usuario ha sido creado exitosamente.', 'success')
                    return redirect(url_for('usuarios'))
                except IntegrityError:
                    db_db_session.rollback()
                    error = "El nombre de usuario o correo electrónico ya están en uso"

    return render_template('usuario/nuevo.html', error=error, rol=rol)
    
@app.route('/usuarios/papelera')
def usuario_papelera():
    rol = db_session.query(Rol).all()
    # Obtenemos todos los usuarios de la base de datos
    usuarios = db_session.query(Usuario).all()

    # Verificamos si hay al menos un usuario no activo
    hay_activos = any(usuario.activo for usuario in usuarios)
    i = 0
    for usuario in usuarios:
        if not usuario.activo:
            i=i+1
    if i>=1:
        hay_activos = True
    if i == 0:
        hay_activos = False

    return render_template('usuario/papelera.html', usuarios=usuarios, hay_activos=hay_activos)

@app.route('/usuario/restaurar/<int:id>', methods=['GET', 'POST'])
def usuario_restaurar(id):
    rol = db_session.query(Rol).all()
    usuario = db_session.query(Usuario).filter_by(id=id).one()
    if request.method == 'POST':
        usuario.activo = 1
        db_session.commit()
        return redirect(url_for('usuarios'))
    else:
        return render_template('usuario/restaurar.html', usuario=usuario)

@app.route('/usuario/editar/<int:id>', methods=['GET', 'POST'])
def usuario_editar(id):
    rol = db_session.query(Rol).all()
    usuario = db_session.query(Usuario).get(id)

    if not usuario:
        flash('El usuario no existe', 'error')
        return redirect(url_for('usuarios'))

    if request.method == 'POST':
        nombre_usuario = request.form['nombre_usuario']
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        confirmar_contrasena = request.form['confirmar_contrasena']
        rol_id = request.form['rol_id']
        
        # Validar formulario
        if not nombre_usuario:
            flash('El nombre de usuario es requerido', 'error')
        elif not correo:
            flash('El correo electrónico es requerido', 'error')
        elif contrasena != confirmar_contrasena:
            flash('Las contraseñas no coinciden', 'error')
        else:
            # Actualizar usuario
            usuario.nombre_usuario = nombre_usuario
            usuario.correo = correo
            usuario.rol_id = rol_id
            if contrasena:
                contrasena_hash = bcrypt.hashpw(contrasena.encode(), bcrypt.gensalt())
                usuario.contrasena = contrasena_hash
            usuario.ultima_modificacion = datetime.now()
            db_session.commit()
            
            flash('Usuario actualizado exitosamente', 'success')
            return redirect(url_for('usuarios'))
    return render_template('usuario/editar.html', usuario=usuario, rol=rol)

@app.route('/usuario/eliminar/<int:id>', methods=['GET', 'POST'])
def usuario_eliminar(id):
    usuario = db_session.query(Usuario).filter_by(id=id).one()
    if request.method == 'POST':
        usuario.activo = 0
        db_session.commit()
        return redirect(url_for('usuarios'))
    else:
        return render_template('usuario/eliminar.html', usuario=usuario)

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
    # Cerrar sesión asignando False a la sesión 
    session['logged_in'] = False
    # Agregar mensaje de "Has cerrado sesión"
    flash('Has cerrado sesión', 'success')
    # Redirecciona al usuario a la página de inicio de sesión después de cerrar sesión
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre_usuario = request.form['nombre_usuario']
        contrasena = request.form['contrasena']

        # Verificar si el nombre_usuario y la contraseña coinciden con un usuario en la base de datos
        usuario = db_session.query(Usuario).filter_by(nombre_usuario=nombre_usuario).first()
        persona = db_session.query(Persona).filter_by(usuario_id=usuario.id).first()

        if usuario and bcrypt.checkpw(contrasena.encode(), usuario.contrasena.encode()):
            # Establecer la sesión del usuario como iniciada
            session['logged_in'] = True
            session['user_id'] = usuario.id
            session['user_nombre'] = persona.nombre  # Guardar el nombre de usuario en la sesión

            flash('Sesión iniciada correctamente', 'success')
            return redirect(url_for('index'))
        else:
            flash('Credenciales inválidas', 'error')
            return redirect(url_for('login'))

    return render_template('sesion/login.html')

@app.route('/productos')
def productos():
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
    return render_template('producto/productos.html', productos=productos, hay_activas=hay_activas)

@app.route('/productos/papelera')
def producto_papelera():
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

@app.route('/producto/nuevo', methods=['GET', 'POST'])
def producto_nuevo():
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
        
        # Ruta de las imágenes
        app.config['UPLOAD_FOLDER'] = 'app\static\img\productos'

        if imagen and imagen.filename:
            filename = secure_filename(imagen.filename)
            imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            nuevo_producto.imagen = '/productos/' + filename
        else:
            filename = None
            nuevo_producto.imagen = None
        
        # Agregar el producto a la base de datos
        db_session.add(nuevo_producto)
        db_session.commit()
        
        # Redireccionar al listado de productos
        return redirect(url_for('productos'))
    
    # Renderizar la plantilla de nuevo producto
    return render_template('producto/nuevo.html', categorias=categorias)

@app.route('/producto/restaurar/<int:id>', methods=['GET', 'POST'])
def producto_restaurar(id):
    producto = db_session.query(Producto).filter_by(id=id).one()
    if request.method == 'POST':
        producto.activo = 1
        db_session.commit()
        return redirect(url_for('productos'))
    else:
        return render_template('producto/restaurar.html', producto=producto)
    
@app.route('/producto/reporte')
def producto_reporte():
    return render_template('producto/reporte.html')

@app.route('/producto/editar/<int:id>', methods=['GET', 'POST'])
def producto_editar(id):
    # Obtener el producto a editar de la base de datos
    producto = db_session.query(Producto).filter_by(id=id).one()
    categorias = db_session.query(Categoria).all()
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
            app.config['UPLOAD_FOLDER'] = 'app\static\img\productos'
            imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            producto.imagen = '/productos/' + filename
        
        # Registrar ultima modificación
        producto.ultima_modificacion = datetime.now()
        
        # Guardar los cambios en la base de datos
        db_session.commit()

        # Redireccionar al listado de productos
        return redirect(url_for('productos'))

    # Renderizar la plantilla de edición de productos
    return render_template('producto/editar.html', producto=producto, categorias=categorias)

@app.route('/producto/eliminar/<int:id>', methods=['GET', 'POST'])
def producto_eliminar(id):
    producto = db_session.query(Producto).filter_by(id=id).one()
    if request.method == 'POST':
        producto.activo = 0
        db_session.commit()
        return redirect(url_for('productos'))
    else:
        return render_template('producto/eliminar.html', producto=producto)

@app.route('/ingredientes')
def ingredientes():
    # Obtenemos todas los ingredientes de la base de datos
    ingredientes = db_session.query(Ingrediente).all()
    # Verificamos si hay al menos un producto activo
    hay_activas = any(ingrediente.activo for ingrediente in ingredientes)
    i = 0
    for ingrediente in ingredientes:
        if ingrediente.activo:
            i=i+1
    if i>=1:
        hay_activas = True
    if i == 0:
        hay_activas = False
    return render_template('ingredientes/ingredientes.html', ingredientes=ingredientes, hay_activas=hay_activas)

@app.route('/ingrediente_papelera')
def ingrediente_papelera():
    return render_template('ingredientes/papelera.html')

@app.route('/ingrediente_nuevo', methods=['GET', 'POST'])
def ingrediente_nuevo():
    # Obtener las categorías para mostrarlas en el formulario
    unidadmedida = db_session.query(UnidadMedida).all()
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.files['nombre']
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
        return redirect(url_for('ingredientes'))
    
    # Renderizar la plantilla ingredientes
    return render_template('ingredientes/nuevo.html', unidadmedida=unidadmedida)

@app.route('/ingrediente_editar')
def ingrediente_editar():
    return render_template('ingredientes/editar.html')

@app.route('/ingrediente_eliminar')
def ingrediente_eliminar():
    return render_template('ingredientes/eliminar.html')

if __name__ == '__main__':
    app.debug = True
    app.run()