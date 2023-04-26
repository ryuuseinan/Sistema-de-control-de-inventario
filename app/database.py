from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Cambia las variables según tu configuración
usuario = 'root'
contraseña = ''
host = 'localhost'
puerto = 3306
nombre_base_datos = 'pizzeria_fratelli'

# Crea la URL de conexión a la base de datos MySQL
url = f'mysql://{usuario}:{contraseña}@{host}:{puerto}/{nombre_base_datos}'

# Crea una instancia de la clase create_engine
engine = create_engine(url)

# Crea una clase que se utilizará para crear objetos de sesión de base de datos
Session = sessionmaker(bind=engine)

# Crea un objeto de sesión de base de datos que se utilizará para enviar consultas a la base de datos.
session = Session()

Base = declarative_base()

class Sucursal(Base):
    __tablename__ = 'sucursal'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50))
    direccion = Column(String(100))
    telefono = Column(String(20))
    inventario = relationship('Inventario', back_populates='sucursal')
    ventas = relationship('Venta', back_populates='sucursal')

class Ingrediente(Base):
    __tablename__ = 'ingrediente'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50))
    stock = Column(Integer)
    precio_unitario = Column(Integer)

class Inventario(Base):
    __tablename__ = 'inventario'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sucursal_id = Column(Integer, ForeignKey('sucursal.id'))
    ingrediente_id = Column(Integer, ForeignKey('ingrediente.id'))
    cantidad = Column(Integer)
    sucursal = relationship('Sucursal', back_populates='inventario')
    ingrediente = relationship('Ingrediente', back_populates='inventario')

class Persona(Base):
    __tablename__ = 'persona'
    rut = Column(String(12), primary_key=True)
    nombre = Column(String(50))
    apellido = Column(String(50))
    email = Column(String(50))
    ventas = relationship('Venta', back_populates='cliente')

class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_usuario = Column(String(50))
    contrasena = Column(String(50))
    es_administrador = Column(Boolean)
    ventas = relationship('Venta', back_populates='vendedor')

class Venta(Base):
    __tablename__ = 'venta'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sucursal_id = Column(Integer, ForeignKey('sucursal.id'))
    cliente_rut = Column(String(12), ForeignKey('persona.rut'))
    vendedor_id = Column(Integer, ForeignKey('usuario.id'))
    fecha = Column(DateTime)
    total = Column(Integer)
    detalles = relationship('DetalleVenta', back_populates='venta')
    sucursal = relationship('Sucursal', back_populates='ventas')
    cliente = relationship('Persona', back_populates='ventas')
    vendedor = relationship('Usuario', back_populates='ventas')

class DetalleVenta(Base):
    __tablename__ = 'detalle_venta'
    id = Column(Integer, primary_key=True, autoincrement=True)
    venta_id = Column(Integer, ForeignKey('venta.id'))
    ingrediente_id = Column(Integer, ForeignKey('ingrediente.id'))
    cantidad = Column(Integer)
    precio_unitario = Column(Integer)
    venta = relationship('Venta', back_populates='detalles')
    ingrediente = relationship('Ingrediente')

# crear las tablas en caso que no existan
Base.metadata.create_all(engine)