import os

# Nombre de aplicación
app_name_cfg = 'Pizzería Fratelli'

# Otras variables de configuración
secret_key_cfg = os.urandom(24)

# Habilitar modo depurador
debug_cfg = False

# hosting
#host_cfg = '127.0.0.1'
port_cfg = 5000

# mysql credenciales
mysql = {
    'nombre_base_datos_db': 'test',
    'host_db': 'localhost',
    'usuario_db': 'root',
    'contrasena_db': '',
    'puerto_db': 3306
}

# Archivo de configuración
UPLOAD_FOLDER = 'app\static\img'