from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from models.database import Usuario, Producto, Categoria, Ingrediente, UnidadMedida, Rol, Persona, Receta, RecetaDetalle, db, db_session
from db_init import init_db
from datetime import datetime
import arrow, bcrypt
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from config import *

from controllers.categoria_controller import create_categoria_blueprint
from controllers.producto_controller import create_producto_blueprint
from controllers.ingrediente_controller import create_ingrediente_blueprint

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

@app.route('/caja')
def caja():
    return render_template('caja.html')

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
    rol = db_session.query(Rol).all()
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
    rol = db_session.query(Rol).all()

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
            persona_existente = db_session.query(Persona).filter_by(rut=rut).first()

            if persona_existente:
                error = 'El RUT ya existe en la base de datos.'
            else:
                usuario = Usuario(nombre_usuario=nombre_usuario, correo=correo, contrasena=contrasena_hash, rol_id=rol_id)
                try:
                    db_session.add(usuario)
                    db_session.commit()

                    # Asignar el ID del usuario creado a persona.usuario_id
                    nueva_persona = Persona(usuario_id=usuario.id, rut=rut, nombre=nombre, apellido_paterno=apellido_paterno,
                                            apellido_materno=apellido_materno, celular=celular)
                    db_session.add(nueva_persona)
                    db_session.commit()

                    flash('El usuario ha sido creado exitosamente.', 'success')
                    return redirect(url_for('usuarios'))
                except IntegrityError:
                    db_session.rollback()
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
    persona = db_session.query(Persona).filter(Persona.usuario_id == usuario.id).first()
    
    if usuario is None:
        flash('El usuario no existe', 'error')
        return redirect(url_for('usuarios'))

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
            
            # Si se proporciona una nueva contraseña, se actualiza
            if contrasena:
                contrasena_hash = bcrypt.hashpw(contrasena.encode(), bcrypt.gensalt())
                usuario.contrasena = contrasena_hash
                
            usuario.ultima_modificacion = datetime.now()                
            db_session.commit()
            
            # Actualizar los datos de la persona asociada al usuario
            if persona:
                persona.rut = rut
                persona.nombre = nombre
                persona.apellido_paterno = apellido_paterno
                persona.apellido_materno = apellido_materno
                persona.celular = celular
                persona.ultima_modificacion = datetime.now()             
            db_session.commit()
            
            flash('Usuario actualizado exitosamente', 'success')
            return redirect(url_for('usuarios'))
    
    return render_template('usuario/editar.html', usuario=usuario, rol=rol, persona=persona)


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