import sqlite3
from querys_db import list_of_tables

# Función para obtener los precios de los productos de una base de datos
def obtener_precios(db_path,tabla="Coches"):
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Obtener los precios de todos los productos
    cursor.execute(f"SELECT nombre_it, precio_it FROM {tabla}")
    precios = cursor.fetchall()# Retorna lista de tuplas (nombre_it,precio_it)
    
    # Cerrar la conexión
    conn.close()

    # Devolver un diccionario con el id del producto como clave y el precio como valor
    return {producto_id: precio for producto_id, precio in precios}
#print("\n",obtener_precios("database/rtr_db2.db"),"\n")


# Función para comparar los precios entre dos bases de datos
def comparar_precios(db1_path, db2_path,lista="Coches"):
    # Obtener los precios de ambas bases de datos
    precios_db1 = obtener_precios(db1_path,lista)
    precios_db2 = obtener_precios(db2_path,lista)

    # Comparar los precios de ambas bases de datos
    productos_cambiados = []
    
    # Comprobar si los precios en ambas bases de datos son iguales
    for producto_id in precios_db1:
        if producto_id in precios_db2:
            if precios_db1[producto_id] != precios_db2[producto_id]:
                productos_cambiados.append((producto_id, precios_db1[producto_id], precios_db2[producto_id]))

    # Mostrar los productos cuyos precios han cambiado
    if productos_cambiados:
        print("Los siguientes productos tienen precios diferentes entre las bases de datos:")
        for producto_id, precio_db1, precio_db2 in productos_cambiados:
            print(f"Producto ID: {producto_id} - Precio DB1: {precio_db1} - Precio DB2: {precio_db2} - Ahorras: {precio_db1-precio_db2}")
    else:
        print("No se encontraron cambios en los precios.")
    return productos_cambiados


# Rutas de las dos bases de datos SQLite
db1_path = 'database/rtr_db2.db'
db2_path = 'database/rtr_db3.db'

# Comparar precios entre las dos bases de datos de una tabla
def compare_table():    
    return comparar_precios(db1_path, db2_path)

# Comparar precios de todas las tablas de la BD
def compare_all():
    categorias = list_of_tables()
    for tabla in categorias:
        comparar_precios(db1_path, db2_path,tabla)
	
#print (compare_table())
#print (compare_all())
  
 

