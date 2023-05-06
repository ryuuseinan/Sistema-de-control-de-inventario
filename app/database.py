from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean, Text, Float
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Crear objeto de base de datos SQLAlchemy
db = SQLAlchemy()

# Cambia las variables según tu configuración
usuario = 'root'
contrasena = ''
host = 'localhost'
puerto = 3306
nombre_base_datos = 'xd'

# Crea la URL de conexión a la base de datos MySQL
url = f'mysql://{usuario}:{contrasena}@{host}:{puerto}/{nombre_base_datos}'

# Crea una instancia de la clase create_engine
engine = create_engine(url)

# Crea una clase que se utilizará para crear objetos de sesión de base de datos
Session = sessionmaker(bind=engine)

# Crea un objeto de sesión de base de datos que se utilizará para enviar consultas a la base de datos.
session = Session()

Base = declarative_base()

# Creamos tabla para almacenar usuarios
class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True)
    nombre_usuario = Column(String(50), unique=True, nullable=False)
    correo = Column(String(255), unique=True, nullable=False)
    contrasena = Column(String(60), nullable=False)
    es_administrador = Column(Boolean, default=False, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.now(), nullable=False)
    ultima_modificacion = Column(DateTime, default=datetime.now(), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)

# Creamos tabla para almacenar categorias
class Categoria(Base):
    __tablename__ = 'categoria'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.now(), nullable=False)
    ultima_modificacion = Column(DateTime, default=datetime.now(), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)

# Creamos tabla para almacenar productos
class Producto(Base):
    __tablename__ = 'producto'
    id = Column(Integer, primary_key=True)
    imagen = Column(String(255))
    codigo_barra = Column(String(50), unique=True, nullable=False)
    nombre = Column(String(50), nullable=False)
    descripcion = Column(Text)
    precio = Column(Integer, nullable=False)
    stock = Column(Integer)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    categoria_id = Column(Integer, ForeignKey('categoria.id'))
    fecha_creacion = Column(DateTime, default=datetime.now(), nullable=False)
    ultima_modificacion = Column(DateTime, default=datetime.now(), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)
    # Crea la relación con Categoría
    categoria = relationship('Categoria')

# Creamos tabla para almacenar personas
class Persona(Base):
    __tablename__ = 'persona'
    id = Column(Integer, primary_key=True)
    rut = Column(String(12), unique=True, nullable=False)
    nombre = Column(String(30), nullable=False)
    apellido = Column(String(30), nullable=False)
    direccion = Column(String(50), nullable=False)
    celular = Column(String(22), nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.now(), nullable=False)
    ultima_modificacion = Column(DateTime, default=datetime.now(), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)

# Creamos tabla para almacenar cajas
class Caja(Base):
    __tablename__ = 'caja'
    id = Column(Integer, primary_key=True)
    fecha_creacion = Column(DateTime, default=datetime.now(), nullable=False)
    ultima_modificacion = Column(DateTime, default=datetime.now(), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)

# Creamos tabla para almacenar ingredientes
class Ingrediente(Base):
    __tablename__ = 'ingrediente'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    precio = Column(Integer, nullable=False)

# Creamos tabla para almacenar los ingredientes de los productos
class ProductoIngrediente(Base):
    __tablename__ = 'producto_ingrediente'
    id = Column(Integer, primary_key=True)
    producto_id = Column(Integer, ForeignKey('producto.id'))
    ingrediente_id = Column(Integer, ForeignKey('ingrediente.id'))

Base.metadata.create_all(engine)