from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config import *

# Crear objeto de base de datos SQLAlchemy
db = SQLAlchemy()

url = f"mysql+pymysql://{mysql['usuario_db']}:{mysql['contrasena_db']}@{mysql['host_db']}:{mysql['puerto_db']}/{mysql['nombre_base_datos_db']}"

# Crea una instancia de la clase create_engine
engine = create_engine(url)

# Crea una clase que se utilizará para crear objetos de sesión de base de datos
Session = sessionmaker(bind=engine)

# Crea un objeto de sesión de base de datos que se utilizará para enviar consultas a la base de datos.
db_session = Session()

Base = declarative_base()

# Usar una base de datos en utf8mb4_general_ci para no tener problemas con el rut.

# Creamos tabla para almacenar usuarios
class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True)
    nombre_usuario = Column(String(30), unique=True, nullable=False)
    correo = Column(String(30), unique=True, nullable=False)
    contrasena = Column(String(255), nullable=False)
    rol_id = Column(Integer, ForeignKey('rol.id'))
    fecha_creacion = Column(DateTime, default=datetime.now(), nullable=False)
    ultima_modificacion = Column(DateTime, default=datetime.now(), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)
    # Crea la relación con Rol
    rol = relationship('Rol')

class Rol(Base):
    __tablename__ = 'rol'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(30), unique=True, nullable=False)
    activo = Column(Boolean, default=True, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.now(), nullable=False)
    ultima_modificacion = Column(DateTime, default=datetime.now(), nullable=False)

# Creamos tabla para almacenar personas
class Persona(Base):
    __tablename__ = 'persona'
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    rut = Column(String(12, collation='utf8mb4_general_ci'), unique=True, nullable=False) 
    nombre = Column(String(30), nullable=False)
    apellido_paterno = Column(String(30), nullable=False)
    apellido_materno = Column(String(30), nullable=False)
    celular = Column(String(12), unique=True, nullable=False)
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
    codigo_barra = Column(String(30), unique=True, nullable=False)
    nombre = Column(String(30), nullable=False)
    descripcion = Column(Text)
    precio = Column(Integer, nullable=False)
    stock = Column(Integer)
    alerta_stock = Column(Integer)
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
    nombre = Column(String(50), unique=True, nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio = Column(Integer, default=1000, nullable=False)
    alerta_stock = Column(Integer, default=1000, nullable=False)
    extra_mediana = Column(Integer, default=100, nullable=False)
    extra_familiar = Column(Integer, default=100, nullable=False)
    activo = Column(Boolean, default=True, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.now(), nullable=False)
    ultima_modificacion = Column(DateTime, default=datetime.now(), nullable=False)
    unidadmedida_id = Column(Integer, ForeignKey('unidadmedida.id'))
    # Crea la relación con UnidadMedida
    unidadmedida = relationship('UnidadMedida')

class UnidadMedida(Base):
    __tablename__ = 'unidadmedida'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(30), unique=True, nullable=False)
    activo = Column(Boolean, default=True, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.now(), nullable=False)
    ultima_modificacion = Column(DateTime, default=datetime.now(), nullable=False)
    
class Receta(Base):
    __tablename__ = 'receta'
    id = Column(Integer, primary_key=True)
    producto_id = Column(Integer, ForeignKey('producto.id'))
    fecha_creacion = Column(DateTime, default=datetime.now(), nullable=False)
    ultima_modificacion = Column(DateTime, default=datetime.now(), nullable=False)
    producto = relationship('Producto')
    detalles = relationship('RecetaDetalle', backref='receta')

    def verificar_stock_suficiente(self):
        """
        Verifica si hay suficiente stock de ingredientes para realizar el producto.
        Retorna True si hay suficiente stock, False en caso contrario.
        """
        return all(detalle.ingrediente.activo and detalle.cantidad <= detalle.ingrediente.stock for detalle in self.detalles)

class RecetaDetalle(Base):
    __tablename__ = 'receta_detalle'
    id = Column(Integer, primary_key=True)
    cantidad = Column(Integer, nullable=False)
    receta_id = Column(Integer, ForeignKey('receta.id'))
    ingrediente_id = Column(Integer, ForeignKey('ingrediente.id'))
    fecha_creacion = Column(DateTime, default=datetime.now(), nullable=False)
    ultima_modificacion = Column(DateTime, default=datetime.now(), nullable=False)
    # Crea la relación con Ingrediente
    ingrediente = relationship('Ingrediente')

class Pedido(Base):
    __tablename__ = 'pedido'
    id = Column(Integer, primary_key=True)
    persona_id = Column(Integer, ForeignKey('persona.id'))
    estado_id = Column(Integer, ForeignKey('pedido_estado.id'), default=1, nullable=False)
    metodopago_id = Column(Integer, ForeignKey('metodopago.id'))
    delivery = Column(Boolean, default=False, nullable=False)
    nombre_cliente = Column(String(50), default='No definido', nullable=False)
    notificacion = Column(Boolean, default=False, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.now(), nullable=False)
    ultima_modificacion = Column(DateTime, default=datetime.now(), nullable=False)
    # Crea la relación con persona
    persona = relationship('Persona')
    pedido_estado = relationship('PedidoEstado')
    detalles = relationship('PedidoDetalle', backref='pedido_detalles')
    venta = relationship('Venta', back_populates='pedido')

