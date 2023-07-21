from flask import Flask, render_template
from models.database import db
from db_init import init_db
import arrow
from config import *
import socket
import io
import qrcode
import base64
import webbrowser
from flask_compress import Compress

from controllers.categoria_controller import create_categoria_blueprint
from controllers.producto_controller import create_producto_blueprint
from controllers.ingrediente_controller import create_ingrediente_blueprint
from controllers.sesion_controller import create_sesion_blueprint
from controllers.persona_controller import create_persona_blueprint
from controllers.usuario_controller import create_usuario_blueprint
from controllers.receta_controller import create_receta_blueprint
from controllers.unidadmedida_controller import create_unidadmedida_blueprint
from controllers.rol_controller import create_rol_blueprint
from controllers.pedido_controller import create_pedido_blueprint
from controllers.reporte_controller import create_reporte_blueprint

# Configurar la aplicación
app = Flask(__name__)
app.debug = debug_cfg
sqlite_db_file = "sqlite_database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{sqlite_db_file}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = secret_key_cfg
app.jinja_env.filters['b64encode'] = base64.b64encode
Compress(app)

# Forzar eliminación de caché
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.add_template_global(arrow, 'arrow')

# Configurar la base de datos
db.init_app(app)

# Inicializar la aplicación y la base de datos
with app.app_context():
    init_db()

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

unidadmedida_blueprint = create_unidadmedida_blueprint()
app.register_blueprint(unidadmedida_blueprint)

rol_blueprint = create_rol_blueprint()
app.register_blueprint(rol_blueprint)

pedido_blueprint = create_pedido_blueprint()
app.register_blueprint(pedido_blueprint)

reporte_blueprint = create_reporte_blueprint()
app.register_blueprint(reporte_blueprint)

# Creamos la ruta para la página principal
@app.route('/')
def index():
    # Renderizamos el archivo index.html
    return render_template('index.html')

@app.template_global()
def appName() -> str:
    return app_name_cfg

@app.context_processor
def inject_host_cfg():
    def generate_qr_code(data):
        # Generar el código QR
        qr = qrcode.QRCode(version=1, box_size=10, border=1)
        qr.add_data(data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill="black", back_color="white")

        # Convertir la imagen del código QR en una cadena base64
        qr_img_buffer = io.BytesIO()
        qr_img.save(qr_img_buffer, format='PNG')
        qr_img_buffer.seek(0)
        qr_img_base64 = base64.b64encode(qr_img_buffer.getvalue()).decode()

        return qr_img_base64

    host_cfg = get_local_ip()
    address = f"{host_cfg}:{port_cfg}"
    return dict(host_cfg=host_cfg, port_cfg=port_cfg, address=address, generate_qr_code=generate_qr_code)

@app.errorhandler(404)
def page_not_found(error):
    # Renderiza el template de error 404
    return render_template("404.html"), 404

@app.errorhandler(500)
def handle_internal_server_error(error):
    return render_template('error.html', error_message='Error interno del servidor', error=error), 500

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    local_ip = s.getsockname()[0]
    s.close()
    return local_ip

host_cfg = get_local_ip()

def open_browser():
    webbrowser.open(f"http://{host_cfg}:{port_cfg}/")

if __name__ == '__main__':
    open_browser()
    app.run(port=port_cfg, host=host_cfg)