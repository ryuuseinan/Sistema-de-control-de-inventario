# Importamos las librerías necesarias
from flask import Flask, render_template
import secrets
from database import engine

# Creamos la aplicación Flask
app = Flask(__name__)

# Generamos una clave secreta aleatoria y la establecemos en la aplicación
app.secret_key = secrets.token_hex(16)

# Creamos la ruta para la página principal
@app.route('/')
def index():
    # Renderizamos el archivo index.html
    return render_template('index.html')

# Iniciamos la aplicación si se ejecuta este archivo directamente
if __name__ == '__main__':
    app.run()