class MetodoPago(Base):
    __tablename__ = 'metodopago'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)
    activo = Column(Boolean, default=True, nullable=False)
    # Crea la relación con persona
    pedido = relationship('Pedido')

class PedidoEstado(Base):
    __tablename__ = 'pedido_estado'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)

class PedidoDetalle(Base):
    __tablename__ = 'pedido_detalle'
    id = Column(Integer, primary_key=True)
    pedido_id = Column(Integer, ForeignKey('pedido.id'))
    producto_id = Column(Integer, ForeignKey('producto.id'))
    cantidad = Column(Integer, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.now(), nullable=False)
    ultima_modificacion = Column(DateTime, default=datetime.now(), nullable=False)

    producto = relationship('Producto')

class Venta(Base):
    __tablename__ = 'venta'
    id = Column(Integer, primary_key=True)
    pedido_id = Column(Integer, ForeignKey('pedido.id'))
    total = Column(Integer)
    activo = Column(Boolean, default=True, nullable=False)

    pedido = relationship('Pedido', back_populates='venta')

class PedidoDetalleIngrediente(Base):
    __tablename__ = 'pedido_detalle_ingrediente'
    id = Column(Integer, primary_key=True)
    pedido_detalle_id = Column(Integer, ForeignKey('pedido_detalle.id'))
    ingrediente_id = Column(Integer, ForeignKey('ingrediente.id'))
    cantidad = Column(Integer, nullable=False)
    pedido_detalle = relationship('PedidoDetalle')
    ingrediente = relationship('Ingrediente')

Base.metadata.create_all(engine)

metodo_pago_0 = db_session.query(MetodoPago).filter_by(nombre='Efectivo').first()
metodo_pago_1 = db_session.query(MetodoPago).filter_by(nombre='Transferencia').first()
metodo_pago_2 = db_session.query(MetodoPago).filter_by(nombre='Tarjeta de crédito').first()
metodo_pago_3 = db_session.query(MetodoPago).filter_by(nombre='Tarjeta de débito').first()
metodo_pago_4 = db_session.query(MetodoPago).filter_by(nombre='Cheque').first()

if not metodo_pago_0:
    metodo_pago_0 = MetodoPago(nombre='Efectivo', activo=True)
    db_session.add(metodo_pago_0)

if not metodo_pago_1:
    metodo_pago_1 = MetodoPago(nombre='Transferencia', activo=True)
    db_session.add(metodo_pago_1)

if not metodo_pago_2:
    metodo_pago_2 = MetodoPago(nombre='Tarjeta de crédito', activo=True)
    db_session.add(metodo_pago_2)

if not metodo_pago_3:
    metodo_pago_3 = MetodoPago(nombre='Tarjeta de débito', activo=True)
    db_session.add(metodo_pago_3)

if not metodo_pago_4:
    metodo_pago_4 = MetodoPago(nombre='Cheque', activo=False)
    db_session.add(metodo_pago_4)

unidad_medida_gr = db_session.query(UnidadMedida).filter_by(nombre='gr').first()
unidad_medida_ml = db_session.query(UnidadMedida).filter_by(nombre='ml').first()
unidad_medida_unidades = db_session.query(UnidadMedida).filter_by(nombre='Unidad(es)').first()

if not unidad_medida_gr:
    unidad_medida_gr = UnidadMedida(nombre='gr', activo=True)
    db_session.add(unidad_medida_gr)

if not unidad_medida_ml:
    unidad_medida_ml = UnidadMedida(nombre='ml', activo=True)
    db_session.add(unidad_medida_ml)

if not unidad_medida_unidades:
    unidad_medida_unidades = UnidadMedida(nombre='Unidad(es)', activo=True)
    db_session.add(unidad_medida_unidades)

pedido_estado_0 = db_session.query(PedidoEstado).filter_by(nombre='En proceso').first()
pedido_estado_1 = db_session.query(PedidoEstado).filter_by(nombre='Finalizado').first()
pedido_estado_2 = db_session.query(PedidoEstado).filter_by(nombre='Anulado').first()

if not pedido_estado_0:
    pedido_estado_0 = PedidoEstado(nombre='En proceso')
    db_session.add(pedido_estado_0)

if not pedido_estado_1:
    pedido_estado_1 = PedidoEstado(nombre='Finalizado')
    db_session.add(pedido_estado_1)

if not pedido_estado_2:
    pedido_estado_2 = PedidoEstado(nombre='Anulado')
    db_session.add(pedido_estado_2)

categoria_pizzamediana = db_session.query(Categoria).filter_by(nombre='Pizza mediana').first()
categoria_pizzafamiliar = db_session.query(Categoria).filter_by(nombre='Pizza familiar').first()
categoria_bebestibles = db_session.query(Categoria).filter_by(nombre='Bebestibles').first()

if not categoria_pizzamediana:
    categoria_pizzamediana = Categoria(nombre='Pizza mediana')
    db_session.add(categoria_pizzamediana)

if not categoria_pizzafamiliar:
    categoria_pizzafamiliar = Categoria(nombre='Pizza familiar')
    db_session.add(categoria_pizzafamiliar)

if not categoria_bebestibles:
    categoria_bebestibles = Categoria(nombre='Bebestibles')
    db_session.add(categoria_bebestibles)
    
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