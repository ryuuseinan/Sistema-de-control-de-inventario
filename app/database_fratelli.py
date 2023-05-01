from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean
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

class Ingrediente(Base):
    __tablename__ = 'ingrediente'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50))
    precio_unitario = Column(Integer)

class TamanoPizza(Base):
    __tablename__ = 'tamano_pizza'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50))
    precio = Column(Integer)

class Pizza(Base):
    __tablename__ = 'pizza'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50))
    precio = Column(Integer)
    tamano_id = Column(Integer, ForeignKey('tamano_pizza.id'))
    tamano = relationship('TamanoPizza')

class Receta(Base):
    __tablename__ = 'receta'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pizza_id = Column(Integer, ForeignKey('pizza.id'))
    ingrediente_id = Column(Integer, ForeignKey('ingrediente.id'))
    cantidad = Column(Integer)
    pizza = relationship('Pizza', back_populates='recetas')
    ingrediente = relationship('Ingrediente', back_populates='recetas')

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

class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50))
    contrasena = Column(String(50))
    es_administrador = Column(Boolean, default=False)

class Venta(Base):
    __tablename__ = 'venta'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(String(20))
    total = Column(Integer)
    cliente_rut = Column(String(12), ForeignKey('persona.rut'))
    cliente = relationship('Persona', back_populates='ventas')
    vendedor_id = Column(Integer, ForeignKey('usuario.id'))
    vendedor = relationship('Usuario', back_populates='ventas')
    detalles = relationship('DetalleVenta', back_populates='venta')

class DetalleVenta(Base):
    __tablename__ = 'detalle_venta'
    id = Column(Integer, primary_key=True, autoincrement=True)
    venta_id = Column(Integer, ForeignKey('venta.id'))
    pizza_id = Column(Integer, ForeignKey('pizza.id'))
    cantidad = Column(Integer)
    precio_unitario = Column(Integer)
    subtotal = Column(Integer)
    venta = relationship('Venta', back_populates='detalles')
   
Base.metadata.create_all(engine)