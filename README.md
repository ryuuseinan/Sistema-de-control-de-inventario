# Sistema-de-control-de-inventario
https://lafratelli.com/prueba23/

`cd Sistema de control de inventario`

`python get-pip.py`

`pip install --upgrade pip`

# Instalacion de venv
`python -m venv venv`

# Iniciar venv
+ Windows
`venv\Scripts\activate`

+ Linux/MacOS
`source venv/bin/activate`

# Instalacion de dependencias
`pip install -r requirements.txt`

# Dependencias
```
mysqlclient pymysql
```

# MySQL config
```
use test;
CREATE USER 'hinami'@'localhost' IDENTIFIED BY 'hinami';
GRANT ALL PRIVILEGES ON test.* TO 'hinami'@'localhost';
FLUSH PRIVILEGES;
```

# Ejecutar app
+ Windows: 
`python .\app\app.py`
+ Linux: 
`python ./app/app.py`
