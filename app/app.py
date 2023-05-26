from flask import Flask
from vistas import *
from models.database import usuario_db, contrasena_db, host_db, puerto_db, nombre_base_datos_db

# Configurar la aplicación
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{usuario_db}:{contrasena_db}@{host_db}:{puerto_db}/{nombre_base_datos_db}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = os.urandom(24)
 
# Forzar eliminación de caché
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.add_template_global(arrow, 'arrow')

if __name__ == '__main__':
    app.debug = True
    app.run()
    #app.run(host='192.168.187.187')