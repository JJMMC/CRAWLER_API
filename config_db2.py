import sqlite3 as sql
import datetime
from scrap_url import get_items_data, request_categorias_and_main_urls, find_child_urls

path = "database/rtr_crawler_db2.db"


def create_tables ():
    with sql.connect(path) as connection:
        cursor = connection.cursor()

        #Creamos tabla HISTORIAL PRECIOS
        instruction = '''
        CREATE TABLE IF NOT EXISTS historial_precios (
    	id INTEGER PRIMARY KEY AUTOINCREMENT,
    	articulo_id INTEGER,
    	precio REAL NOT NULL,
    	fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    	FOREIGN KEY (articulo_id) REFERENCES articulos(id)
		);
        '''
        cursor.execute(instruction)
        connection.commit()
        print("Tabla -precios- creada correctamente")
        
        #Creamos tabla ARTÍCULOS
        instruction = '''
        CREATE TABLE IF NOT EXISTS articulos (
    	id INTEGER PRIMARY KEY AUTOINCREMENT,
    	nombre TEXT NOT NULL UNIQUE,
    	categoria TEXT
		);
        '''
        cursor.execute(instruction)
        connection.commit()
        print("Tabla -articulos- creada correctamente")

def data_from_old_db(path = 'database/rtr_crawler_db.db'):
    with sql.connect(path) as connection:
        cursor = connection.cursor()
        cursor.execute('''SELECT categoria, articulo, precio, fecha FROM precios ''')
        old_db = cursor.fetchall()        
    return old_db

def obtener_articulo_id():
    with sql.connect(path) as connection:
        cursor = connection.cursor()
        cursor.execute('''SELECT id, nombre FROM articulos ''')
        id_name_lst = cursor.fetchall()        
    return id_name_lst


# Función para agregar un artículo
def agregar_articulo(nombre, categoria):
    with sql.connect(path) as connection:
        cursor = connection.cursor()
        instruction = '''INSERT OR IGNORE INTO articulos (nombre, categoria)
                         VALUES (?, ?)'''
        cursor.execute(instruction, (nombre, categoria))
        connection.commit()

def transfer_db_articles():
    old_db = data_from_old_db() #List tuplas
    #id_nom_lst = obtener_articulo_id() #List tuplas
    #nom_lst = [nom for id, nom in id_nom_lst] #Desempaquetamos y creamos lista de nombres unicos
    for cat, nom, pre, fecha in old_db:
        nom_lst = [nom for id, nom in obtener_articulo_id()] #Desempaquetamos y creamos lista de nombres unicos
        if nom not in nom_lst:
            agregar_articulo(nom,cat)
            print("El artículo no está en la lista, agregamos artículo")
        else:
            print("el artículo SI está en la lista")
            continue

# Función para agregar el precio de un artículo al historial
def agregar_precio(articulo_id, precio, fecha):
    with sql.connect(path) as connection:
        cursor = connection.cursor()
        instruction = '''INSERT INTO historial_precios (articulo_id, precio, fecha) 
                      VALUES (?, ?, ?)'''
        cursor.execute(instruction, (articulo_id, precio, fecha))
        connection.commit()

def borrar_datos_tabla(tabla='historial_precios'):
    with sql.connect(path) as connection:
        cursor = connection.cursor()
        instruction = f"DELETE FROM {tabla}"
        cursor.execute(instruction)
        connection.commit()
        cursor.execute("VACUUM")
        print(f"Todos los datos de la tabla {tabla} han sido borrados y el contador AUTOINCREMENT ha sido reiniciado.")


def check_article_id_and_import(new_cat, new_nom, new_pre, new_fech):
    id_nom_lst = obtener_articulo_id()
    for articulo_id, nombre in id_nom_lst:
        if new_nom == nombre:
            print(f'El artículo:{new_nom} ya existe, su id de artículo es: {articulo_id}')
            print(f'guardamos precio y fecha')
            agregar_precio(articulo_id, new_pre, new_fech)
        else:
            continue

def eliminar_tabla(tabla='historial_precios'):
    with sql.connect(path) as connection:
        cursor = connection.cursor()
        instruction = f"DROP TABLE IF EXISTS {tabla}"
        cursor.execute(instruction)
        connection.commit()
        print(f"La tabla {tabla} ha sido eliminada.")



for cat, nomb, precio, fecha in data_from_old_db():
    print(f'El item {nomb}, con precio {precio}')
    check_article_id_and_import(cat, nomb, precio, fecha)


