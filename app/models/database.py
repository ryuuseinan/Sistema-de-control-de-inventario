from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean, Text, Float
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config import *
# Crear objeto de base de datos SQLAlchemy
db = SQLAlchemy()

# Crea la URL de conexión a la base de datos MySQL
url = f'mysql://{usuario_db}:{contrasena_db}@{host_db}:{puerto_db}/{nombre_base_datos_db}'

# Crea una instancia de la clase create_engine
engine = create_engine(url)

# Crea una clase que se utilizará para crear objetos de sesión de base de datos
Session = sessionmaker(bind=engine)

# Crea un objeto de sesión de base de datos que se utilizará para enviar consultas a la base de datos.
db_session = Session()

Base = declarative_base()

# Creamos tabla para almacenar usuarios
class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True)
    nombre_usuario = Column(String(50), unique=True, nullable=False)
    correo = Column(String(255), unique=True, nullable=False)
    contrasena = Column(String(60), nullable=False)
    rol_id = Column(Integer, ForeignKey('rol.id'))
    fecha_creacion = Column(DateTime, default=datetime.now(), nullable=False)
    ultima_modificacion = Column(DateTime, default=datetime.now(), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)
    # Crea la relación con Rol
    rol = relationship('Rol')

class Rol(Base):
    __tablename__ = 'rol'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)
    activo = Column(Boolean, default=True, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.now(), nullable=False)
    ultima_modificacion = Column(DateTime, default=datetime.now(), nullable=False)

# Creamos tabla para almacenar personas
class Persona(Base):
    __tablename__ = 'persona'
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    rut = Column(String(12), unique=True, nullable=False)
    nombre = Column(String(30), nullable=False)
    apellido_paterno = Column(String(30), nullable=False)
    apellido_materno = Column(String(30), nullable=False)
    celular = Column(String(22), nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.now(), nullable=False)
    ultima_modificacion = Column(DateTime, default=datetime.now(), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)
    # Crea la relación con Usuario
    usuario = relationship('Usuario')

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
    tiene_receta = Column(Boolean, default=True, nullable=False)
    categoria_id = Column(Integer, ForeignKey('categoria.id'))
    fecha_creacion = Column(DateTime, default=datetime.now(), nullable=False)
    ultima_modificacion = Column(DateTime, default=datetime.now(), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)
    # Crea la relación con Categoría
    categoria = relationship('Categoria')

# Creamos tabla para almacenar ingredientes
class Ingrediente(Base):
    __tablename__ = 'ingrediente'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    cantidad = Column(Integer, nullable=False)
    activo = Column(Boolean, default=True, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.now(), nullable=False)
    ultima_modificacion = Column(DateTime, default=datetime.now(), nullable=False)
    unidadmedida_id = Column(Integer, ForeignKey('unidadmedida.id'))
    # Crea la relación con UnidadMedida
    unidadmedida = relationship('UnidadMedida')

class UnidadMedida(Base):
    __tablename__ = 'unidadmedida'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(10), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.now(), nullable=False)
    ultima_modificacion = Column(DateTime, default=datetime.now(), nullable=False)

# Creamos tabla para almacenar las recetas
class Receta(Base):
    __tablename__ = 'receta'
    id = Column(Integer, primary_key=True)
    producto_id = Column(Integer, ForeignKey('producto.id'))
    ingrediente_id = Column(Integer, ForeignKey('ingrediente.id'))
    cantidad = Column(Integer, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.now(), nullable=False)
    ultima_modificacion = Column(DateTime, default=datetime.now(), nullable=False)
    producto = relationship('Producto', backref='recetas')
    ingrediente = relationship('Ingrediente')

    def verificar_stock_suficiente(self):
        """
        Verifica si hay suficiente stock de ingredientes para realizar el producto.
        Retorna True si hay suficiente stock, False en caso contrario.
        """
        return self.ingrediente.activo and self.cantidad <= self.ingrediente.stock
    
class RecetaDetalle(Base):
    __tablename__ = 'receta_detalle'
    id = Column(Integer, primary_key=True)
    receta_id = Column(Integer, ForeignKey('receta.id'))
    paso = Column(Integer, nullable=False)
    descripcion = Column(Text, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.now(), nullable=False)
    ultima_modificacion = Column(DateTime, default=datetime.now(), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)
    # Crea la relación con Receta
    receta = relationship('Receta', backref='detalles')

Base.metadata.create_all(engine)

unidad_medida_gr = db_session.query(UnidadMedida).filter_by(nombre='gr').first()
unidad_medida_ml = db_session.query(UnidadMedida).filter_by(nombre='ml').first()
unidad_medida_unidades = db_session.query(UnidadMedida).filter_by(nombre='Unidades').first()

if not unidad_medida_gr:
    unidad_medida_gr = UnidadMedida(nombre='gr', activo=True)
    db_session.add(unidad_medida_gr)

if not unidad_medida_ml:
    unidad_medida_ml = UnidadMedida(nombre='ml', activo=True)
    db_session.add(unidad_medida_ml)

if not unidad_medida_ml:
    unidad_medida_ml = UnidadMedida(nombre='Unidades', activo=True)
    db_session.add(unidad_medida_unidades)
    
rol_administrador = db_session.query(Rol).filter_by(nombre='Administrador').first()
rol_caja = db_session.query(Rol).filter_by(nombre='Personal de caja').first()
rol_empleado = db_session.query(Rol).filter_by(nombre='Empleado').first()

if not rol_administrador:
    rol_administrador = Rol(nombre='Administrador', activo=True)
    db_session.add(rol_administrador)

if not rol_caja:
    rol_caja = Rol(nombre='Personal de caja', activo=True)
    db_session.add(rol_caja)

if not rol_empleado:
    rol_empleado = Rol(nombre='Empleado', activo=True)
    db_session.add(rol_empleado)

# Verificar si el usuario ya existe
usuario_existente = db_session.query(Usuario).filter_by(nombre_usuario='galvezluis').first()

if usuario_existente:
    print("El usuario ya existe en la base de datos.")
else:
    # Verificar si el rol existe
    rol = db_session.query(Rol).filter_by(id=1).first()

    if rol:
        usuario = Usuario(nombre_usuario='galvezluis', correo='galvezluis72@gmail.com', contrasena='$2b$12$NJ/4JWBugLVU0pJjIfMcne9NqDk/.zLpotKLUAqXUes4FG7GZ/..O', rol_id=rol.id, fecha_creacion=datetime.now(), ultima_modificacion=datetime.now(), activo=True)
        db_session.merge(usuario)
        db_session.commit()
    else:
        print("El rol con id 1 no existe en la base de datos.")

# Verificar si el usuario existe
usuario = db_session.query(Usuario).filter_by(id=1).first()

if usuario:
    # Verificar si la persona existe
    persona_existente = db_session.query(Persona).filter_by(usuario_id=usuario.id).first()

    if persona_existente:
        print("La persona ya existe en la base de datos.")
    else:
        persona = Persona(usuario_id=usuario.id, rut='20704339-7', nombre='Luis', apellido_paterno='Gálvez', apellido_materno='González', celular='935257778', activo=True)
        db_session.merge(persona)
        db_session.commit()
else:
    print("El usuario con id 1 no existe en la base de datos.")

db_session.commit()