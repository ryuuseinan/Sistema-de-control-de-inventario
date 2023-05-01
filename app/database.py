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
nombre_base_datos = 'invxd'

# Crea la URL de conexión a la base de datos MySQL
url = f'mysql://{usuario}:{contrasena}@{host}:{puerto}/{nombre_base_datos}'

# Crea una instancia de la clase create_engine
engine = create_engine(url)

# Crea una clase que se utilizará para crear objetos de sesión de base de datos
Session = sessionmaker(bind=engine)

# Crea un objeto de sesión de base de datos que se utilizará para enviar consultas a la base de datos.
session = Session()

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    lastname = Column(String(50))
    username = Column(String(50))
    email = Column(String(255))
    password = Column(String(60))
    image = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())
    activo = Column(Boolean, default=True)

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    image = Column(String(255))
    name = Column(String(50))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.now())
    activo = Column(Boolean, default=True)

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    image = Column(String(255))
    barcode = Column(String(50))
    name = Column(String(50))
    description = Column(Text)
    inventary_min = Column(Integer, default=10)
    price_in = Column(Integer)
    price_out = Column(Integer)
    unit = Column(String(255))
    presentation = Column(String(255))
    user_id = Column(Integer, ForeignKey('user.id'))
    category_id = Column(Integer, ForeignKey('category.id'))
    created_at = Column(DateTime, default=datetime.now())
    activo = Column(Boolean, default=True)

    user = relationship('User')
    category = relationship('Category')

class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True, autoincrement=True)
    image = Column(String(255))
    name = Column(String(255))
    lastname = Column(String(50))
    company = Column(String(50))
    address1 = Column(String(50))
    address2 = Column(String(50))
    phone1 = Column(String(50))
    phone2 = Column(String(50))
    email1 = Column(String(50))
    email2 = Column(String(50))
    kind = Column(Integer)
    created_at = Column(DateTime, default=datetime.now())
    activo = Column(Boolean, default=True)

class OperationType(Base):
    __tablename__ = 'operation_type'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    activo = Column(Boolean, default=True)

class Box(Base):
    __tablename__ = 'box'
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.now())
    activo = Column(Boolean, default=True)

class Sell(Base):
    __tablename__ = 'sell'
    id = Column(Integer, primary_key=True, autoincrement=True)
    person_id = Column(Integer, ForeignKey('person.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    operation_type_id = Column(Integer, ForeignKey('operation_type.id'), default=2)
    box_id = Column(Integer, ForeignKey('box.id'))
    total = Column(Integer)
    cash = Column(Integer)
    discount = Column(Float)
    sell_date = Column(DateTime, default=datetime.now())
    created_at = Column(DateTime, default=datetime.now())
    box = relationship('Box')
    operation_type = relationship('OperationType')
    user = relationship('User')
    person = relationship('Person')
    products = relationship('SellProduct', backref='sell', lazy=True)
    activo = Column(Boolean, default=True)

class Operation(Base):
    __tablename__ = 'operation'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'))
    q = Column(Float)
    operation_type_id = Column(Integer, ForeignKey('operation_type.id'))
    sell_id = Column(Integer, ForeignKey('sell.id'))
    created_at = Column(DateTime, default=datetime.utcnow)

    product = relationship('Product')
    operation_type = relationship('OperationType')
    sell = relationship('Sell')
    activo = Column(Boolean, default=True)

class SellProduct(Base):
    __tablename__ = 'sell_product'
    id = Column(Integer, primary_key=True)
    sell_id = Column(Integer, ForeignKey('sell.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    activo = Column(Boolean, default=True)

class PaymentMethod(Base):
    __tablename__ = 'payment_method'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    activo = Column(Boolean, default=True)

class Configuration(Base):
    __tablename__ = 'configuration'
    id = Column(Integer, primary_key=True, autoincrement=True)
    short = Column(String(255), unique=True)
    name = Column(String(255), unique=True)
    kind = Column(Integer)
    val = Column(String(255))
    activo = Column(Boolean, default=True)

Base.metadata.create_all(engine)