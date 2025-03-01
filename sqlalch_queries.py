from sqlalchemy import insert, select, join
from sqlalchemy.orm import sessionmaker
from scrap_url import scrap_rtr_crawler
from models import engine, Articulo, HistorialPrecio


### CREAMOS LA SESSION ###

# Crear una sesión - Conexión que nos permite interactuar con la base de datos
Session = sessionmaker(bind=engine)

def get_session():
    session = Session()
    try:
        return session
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()





### FUNCIONES INSERT ###

# Convertimos el Return en Dict para importar en lote con SQLAlchemy
def scraped_to_dict(list_productos_tuplas):
    scraped_dict_lst = []
    for cat, rtr_id, nombre, precio, ean, art_url, img_url in list_productos_tuplas:
        producto = {
            'categoria': cat,
            'rtr_id': rtr_id,
            'nombre': nombre,
            'precio': precio,
            'ean': ean,
            'art_url': art_url,
            'img_url': img_url
        }
        scraped_dict_lst.append(producto)
    return scraped_dict_lst

# Insertar artículos desde scrapping
def insert_scraped(list_products=None):
    products_dict = scraped_to_dict(list_products)
    for product in products_dict[:10]:
        print('\n')
        print(product)
    session = get_session()
    try:
        session.execute(insert(Articulo), products_dict)
        session.execute(insert(HistorialPrecio), products_dict)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()





### FUNCIONES SELECT ###

# Leer todo de tabla articulos y printea algunos datos
def leer_tabla():
    session = get_session()
    try:
        stmt = select(Articulo)
        result = session.execute(stmt)
        for user_obj in result.scalars():
            print(f"{user_obj.nombre} {user_obj.rtr_id}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

# Leer tabla ordenada por rtr_id
def leer_tabla_ordenada():
    session = get_session()
    try:
        stmt = select(Articulo).order_by(Articulo.rtr_id)
        result = session.execute(stmt)
        for user_obj in result.scalars():
            print(f"{user_obj.nombre} {user_obj.rtr_id}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

# Consultas con JOIN
def leer_historial_precios_con_nombre():
    session = get_session()
    try:
        stmt = select(HistorialPrecio, Articulo.nombre).select_from(
            join(HistorialPrecio, Articulo, HistorialPrecio.rtr_id == Articulo.rtr_id)
        )
        result = session.execute(stmt)
        for historial, nombre in result:
            print(f"Artículo: {nombre}, RTR ID: {historial.rtr_id}, Precio: {historial.precio}, Fecha: {historial.fecha}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

def leer_historial_precios_con_nombre_y_categoria():
    session = get_session()
    try:
        stmt = select(HistorialPrecio, Articulo.nombre, Articulo.categoria).select_from(
            join(HistorialPrecio, Articulo, HistorialPrecio.rtr_id == Articulo.rtr_id)
        )
        result = session.execute(stmt)
        for historial, nombre, categoria in result:
            print(f"Artículo: {nombre}, Categoría: {categoria}, RTR ID: {historial.rtr_id}, Precio: {historial.precio}, Fecha: {historial.fecha}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

