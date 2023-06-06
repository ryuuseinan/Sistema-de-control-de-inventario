from flask import Flask, render_template, request, redirect, url_for, flash, session
from models.database import db
from db_init import init_db
import arrow
from config import *

from controllers.categoria_controller import create_categoria_blueprint
from controllers.producto_controller import create_producto_blueprint
from controllers.ingrediente_controller import create_ingrediente_blueprint
from controllers.sesion_controller import create_sesion_blueprint
from controllers.persona_controller import create_persona_blueprint
from controllers.usuario_controller import create_usuario_blueprint
from controllers.receta_controller import create_receta_blueprint
from controllers.vender_controller import create_vender_blueprint
from controllers.ventas_controller import create_ventas_blueprint

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

receta_blueprint = create_receta_blueprint()
app.register_blueprint(receta_blueprint)

vender_blueprint = create_vender_blueprint()
app.register_blueprint(vender_blueprint)

ventas_blueprint = create_ventas_blueprint()
app.register_blueprint(ventas_blueprint)

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

@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    return redirect(url_for('vender'))

@app.errorhandler(404)
def page_not_found(error):
    # Renderiza el template de error 404
    return render_template("404.html"), 404

if __name__ == '__main__':
    app.debug = True
    app.run()
    #app.run(host='192.168.187.187')