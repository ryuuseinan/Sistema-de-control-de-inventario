from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.database import Pedido, PedidoEstado, Producto, Categoria, Receta, RecetaDetalle, PedidoDetalle, PedidoDetalleIngrediente, Venta, Ingrediente, db_session
from sqlalchemy import or_, func, and_
from datetime import date
import calendar
import matplotlib.pyplot as plt
import io

reporte_controller = Blueprint('reporte_controller', __name__)
def create_reporte_blueprint():
    # Crear el objeto Blueprint
    reporte_blueprint = Blueprint('reporte', __name__)

    # Definir las rutas y las funciones controladoras
    @reporte_blueprint.route('/reporte/inventario')
    def inventario():
        try:
            productos = db_session.query(Producto).filter(Producto.activo == True).all()
            for producto in productos:
                receta = db_session.query(Receta).filter_by(producto_id=producto.id).first()
                if receta:
                    receta_detalles = db_session.query(RecetaDetalle).filter_by(receta_id=receta.id).all()
                    ingredientes = [detalle.ingrediente for detalle in receta_detalles]
                    producto.receta = receta
                    producto.receta_detalles = receta_detalles
                    producto.ingredientes = ingredientes
                    producto.stock_disponible = (
                        producto.stock if not producto.tiene_receta else min(
                            [ingrediente.cantidad // detalle.cantidad for ingrediente, detalle in
                            zip(ingredientes, receta_detalles)])
                    )
                else:
                    producto.receta = None
                    producto.receta_detalles = []
                    producto.ingredientes = []
                    producto.stock_disponible = producto.stock

            ingredientes = db_session.query(Ingrediente).filter(Ingrediente.activo == True).order_by(Ingrediente.nombre).all()
            total_ingredientes = db_session.query(func.count()).filter(Ingrediente.activo == True).scalar()

            total_productos = db_session.query(func.count()).filter(Producto.activo == True).scalar()
            
            ingrediente_alerta_stock = db_session.query(func.count()).filter(Ingrediente.cantidad <= Ingrediente.alerta_stock, Ingrediente.activo == True).order_by(Ingrediente.nombre).scalar()
            print(ingrediente_alerta_stock)

            ingredientes_criticos = db_session.query(Ingrediente).filter(Ingrediente.cantidad <= Ingrediente.alerta_stock, Ingrediente.activo == True).order_by(Ingrediente.nombre).all()
            print(ingredientes_criticos)

            productos_criticos = [producto for producto in productos if producto.stock_disponible is not None and producto.stock_disponible <= producto.alerta_stock]
            producto_alerta_stock = len(productos_criticos)
            
            umbral_proporcional = 0.50  # Ajusta el valor proporcional según tus necesidades

            productos_cerca_alerta = [producto for producto in productos if producto.stock_disponible is not None and producto.stock_disponible <= producto.alerta_stock * (1 + umbral_proporcional) and producto.stock_disponible > producto.alerta_stock]
        
            ingredientes_cerca_alerta = db_session.query(Ingrediente).filter(
                Ingrediente.cantidad <= Ingrediente.alerta_stock * (1 + umbral_proporcional),
                Ingrediente.cantidad > Ingrediente.alerta_stock,
                Ingrediente.activo == True
            ).order_by(Ingrediente.nombre).all()

            print(productos_cerca_alerta)

            return render_template('reporte/inventario.html', 
                                ingrediente_alerta_stock=ingrediente_alerta_stock, 
                                ingredientes_criticos=ingredientes_criticos,
                                total_ingredientes=total_ingredientes,
                                ingredientes=ingredientes,
                                ingredientes_cerca_alerta=ingredientes_cerca_alerta,
                                total_productos=total_productos,
                                producto_alerta_stock=producto_alerta_stock,
                                productos_cerca_alerta=productos_cerca_alerta,
                                productos_criticos=productos_criticos,
                                productos=productos)
        except Exception as e:
            # Manejo de excepciones
            return render_template('error.html', error=str(e))
    
    @reporte_blueprint.route('/reporte/ventas')
    def ventas():
        try:
            ventas = db_session.query(Venta).filter(Venta.activo == True).all()

            ventas_por_mes = {}

            for venta in ventas:
                fecha_creacion = venta.pedido.fecha_creacion.date()
                total = venta.total
                mes = fecha_creacion.month

                if mes in ventas_por_mes:
                    ventas_por_mes[mes].append((fecha_creacion, total))
                else:
                    ventas_por_mes[mes] = [(fecha_creacion, total)]

            fecha_actual = date.today()
            monthrange = calendar.monthrange

            meses_ventas = []

            for mes, ventas_dia in ventas_por_mes.items():
                dias_mes = range(1, monthrange(fecha_actual.year, mes)[1] + 1)
                ventas_por_dia = {dia: 0 for dia in dias_mes}

                for venta in ventas_dia:
                    fecha = venta[0]
                    total = venta[1]
                    dia = fecha.day
                    ventas_por_dia[dia] += total

                dias_con_ventas = get_dias_con_ventas(dias_mes, ventas_por_mes)
                dias_sin_ventas = get_dias_sin_ventas(dias_mes, ventas_por_mes, dias_con_ventas)

                meses_ventas.append({
                    'mes': mes,
                    'nombre': mes_nombre(mes),
                    'ventas_por_dia': ventas_por_dia,
                    'dias_con_ventas': dias_con_ventas,
                    'dias_sin_ventas': dias_sin_ventas
                })

            print(meses_ventas)
            
            return render_template('reporte/ventas.html', meses_ventas=meses_ventas, ventas_por_mes=ventas_por_mes, mes_nombre=mes_nombre, fecha_actual=fecha_actual, get_dias_sin_ventas=get_dias_sin_ventas, monthrange=monthrange, date=date)
        except Exception as e:
            # Manejo de excepciones
            return render_template('error.html', error=str(e))

    def mes_nombre(mes):
        traducciones = {
            1: "Enero",
            2: "Febrero",
            3: "Marzo",
            4: "Abril",
            5: "Mayo",
            6: "Junio",
            7: "Julio",
            8: "Agosto",
            9: "Septiembre",
            10: "Octubre",
            11: "Noviembre",
            12: "Diciembre"
        }
        return traducciones.get(mes, "")

    def get_dias_con_ventas(dias_mes, ventas_por_mes):
        dias_con_ventas = set(venta[0].day for ventas_dia in ventas_por_mes.values() for venta in ventas_dia)
        return dias_con_ventas

    def get_dias_sin_ventas(dias_mes, ventas_por_mes, dias_con_ventas):
        dias_sin_ventas = [dia for dia in dias_mes if dia not in dias_con_ventas]
        return dias_sin_ventas

    # Devolver el blueprint
    return reporte_blueprint
