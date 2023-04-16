from flask import Flask, flash, render_template
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/')
def index():
    flash('Hola, mundo!')
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
